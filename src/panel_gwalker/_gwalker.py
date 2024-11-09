import asyncio
import json
import os
import sys
import uuid
from functools import partial
from os import PathLike
from pathlib import Path
from typing import (
    IO,
    Any,
    Callable,
    Concatenate,
    Coroutine,
    Literal,
    Optional,
    ParamSpec,
)

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


def _extract_layout_params(params):
    layout_params = {}
    for key in ["sizing_mode", "width", "max_width"]:
        if key in params:
            layout_params[key] = params.pop(key)
    return layout_params


class ExportControls(Viewer):
    """A UI component to export the Chart(s) spec of SVG(s)"""

    mode: Literal["spec", "svg"] = param.Selector(
        default="spec",
        objects=["spec", "svg"],
        doc="Whether to export the chart as a specification or as SVG.",
    )

    scope: Literal["all", "current"] = param.Selector(
        default="all",
        objects=["all", "current"],
        doc="Whether to export the current chart or all charts.",
    )

    timeout: int = param.Integer(
        default=5000,
        doc="Export timeout in milliseconds.",
    )

    value: list | dict = param.ClassSelector(
        class_=(list, dict), doc="The exported Chart(s) spec or SVG."
    )

    run: bool = param.Event(doc="Click to export.", label="Export")

    def __init__(
        self,
        walker: "GraphicWalker",
        icon: str = "download",
        name: str | None = "Export",
        description: str = "Click to export",
        include_settings: bool = True,
        **params,
    ):
        layout_params = _extract_layout_params(params)
        super().__init__(**params)
        self._walker = walker
        if include_settings:
            settings = Column(
                RadioButtonGroup.from_param(
                    self.param.mode,
                    button_style="outline",
                    button_type="primary",
                    **layout_params,
                ),
                RadioButtonGroup.from_param(
                    self.param.scope,
                    button_style="outline",
                    button_type="primary",
                    **layout_params,
                ),
                IntInput.from_param(self.param.timeout, **layout_params),
            )
        # Should be changed to IconButton once https://github.com/holoviz/panel/issues/7458 is fixed.
        button = Button.from_param(
            self.param.run,
            icon=icon,
            description=description,
            **layout_params,
        )
        self._layout = Column(
            *settings,
            button,
        )

    @param.depends("run", watch=True)
    async def _export(self):
        self.param.run.constant = True
        try:
            self.value = await self._walker.export_chart(
                mode=self.mode, scope=self.scope, timeout=self.timeout
            )
        except TimeoutError as ex:
            self.value = {"TimeoutError": str(ex)}
        finally:
            self.param.run.constant = False

    def __panel__(self):
        return self._layout


class SaveControls(ExportControls):
    """
    A UI component to save the Chart(s) spec of SVG(s).

    Will save to `save_path` path of the `walker`.
    """

    save_path: str | PathLike = param.ClassSelector(
        label="Path",
        default="tmp_graphic_walker.json",
        class_=(str, PathLike, IO),
        doc="""Used as default path for the save method.""",
    )

    run: bool = param.Event(doc="Click to save.", label="Save")

    def __init__(
        self,
        walker: "GraphicWalker",
        *,
        icon: str = "download",
        name: str | None = "Save",
        description: str = "Click to save",
        include_settings: bool = True,
        **params,
    ):
        layout_params = _extract_layout_params(params)
        super().__init__(
            walker,
            icon=icon,
            name=name,
            description=description,
            include_settings=include_settings,
            **dict(params, **layout_params),
        )
        if include_settings:
            if isinstance(self.save_path, str):
                save_path = TextInput.from_param(self.param.save_path, **layout_params)
                self._layout.insert(3, save_path)

    @param.depends("run", watch=True)
    async def _export(self):
        self.param.run.constant = True
        try:
            await self._walker.save_chart(
                self.save_path, mode=self.mode, scope=self.scope, timeout=self.timeout
            )
        finally:
            self.param.run.constant = False


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
    kernel_computation: bool = param.Boolean(
        default=False,
        doc="""If True the computations will take place on the server or in the Jupyter kernel
        instead of the client to scale to larger datasets. Default is False. In Pyodide this will
        always be set to False. The 'chart' renderer will only work with client side rendering.""",
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
    hide_profiling: bool = param.Boolean(
        default=False,
        doc="""Whether to hide the profiling part of the 'profiler' renderer. Does not apply to other renderers.""",
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

    _importmap = {
        "imports": {
            "graphic-walker": f"https://esm.sh/@kanaries/graphic-walker@{VERSION}"
        }
    }

    _esm = "_gwalker.js"

    _THEME_CONFIG = {
        "default": "light",
        "dark": "dark",
    }

    def __init__(self, object=None, **params):
        if "appearance" not in params:
            params["appearance"] = self._get_appearance(config.theme)

        if params.pop("_debug", False):
            configure_debug_log_level()

        if state._is_pyodide:
            params.pop("kernel_computation", None)

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
            if self.kernel_computation:
                del params["object"]
        if "spec" in params:
            params["spec"] = process_spec(params["spec"])
        if params.get("kernel_computation") is False and "object" not in params:
            params["object"] = self.object
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
            result = pd.DataFrame()

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

    async def export_chart(
        self,
        mode: Literal["spec", "svg"] = "spec",
        scope: Literal["current", "all"] = "current",
        timeout: int = 5000,
    ):
        """
        Requests chart(s) on the frontend to be exported either
        as Vega specs or rendered to SVG.

        Arguments
        ---------
        mode: 'code' | 'svg'
            Whether to export the chart specification(s) or the SVG(s).
        scope: 'current' | 'all'
            Whether to export only the current chart or all charts.
        timeout: int | None (default)
            How long to wait for the response before timing out (in milliseconds).

        Returns
        -------
        Dictionary containing the exported chart(s).
        """
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

    async def save_chart(
        self,
        path: str | PathLike | IO,
        mode: Literal["spec", "svg"] = "spec",
        scope: Literal["current", "all"] = "current",
        timeout: int = 5000,
    ) -> None:
        """
        Saves chart(s) from the frontend either as Vega specs or rendered to SVG.

        Arguments
        ---------
        path: str | PathLike | IO
        mode: 'code' | 'svg'
           Whether to export and save the chart specification(s) or SVG. If None the mode is set
           to the 'export_code' parameter value.
        scope: 'current' | 'all'
           Whether to export and save only the current chart or all charts. If None the scope is
           set to the 'export_scope' parameter value.
        timeout: int
           How long to wait for the response before timing out. If None the timeout is
           set to the 'export_timeout' parameter value.
        """
        spec = await self.export_chart(mode=mode, scope=scope, timeout=timeout)
        if isinstance(path, IO):
            json.dump(spec, path)
        else:
            path = Path(path)
            with path.open("w") as file:
                json.dump(spec, file)
        logger.debug("Saved spec to %s", path)

    def export_controls(self, **params) -> SaveControls:
        """Returns a UI component to save the chart(s) as either a spec or SVG.

        >>> walker.export_controls(width=400)
        """
        return ExportControls(self, **params)

    def save_controls(
        self, save_path: str | os.PathLike | IO, **params
    ) -> SaveControls:
        """Returns a UI component to save the chart(s) as either a spec or SVG.

        >>> walker.create_save_button(width=400)

        The spec or SVG will be saved to the path give by `save_path`.
        """
        return SaveControls(self, save_path=save_path, **params)

    def chart(self, index: int | list | None = None, **params) -> "GraphicWalker":
        """Returns a clone with `renderer='chart'` and `kernel_computation=False`.

        >>> walker.chart(1, width=400)
        """
        params["index"] = index
        params["renderer"] = "chart"
        params["kernel_computation"] = False
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

    _PARAMETER_IS_ENABLED = {
        "page_size": ["profiler"],
        "hide_profiling": ["profiler"],
        "index": ["viewer", "chart"],
        "tab": ["explorer"],
        "container_height": ["viewer", "chart"],
    }

    @classmethod
    def _is_enabled(cls, renderer, parameter) -> bool:
        """Returns True if the parameter is enabled for the renderer."""
        if not parameter in cls._PARAMETER_IS_ENABLED:
            return True

        return renderer in cls._PARAMETER_IS_ENABLED[parameter]

    @classmethod
    def _is_disabled(cls, renderer, parameter) -> bool:
        """Returns True if the parameter is disabled for the renderer."""
        return not cls._is_enabled(renderer, parameter)

    def is_enabled(self, parameter: str):
        """Returns a bound function. The function will evaluate to True if the parameter is
        enabled for the current renderer."""
        return param.bind(self._is_enabled, self.param.renderer, parameter)

    def is_disabled(self, parameter: str):
        """Returns a bound function. The function will return True if the parameter is disabled
        for the current renderer."""
        return param.bind(self._is_disabled, self.param.renderer, parameter)
