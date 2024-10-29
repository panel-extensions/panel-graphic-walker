import asyncio
import uuid
from typing import Any, Dict, List, Literal

import numpy as np
import pandas as pd
import param
from panel import config
from panel.custom import ReactComponent
from panel.io.state import state
from panel.pane.base import PaneBase
from panel.reactive import SyncableData
from param.parameterized import Event

from panel_gwalker._pygwalker import get_data_parser, get_sql_from_payload
from panel_gwalker._utils import (_infer_prop, _raw_fields,
                                  configure_debug_log_level, logger)

VERSION = "0.4.72"


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
    server_computation: bool = param.Boolean(
        default=False,
        doc="""If True the computations will take place on the Panel server or in the Jupyter kernel
        instead of the client to scale to larger datasets. Default is False. In Pyodide this will
        always be set to False.""",
        constant=state._is_pyodide,
    )
    config: dict = param.Dict(
        doc="""Optional extra Graphic Walker configuration. For example `{"i18nLang": "ja-JP"}`. See the
    [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details."""
    )

    appearance: Literal["media", "dark", "light"] = param.Selector(
        default="light",
        objects=["light", "dark", "media"],
        doc="""Dark mode preference: 'light', 'dark' or 'media'.
        If not provided the appearance is derived from pn.config.theme.""",
    )
    theme: Literal["vega", "g2", "streamlit"]=param.Selector(
        default="vega",
        objects=["vega", "g2", "streamlit"],
        doc="""The theme of the chart(s). One of 'vega' (default), 'g2' or 'streamlit'.""",
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
        if not "appearance" in params:
            params["appearance"] = self._get_appearance(config.theme)
        if "_debug" in params:
            _debug=params.pop("_debug")
            if _debug:
                configure_debug_log_level()
        if state._is_pyodide and "server_computation" in params:
            params.pop("server_computation")

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
    def calculated_fields(self)->dict:
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
        return super()._process_param_change(params)

    def _compute(self, payload):
        logger.debug("request: %s", payload)
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
            sql = get_sql_from_payload(
                "pygwalker_mid_table",
                payload,
                {"pygwalker_mid_table": parser.field_metas}
            ) # type: ignore
            logger.exception("SQL raised exception:\n%s\n\npayload:%s", sql, payload)

        df = pd.DataFrame.from_records(result)
        logger.debug("response:\n%s", df)
        return {col: df[col].values for col in df.columns}

    def _handle_msg(self, msg: Any) -> None:
        action = msg['action']
        event_id = msg.pop('id')
        if action == 'export' and event_id in self._exports:
            self._exports[event_id] = msg['data']
        elif action == 'compute':
            self._send_msg({
                'action': 'compute',
                'id': event_id,
                'result': self._compute(msg['payload'])
            })

    async def export(
        self,
        mode: Literal['spec', 'svg'] = 'spec',
        scope: Literal['current', 'all'] = 'current',
        timeout: int = 5000
    ):
        """
        Requests chart(s) on the frontend to be exported either
        as Vega specs or rendered to SVG.

        Arguments
        ---------
        mode: 'code' | 'svg'
           Whether to export the chart specification or SVG.
        scope: 'current' | 'all'
           Whether to export only the current chart or all charts.
        timeout: int
           How long to wait for the response before timing out.

        Returns
        -------
        Dictionary containing the exported chart(s).
        """
        event_id = uuid.uuid4().hex
        self._send_msg({
            'action': 'export',
            'id': event_id,
            'scope': f'{scope}',
            'mode': mode
        })
        wait_count = 0
        self._exports[event_id] = None
        while self._exports[event_id] is not None:
            await asyncio.sleep(0.1)
            wait_count += 1
            if (wait_count * 100) > timeout:
                del self._exports[event_id]
                raise TimeoutError(
                    f'Exporting {scope} chart(s) timed out.'
                )
        return self._exports.pop(event_id)
