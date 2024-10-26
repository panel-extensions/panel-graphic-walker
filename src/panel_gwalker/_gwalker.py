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
    # This one is added to better explain that currently only 'client' mode is supported
    # but we envision supporting 'server' mode one day
    computation: Literal["client"] = param.Selector(
        objects=["client"],
        doc="""The computation configuration. Currently only 'client' is supported.""",
    )
    config: dict = param.Dict(
        doc="""Optional extra Graphic Walker configuration. For example `{"i18nLang": "ja-JP"}`. See the
    [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details."""
    )

    current_chart = param.Dict()
    save_current_chart = param.Event(label="Save", doc="Save the current chart.")

    current_chart_list = param.List()
    save_current_chart_list = param.Event(label="Save", doc="Save the current charts.")

    _importmap = {
        "imports": {
            "graphic-walker": f"https://esm.sh/@kanaries/graphic-walker@{VERSION}"
        }
    }

    _esm = "_gwalker.js"

    def __init__(self, object=None, **params):
        if not "appearance" in params:
            params["appearance"]=self._get_appearance(config.theme)
        super().__init__(object=object, **params)

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

    def _process_param_change(self, params):
        if self.object is not None and "object" in params:
            if not self.fields:
                params["fields"] = raw_fields(self.object)
            if not self.config:
                params["config"] = {}
        return params
