from typing import Any, Dict, List, Literal

import numpy as np
import pandas as pd
import param
from panel import config
from panel.custom import ReactComponent
from panel.pane.base import PaneBase
from panel.reactive import SyncableData
from param.parameterized import Event

from panel_gwalker._pygwalker import get_data_parser, get_sql_from_payload
from panel_gwalker._utils import (IS_RUNNING_IN_PYODIDE, _infer_prop,
                                  _raw_fields, configure_debug_log_level,
                                  logger)

VERSION = "0.4.72"

class GraphicWalker(ReactComponent):
    """
    The `GraphicWalker` component enables interactive exploration of data in a DataFrame
    using an interface built on [Graphic Walker](https://docs.kanaries.net/graphic-walker).

    Reference: https://github.com/philippjfr/panel-graphic-walker.

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
    appearance: Literal["media", "dark", "light"] = param.Selector(
        default="light",
        objects=["light", "dark", "media"],
        doc="""Dark mode preference: 'light', 'dark', 'media'.
        If not provided the appearance is derived from pn.config.theme.""",
    )
    server_computation: bool = param.Boolean(
        default=False,
        doc="""If True the computations will take place on the Panel server or in the Jupyter kernel
        instead of the client to scale to larger datasets. Default is False. In Pyodide this will
        always be set to False.""",
        constant=IS_RUNNING_IN_PYODIDE,
    )
    config: dict = param.Dict(
        doc="""Optional extra Graphic Walker configuration. For example `{"i18nLang": "ja-JP"}`. See the
    [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details."""
    )

    chart: dict = param.Dict(doc="""The current chart.""")
    export_chart: bool = param.Event(doc="""Updates the current chart.""")
    chart_list: list = param.List(doc="""The current chart list.""")
    export_chart_list: bool = param.Event(doc="""Updates the current chart list.""")

    _payload_request: dict = param.Dict(doc="The payload request from the server.")
    _payload_response: list = param.List(doc="The payload response to the server.")


    _importmap = {
        "imports": {
            "graphic-walker": f"https://esm.sh/@kanaries/graphic-walker@{VERSION}"
        }
    }

    _esm = "_gwalker.js"

    def __init__(self, object=None, **params):
        if not "appearance" in params:
            params["appearance"] = self._get_appearance(config.theme)
        if "_log_level_debug" in params:
            _log_level_debug=params.pop("_log_level_debug")
            if _log_level_debug:
                configure_debug_log_level()
        if IS_RUNNING_IN_PYODIDE and "server_computation" in params:
            params.pop("server_computation")

        super().__init__(object=object, **params)
        self.param.watch(self._on_payload_request_change, "_payload_request")

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

    _THEME_CONFIG = {
        "default": "light",
        "dark": "dark",
    }

    def _get_appearance(self, theme):
        config = self._THEME_CONFIG
        return config.get(theme, self.param.appearance.default)

    # Todo: When `server_computation=True` we should not waste resources on transferring the data object.
    # The `fields` should still be transferred though.
    def _process_param_change(self, params):
        if self.object is not None and "object" in params:
            if not self.fields:
                params["fields"] = _raw_fields(self.object)
            if not self.config:
                params["config"] = {}
        return params

    # Todo: Test if this performs?
    # - Compute
    # - Memory
    # - Multiple walkers in an app
    # - Multiple sessions and users
    # Todo: Figure out if duckdb config should be exposed. Currently I believe its memory
    # Would probably scale even better if disk based. But then slower.
    def _on_payload_request_change(self, event: param.parameterized.Event):
        payload = event.new
        if not payload:
            # This will happen when we set payload={} after the response has been received
            return

        logger.debug("requested %s", payload)

        field_specs = _raw_fields(self.object)
        parser = get_data_parser(
            self.object,
            field_specs=field_specs,
            infer_string_to_date=False,
            infer_number_to_dimension=False,
            other_params={},
        )
        try:
            result = parser.get_datas_by_payload(payload)
        except Exception as ex:
            # Todo: Figure out why there is type issue and how to solve
            sql = get_sql_from_payload("pygwalker_mid_table", payload, {"pygwalker_mid_table": parser.field_metas}) # type: ignore
            logger.exception("SQL raised exception:\n%s\n\npayload:%s", sql, payload)

        # Todo: Figure out how to transfer this efficiently (as a dataframe?)
        self._payload_response = result
        logger.debug("responded %s", result)
