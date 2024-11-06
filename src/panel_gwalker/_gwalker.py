import asyncio
import json
import sys
import uuid
from os import PathLike
from pathlib import Path
from typing import Any, Callable, Concatenate, Coroutine, Literal, Optional, ParamSpec

import numpy as np
import pandas as pd
import param
from panel import config
from panel.custom import ReactComponent
from panel.io.state import state
from panel.layout import Column
from panel.pane import Markdown
from panel.viewable import Viewer
from panel.widgets import Button, IntInput, RadioButtonGroup, TextInput

from panel_gwalker._pygwalker import get_data_parser, get_sql_from_payload
from panel_gwalker._utils import (
    SPECTYPES,
    SpecType,
    _raw_fields,
    configure_debug_log_level,
    logger,
    process_spec,
)

VERSION = "0.4.72"

P = ParamSpec("P")


# Can be replaced with ClassSelector once https://github.com/holoviz/panel/pull/7454 is released
class Spec(param.Parameter):
    """
    A parameter that holds a chart specification.
    """

    def _validate(self, val):
        if not isinstance(val, SPECTYPES):
            spec_types = ",".join(SPECTYPES)
            msg = f"Spec must be a {spec_types}. Got '{type(val).__name__}'."
            raise ValueError(msg)
        return val


def _label(value):
    return Markdown(value, margin=(-10, 10))


def create_export_settings(walker: "GraphicWalker", **params) -> Column:
    """Returns a UI component to set the `export_scope`, `export_mode` and `export_timeout` parameters.

    Args:
        walker (GraphicWalker): The GraphicWalker to create the UI Component for.

    Returns:
        Column: The component.
    """
    mode = RadioButtonGroup.from_param(
        walker.param.export_mode,
        button_style="outline",
        button_type="primary",
        **params,
    )
    scope = RadioButtonGroup.from_param(
        walker.param.export_scope,
        button_style="outline",
        button_type="primary",
        **params,
    )
    timeout = IntInput.from_param(walker.param.export_timeout, **params)
    return Column(mode, scope, timeout)


def _extract_layout_params(params):
    layout_params = {}
    for key in ["sizing_mode", "width", "max_width"]:
        if key in params:
            layout_params[key] = params.pop(key)
    return layout_params


class ExportButton(Viewer):
    """A UI component to export the Chart(s) spec of SVG(s)"""

    value: list | dict = param.ClassSelector(
        class_=(list, dict), doc="""The exported Chart(s) spec or SVG."""
    )

    export: bool = param.Event(doc="""Click to export.""")

    def __init__(
        self,
        walker: "GraphicWalker",
        icon: str = "download",
        name: str = "Export",
        description: str = "Click to export",
        include_settings: bool = True,
        **params,
    ):
        layout_params = _extract_layout_params(params)
        super().__init__(**params)
        self._walker = walker

        if include_settings:
            settings = create_export_settings(walker, **layout_params)
        else:
            settings = []

        # Should be changed to IconButton once https://github.com/holoviz/panel/issues/7458 is fixed.
        button = Button.from_param(
            self.param.export,
            icon=icon,
            name=name,
            description=description,
            **layout_params,
        )
        self._layout = Column(
            *settings,
            button,
        )

    def __panel__(self):
        return self._layout

    @param.depends("export", watch=True)
    async def _export(self):
        try:
            self.value = await self._walker.export()
        except TimeoutError as ex:
            self.value = {"TimeoutError": str(ex)}


class SaveButton(Viewer):
    """A UI component to save the Chart(s) spec of SVG(s).

    Will save to `save_path` path of the `walker`."""

    save: bool = param.Event(doc="""Click to save.""")

    def __init__(
        self,
        walker: "GraphicWalker",
        icon: str = "download",
        name: str = "Save",
        description: str = "Click to save",
        include_settings: bool = True,
        **params,
    ):
        layout_params = _extract_layout_params(params)
        super().__init__(**params)
        self._walker = walker

        if include_settings:
            settings = create_export_settings(walker, **layout_params)
            if isinstance(walker.save_path, str):
                settings.append(
                    TextInput.from_param(walker.param.save_path, **layout_params)
                )
        else:
            settings = []

        # Should be changed to IconButton once https://github.com/holoviz/panel/issues/7458 is fixed.
        # layout_params.pop("width", None)
        button = Button.from_param(
            self.param.save,
            icon=icon,
            name=name,
            description=description,
            **layout_params,
        )
        self._layout = Column(
            *settings,
            button,
        )

    def __panel__(self):
        return self._layout

    @param.depends("save", watch=True)
    async def _save(self):
        await self._walker.save()


class GraphicWalker(ReactComponent):
    """
    The `GraphicWalker` component enables interactive exploration of data in a DataFrame
    using an interface built on [Graphic Walker](https://docs.kanaries.net/graphic-walker).

    Reference: https://github.com/panel-extensions/panel-graphic-walker.

    Example:
        ```python
        import pandas as pd
        import panel as pn
        from panel_gwalker import GraphicWalker

        pn.extension()

        # Load a sample dataset
        df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz")

        # Display the interactive graphic interface
        GraphicWalker(df).servable()
        ```

    Args:
        `object`: The DataFrame to explore.
        `config`: The Graphic Walker configuration, i.e. the keys `rawFields` and `spec`.
            `i18nLang` is currently not

    Returns:
        Servable `GraphicWalker` object that creates a UI for visual exploration of the input DataFrame.
    """

    object: pd.DataFrame = param.DataFrame(
        doc="""The data to explore.
        Please note that if you update the `object`, then the existing charts will not be deleted."""
    )
    fields: list = param.List(doc="""Optional fields, i.e. columns, specification.""")
    # Can be replaced with ClassSelector once https://github.com/holoviz/panel/pull/7454 is released
    spec: SpecType = Spec(
        doc="""Optional chart specification as url, json, dict or list.
    Can be generated via the `export` method."""
    )
    server_computation: bool = param.Boolean(
        default=False,
        doc="""If True the computations will take place on the Panel server or in the Jupyter kernel
        instead of the client to scale to larger datasets. Default is False. In Pyodide this will
        always be set to False. For the chart renderer computations will always be done in the client.""",
        constant=state._is_pyodide,
    )
    config: dict = param.Dict(
        doc="""Optional extra Graphic Walker configuration. For example `{"i18nLang": "ja-JP"}`. See the
    [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details."""
    )
    renderer: Literal["explorer", "profiler", "viewer", "chart"] = param.Selector(
        default="explorer",
        objects=["explorer", "profiler", "viewer", "chart"],
        doc="""How to display the data. One of 'explorer' (default), 'profiler,
        'viewer' or 'chart'.""",
    )
    index: int | list[int] | None = param.ClassSelector(
        class_=(int, list, type(None)),
        doc="""An optional chart index or list of chart indices to display in the 'viewer' or 'chart' renderer.
    Has no effect on other renderers.""",
    )
    page_size: int = param.Integer(
        20,
        bounds=(1, None),
        doc="""The number of rows per page in the table of the 'profiler' render.
    Has no effect on other renderers.""",
    )
    tab: Literal["data", "vis"] = param.Selector(
        default="vis",
        objects=["data", "vis"],
        doc="""Set the active tab to 'data' or 'vis' (default). Only applicable for the 'explorer' renderer. Not bi-directionally synced with client.""",
    )
    container_height: str = param.String(
        default="400px",
        doc="""The height of a single chart in the 'viewer' or 'chart' renderer. For example '500px' (pixels) or '30vh' (viewport height).""",
    )

    appearance: Literal["media", "dark", "light"] = param.Selector(
        default="light",
        objects=["light", "dark", "media"],
        doc="""Dark mode preference: 'light', 'dark' or 'media'.
        If not provided the appearance is derived from pn.config.theme.""",
    )
    theme_key: Literal["g2", "streamlit", "vega"] = param.Selector(
        default="g2",
        objects=["g2", "streamlit", "vega"],
        doc="""The theme of the chart(s). One of 'g2', 'streamlit' or 'vega' (default).""",
    )

    export_mode: Literal["spec", "svg"] = param.Selector(
        label="Mode",
        default="spec",
        objects=["spec", "svg"],
        doc="""Used as default mode for export and save methods.""",
    )
    export_scope: Literal["all", "current"] = param.Selector(
        label="Scope",
        default="all",
        objects=["all", "current"],
        doc="""Used as default scope for export and save methods.""",
    )
    export_timeout: int = param.Integer(
        label="Timeout",
        default=5000,
        doc="""Export timeout in milliseconds. Used as default for export and save methods.""",
    )
    export: Callable[
        Concatenate[
            Literal["spec", "svg", None],
            Literal["current", "all", None],
            Optional[int],
            P,
        ],
        Coroutine[Any, Any, str],
    ] = param.Action(
        doc="""Exports the chart(s) as either a spec or SVG.""",
        constant=True,
        allow_refs=False,
    )

    save_path: str | PathLike = param.ClassSelector(
        label="Path",
        default="tmp_graphic_walker.json",
        class_=(str, PathLike),
        allow_None=False,
        doc="""Used as default path for the save method.""",
    )
    save: Callable[
        Concatenate[
            str | Path | None,
            Literal["spec", "svg", None],
            Literal["current", "all", None],
            Optional[int],
            P,
        ],
        Coroutine[Any, Any, None],
    ] = param.Action(
        doc="""Saves the chart(s) as either a spec or SVG.""",
        constant=True,
        allow_refs=False,
    )

    _importmap = {
        "imports": {
            "graphic-walker": f"https://esm.sh/@kanaries/graphic-walker@{VERSION}"
        }
    }

    _rename = {
        "export": None,
        "export_mode": None,
        "export_scope": None,
        "export_timeout": None,
        "save": None,
        "save_path": None,
    }

    _esm = "_gwalker.js"

    _THEME_CONFIG = {
        "default": "light",
        "dark": "dark",
    }

    def __init__(self, object=None, **params):
        self.param.export.default = params.pop("export", self._export)
        self.param.save.default = params.pop("save", self._save)

        if "appearance" not in params:
            params["appearance"] = self._get_appearance(config.theme)

        if params.pop("_debug", False):
            configure_debug_log_level()

        if state._is_pyodide:
            params.pop("server_computation", None)

        super().__init__(object=object, **params)
        self._exports = {}

    @classmethod
    def applies(cls, object):
        if isinstance(object, dict) and all(
            isinstance(v, (list, np.ndarray)) for v in object.values()
        ):
            return 0 if object else None
        elif "pandas" in sys.modules:
            import pandas as pd

            if isinstance(object, pd.DataFrame):
                return 0
        return False

    def _get_appearance(self, theme):
        config = self._THEME_CONFIG
        return config.get(theme, self.param.appearance.default)

    @param.depends("object")
    def calculated_fields(self) -> list[dict]:
        """Returns all the fields calculated from the object.

        The calculated fields are a great starting point if you want to customize the fields.
        """
        return _raw_fields(self.object)

    def _process_param_change(self, params):
        if params.get("object") is not None:
            if not self.fields:
                params["fields"] = self.calculated_fields()
            if not self.config:
                params["config"] = {}
            if self.server_computation:
                del params["object"]
        if "spec" in params:
            params["spec"] = process_spec(params["spec"])
        return super()._process_param_change(params)

    def _compute(self, payload):
        logger.debug("request: %s", payload)
        field_specs = self.fields or self.calculated_fields()
        parser = get_data_parser(
            self.object,
            field_specs=field_specs,
            infer_string_to_date=False,
            infer_number_to_dimension=False,
            other_params={},
        )
        try:
            result = parser.get_datas_by_payload(payload)
        except Exception:
            sql = get_sql_from_payload(
                "pygwalker_mid_table",
                payload,
                {"pygwalker_mid_table": parser.field_metas},
            )
            logger.exception("SQL raised exception:\n%s\n\npayload:%s", sql, payload)

        df = pd.DataFrame.from_records(result)
        logger.debug("response:\n%s", df)
        return {col: df[col].values for col in df.columns}

    def _handle_msg(self, msg: Any) -> None:
        action = msg["action"]
        event_id = msg.pop("id")
        if action == "export" and event_id in self._exports:
            self._exports[event_id] = msg["data"]
        elif action == "compute":
            self._send_msg(
                {
                    "action": "compute",
                    "id": event_id,
                    "result": self._compute(msg["payload"]),
                }
            )

    async def _export(
        self,
        mode: Literal["spec", "svg", None] = None,
        scope: Literal["current", "all", None] = None,
        timeout: int | None = None,
    ):
        """
        Requests chart(s) on the frontend to be exported either
        as Vega specs or rendered to SVG.

        Arguments
        ---------
        mode: 'code' | 'svg' | None (default)
           Whether to export the chart specification(s) or the SVG(s). If None the mode is set to the 'export_code' parameter value.
        scope: 'current' | 'all' | None (default)
           Whether to export only the current chart or all charts. If None the scope is set to the 'export_scope' parameter value.
        timeout: int | None (default)
           How long to wait for the response before timing out. If None the timeout is set to the 'export_timeout' parameter value.

        Returns
        -------
        Dictionary containing the exported chart(s).
        """
        mode = mode or self.export_mode
        scope = scope or self.export_scope
        timeout = timeout or self.export_timeout

        event_id = uuid.uuid4().hex
        self._send_msg(
            {"action": "export", "id": event_id, "scope": f"{scope}", "mode": mode}
        )
        wait_count = 0
        self._exports[event_id] = None
        while self._exports[event_id] is None:
            await asyncio.sleep(0.1)
            wait_count += 1
            if (wait_count * 100) > timeout:
                del self._exports[event_id]
                raise TimeoutError(f"Exporting {scope} chart(s) timed out.")
        return self._exports.pop(event_id)

    def create_export_settings(self, **params) -> Column:
        """Returns a UI component to configure the export settings.

        >>> button = walker.create_export_settings(width=400)
        """
        return create_export_settings(self, **params)

    def create_export_button(self, **params) -> ExportButton:
        """Returns a UI component to export the chart(s) as either a spec or SVG.

        >>> button = walker.create_export_button(width=400)

        The `value` parameter of the button will hold the exported chart(s) spec or SVG.
        """
        return ExportButton(self, **params)

    async def _save(
        self,
        path: str | PathLike | None = None,
        mode: Literal["spec", "svg", None] = None,
        scope: Literal["current", "all", None] = None,
        timeout: int | None = None,
    ) -> None:
        """
        Saves chart(s) from the frontend either
        as Vega specs or rendered to SVG.

        Arguments
        ---------
        path: str |
        mode: 'code' | 'svg' | None
           Whether to export and save the chart specification(s) or SVG. If None the mode is set
           to the 'export_code' parameter value.
        scope: 'current' | 'all'
           Whether to export and save only the current chart or all charts. If None the scope is
           set to the 'export_scope' parameter value.
        timeout: int
           How long to wait for the response before timing out. If None the timeout is
           set to the 'export_timeout' parameter value.
        """
        if not path:
            path = self.save_path
        spec = await self._export(mode=mode, scope=scope, timeout=timeout)
        path = Path(path)
        with path.open("w") as file:
            json.dump(spec, file)
        logger.debug("Saved spec to %s", path)

    def create_save_button(self, **params) -> SaveButton:
        """Returns a UI component to save the chart(s) as either a spec or SVG.

        >>> walker.create_save_button(width=400)

        The spec or SVG will be saved to the path give by `save_path`.
        """
        return SaveButton(self, **params)

    def chart(self, index: int | list | None = None, **params) -> "GraphicWalker":
        """Returns a clone with `renderer='chart'` and `server_computation=False`.

        >>> walker.chart(1, width=400)
        """
        params["index"] = index
        params["renderer"] = "chart"
        params["server_computation"] = False
        return self.clone(**params)

    def explorer(self, **params) -> "GraphicWalker":
        """Returns a clone with `renderer='explorer'`.

        >>> walker.explorer(width=400)
        """
        params["renderer"] = "explorer"
        return self.clone(**params)

    def profiler(self, **params) -> "GraphicWalker":
        """Returns a clone with `renderer='profiler'`.

        >>> walker.profiler(page_size=50, width=400)
        """
        params["renderer"] = "profiler"
        return self.clone(**params)

    def viewer(self, **params) -> "GraphicWalker":
        """Returns a clone with `renderer='viewer'`.

        >>> walker.viewer(width=400)
        """
        params["renderer"] = "viewer"
        return self.clone(**params)

    @param.depends("renderer")
    def page_size_enabled(self):
        """Returns True if the page_size parameter applies to the current renderer."""
        return self.renderer == "profiler"

    @param.depends("renderer")
    def index_enabled(self):
        """Returns True if the index parameter applies to the current renderer."""
        return self.renderer == "chart"

    @param.depends("renderer")
    def tab_enabled(self):
        """Returns True if the tab parameter applies to the current renderer."""
        return self.renderer == "explorer"

    @param.depends("renderer")
    def container_height_enabled(self):
        return self.renderer in ["viewer" or "chart"]
