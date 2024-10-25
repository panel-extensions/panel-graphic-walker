from typing import Dict

import numpy as np
import param
import pandas as pd

from panel.custom import ReactComponent
from panel.pane.base import PaneBase
from panel.reactive import SyncableData


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
    semanticType = 'quantitative' if \
        (kind in 'fcmiu' and v_cnt > 16) \
            else 'temporal' if kind in 'M' \
                else 'nominal' if kind in 'bOSUV' or v_cnt <= 2 \
                    else 'ordinal'
    # 'quantitative' | 'nominal' | 'ordinal' | 'temporal';
    analyticType = 'measure' if \
        kind in 'fcm' or (kind in 'iu' and len(s.value_counts()) > 16) \
            else 'dimension'
    return {
        'fid': s.name,
        'name': s.name,
        'semanticType': semanticType,
        'analyticType': analyticType
    }

def raw_fields(data: pd.DataFrame | Dict[str, np.ndarray]):
    if isinstance(data, dict):
        return [
            infer_prop(pd.Series(array, name=col)) for col, array in data.items()
        ]
    else:
        return [
            infer_prop(data[col], i)
            for i, col in enumerate(data.columns)
        ]


class GraphicWalker(ReactComponent):

    config = param.Dict()

    object = param.DataFrame()

    _importmap = {
        "imports": {
            "graphic-walker": "https://esm.sh/@kanaries/graphic-walker@0.4.72"
        }
    }

    _esm = """
    import {GraphicWalker} from "graphic-walker"
    import {useEffect, useState} from "react"

    function transform(data) {
      const keys = Object.keys(data);
      const length = data[keys[0]].length;

      return Array.from({ length }, (_, i) =>
        keys.reduce((obj, key) => {
          obj[key] = data[key][i];
          return obj;
        }, {})
      );
    }

    export function render({ model }) {
      const [config] = model.useState('config')
      const [data] = model.useState('object')
      const [transformedData, setTransformedData] = useState([]);

      useEffect(() => {
        const result = transform(data);
        setTransformedData(result);
      }, [data]);

      return <GraphicWalker data={transformedData} {...config}/>
    }"""

    def __init__(self, object=None, **params):
        super().__init__(object=object, **params)

    @classmethod
    def applies(cls, object):
        if isinstance(object, dict) and all(isinstance(v, (list, np.ndarray)) for v in object.values()):
            return 0 if object else None
        elif 'pandas' in sys.modules:
            import pandas as pd
            if isinstance(object, pd.DataFrame):
                return 0
        return False

    def _process_param_change(self, params):
        if self.object is not None and 'object' in params and not self.config:
            params['config'] = {'rawFields': raw_fields(self.object)}
        return params
