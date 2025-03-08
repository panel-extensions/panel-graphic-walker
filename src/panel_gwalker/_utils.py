import decimal
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Union

import narwhals as nw
import pandas as pd
import panel as pn
import requests
from narwhals.dataframe import LazyFrame
from narwhals.typing import FrameT


def convert_decimals_to_float(df: pd.DataFrame, sample: int = 100) -> pd.DataFrame:
    """
    Convert decimal.Decimal to float in a pandas DataFrame, as
    Bokeh ColumnDataSource does not support decimal.Decimal.
    Samples only a subset of the DataFrame to check for decimal.Decimal

    Arguments
    ---------
    df (pd.DataFrame):
      the DataFrame to convert
    sample (int):
      number of rows to sample to check for decimal.Decimal
    """
    df = df.copy()
    for col in df.select_dtypes(include=["object"]).columns:
        try:
            if (
                df[col]
                .sample(min(sample, len(df)))
                .apply(lambda x: isinstance(x, decimal.Decimal))
                .any()
            ):
                df[col] = pd.to_numeric(df[col], errors="coerce")
        except Exception:
            df[col] = df[col].astype(str)
    return df


logger = logging.getLogger("panel-graphic-walker")
FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
from narwhals.typing import FrameT


def configure_debug_log_level():
    format_ = FORMAT
    level = logging.DEBUG
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


def _infer_prop(s: pd.Series, i=None) -> dict:
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
            else "nominal"
            if kind in "bOSUV" or v_cnt <= 2
            else "ordinal"
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


SAMPLE_ROWS = 100


@pn.cache(max_items=20, ttl=60 * 5, policy="LRU")
def _raw_fields_core(data: pd.DataFrame) -> list[dict]:
    return [_infer_prop(data[col], i) for i, col in enumerate(data.columns)]


@nw.narwhalify
def _raw_fields(data: FrameT) -> list[dict]:
    # Workaround for caching issue. See https://github.com/holoviz/panel/issues/7467.
    # Should probably use Narwhals schema to one day infer this
    if isinstance(data, LazyFrame):
        data = data.head(100).collect()
    else:
        try:
            if len(data) > SAMPLE_ROWS:
                data = data.sample(SAMPLE_ROWS)
        except Exception as ex:
            pass

    pandas_data = convert_decimals_to_float(data.to_pandas())
    return _raw_fields_core(pandas_data)


SpecType = None | str | Path | dict | list[dict]
SPECTYPES = (type(None), str, Path, dict, list)


# We should figure out how to disable when developing with hot reload
# https://github.com/holoviz/panel/issues/7459
# @lru_cache(maxsize=10)
def _read_and_load_json(spec):
    with open(spec, "r") as f:
        return json.load(f)


# @lru_cache(maxsize=10)
def _load_json(spec):
    return json.loads(spec)


def _is_url(spec):
    return isinstance(spec, str) and spec.startswith(("http", "https"))


@pn.cache(max_items=25, policy="LRU", ttl=60 * 5)
def _get_spec(url) -> dict:
    # currently client side loading of url does not work
    return requests.get(url).json()


def process_spec(spec: SpecType):
    if not spec:
        return spec

    if (
        isinstance(spec, str) and os.path.isfile(spec) and spec.endswith(".json")
    ) or isinstance(spec, Path):
        return _read_and_load_json(spec)

    if _is_url(spec):
        return _get_spec(spec)

    if isinstance(spec, str):
        return _load_json(spec)

    return spec
