import json
import logging
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import panel as pn

logger = logging.getLogger("panel-graphic-walker")
FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def configure_debug_log_level():
    format_=FORMAT
    level=logging.DEBUG
    logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setStream(sys.stdout)
    formatter = logging.Formatter(format_)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    logger.setLevel(level)
    logger.info("Logger successfully configured")
    return logger

def _infer_prop(s: pd.Series, i=None)->dict:
    """

    Arguments
    ---------
    s (pd.Series):
      the column
    """
    kind = s.dtype.kind
    logger.debug("%s: type=%s, kind=%s", s.name, s.dtype, s.dtype.kind)
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

@pn.cache(max_items=20, ttl=60*5, policy='LRU')
def _raw_fields(data: pd.DataFrame | Dict[str, np.ndarray])->list[dict]:
    if isinstance(data, dict):
        return [_infer_prop(pd.Series(array, name=col)) for col, array in data.items()]
    else:
        return [_infer_prop(data[col], i) for i, col in enumerate(data.columns)]

SpecType = None | str | Path | dict | list[dict]
SPECTYPES = (type(None), str, Path, dict, list)

@lru_cache(maxsize=10)
def _read_and_load_json(spec):
    with open(spec, 'r') as f:
        return json.load(f)

@lru_cache(maxsize=10)
def _load_json(spec):
    return json.loads(spec)

def _is_url(spec):
    return spec.startswith(("http", "https"))

def process_spec(spec: SpecType):
    if (isinstance(spec, str) and os.path.isfile(spec) and spec.endswith(".json")) or isinstance(spec, Path):
        return _read_and_load_json(spec)

    if isinstance(spec, str) and not _is_url(spec):
        return _load_json(spec)

    return spec
