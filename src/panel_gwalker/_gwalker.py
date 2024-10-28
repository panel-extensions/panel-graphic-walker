import asyncio
import uuid
from typing import Dict, Literal

import numpy as np
import pandas as pd
import param
from panel import config
from panel.custom import ReactComponent
from panel.pane.base import PaneBase
from panel.reactive import SyncableData

VERSION = "0.4.72"

def infer_prop(s: np.ndarray, i=None):
    """

    Arguments
    ---------
    s (pd.Series):
      the column
    """
    kind = s.dtype.kind
    # print(f'{s.name}: type={s.dtype}, kind={s.dtype.kind}')
    v_cnt = len(s.value_counts())
    semanticType = (
        "quantitative"
        if (kind in "fcmiu" and v_cnt > 16)
        else (
            "temporal"
            if kind in "M"
            else "nominal" if kind in "bOSUV" or v_cnt <= 2 else "ordinal"
        )
    )
    # 'quantitative' | 'nominal' | 'ordinal' | 'temporal';
    analyticType = (
        "measure"
        if kind in "fcm" or (kind in "iu" and len(s.value_counts()) > 16)
        else "dimension"
    )
    return {
        "fid": s.name,
        "name": s.name,
        "semanticType": semanticType,
        "analyticType": analyticType,
    }


def raw_fields(data: pd.DataFrame | Dict[str, np.ndarray]):
    if isinstance(data, dict):
        return [infer_prop(pd.Series(array, name=col)) for col, array in data.items()]
    else:
        return [infer_prop(data[col], i) for i, col in enumerate(data.columns)]


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
        instead of the client to scale to larger datasets. Default is False.""",
    )
    config: dict = param.Dict(
        doc="""Optional extra Graphic Walker configuration. For example `{"i18nLang": "ja-JP"}`. See the
    [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details."""
    )

    chart: dict = param.Dict(doc="""The current chart.""")

    chart_list: list = param.List(doc="""The current chart list.""")
    export_chart_list: bool = param.Event(doc="""Updates the current chart list.""")

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

    def _process_param_change(self, params):
        if self.object is not None and "object" in params:
            if not self.fields:
                params["fields"] = raw_fields(self.object)
            if not self.config:
                params["config"] = {}
        return params

    def _handle_msg(self, msg: any) -> None:
        event_id = msg.pop('id')
        if event_id in self._exports:
            self._exports[event_id] = msg['data']

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
        self._send_msg({'id': event_id, 'scope': f'{scope}', 'mode': mode})
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
