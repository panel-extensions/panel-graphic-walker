import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Protocol

import pandas as pd
from narwhals.dependencies import is_dask_dataframe, is_ibis_table
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

if TYPE_CHECKING:
    try:
        from pygwalker.data_parsers.base import BaseDataParser
    except ImportError:
        BaseDataParser = None


def get_sql_from_payload(
    table_name: str,
    payload: Dict[str, Any],
    field_meta: List[Dict[str, str]] | None = None,
) -> str:
    try:
        from gw_dsl_parser import get_sql_from_payload as _get_sql_from_payload
    except ImportError as exc:
        raise ImportError(
            "gw-dsl-parser is not installed, please pip install it first."
        ) from exc

    sql = _get_sql_from_payload(table_name, payload, field_meta)
    return sql


def _convert_to_field_spec(spec: dict) -> dict:
    return {
        "fname": spec["fid"],
        "semantic_type": spec["semanticType"],
        "analytic_type": spec["analyticType"],
        "display_as": spec["name"],
    }


def get_dask_dataframe_parser():
    from dask.dataframe import DataFrame
    from pygwalker.data_parsers.base import FieldSpec
    from pygwalker.data_parsers.pandas_parser import PandasDataFrameDataParser

    class DaskDataFrameParser(PandasDataFrameDataParser):
        def __init__(
            self,
            df: DataFrame,
            field_specs: List[FieldSpec],
            infer_string_to_date: bool,
            infer_number_to_dimension: bool,
            other_params: Dict[str, Any],
        ):
            self.origin_df = df
            self.df = self._rename_dataframe(df)
            self._example_df = self.df.head(1000)  # This is a change
            self.field_specs = field_specs
            self._duckdb_df = self.df
            self.infer_string_to_date = infer_string_to_date
            self.infer_number_to_dimension = infer_number_to_dimension
            self.other_params = other_params

        @property
        def dataset_type(self) -> str:
            return "dask_dataframe"

    return DaskDataFrameParser


def get_ibis_dataframe_parser():
    from pygwalker.data_parsers.pandas_parser import PandasDataFrameDataParser
    from pygwalker.services.fname_encodings import rename_columns

    class IbisDataFrameParser(PandasDataFrameDataParser):
        def _rename_dataframe(self, df):
            df = df.rename(
                {
                    old_col: new_col
                    for old_col, new_col in zip(df.columns, rename_columns(df.columns))
                }
            )
            return df

    @property
    def dataset_type(self) -> str:
        return "ibis_dataframe"

    return IbisDataFrameParser


def get_data_parser(
    object,
    field_specs: List[dict],  # FieldSpec
    infer_string_to_date: bool,
    infer_number_to_dimension: bool,
    other_params: Dict[str, Any],
) -> "BaseDataParser":
    try:
        from pygwalker import data_parsers
        from pygwalker.data_parsers.base import FieldSpec
        from pygwalker.services.data_parsers import __classname2method, _get_data_parser
    except ImportError as exc:
        raise ImportError(
            "Server dependencies are not installed. Please: pip install panel-graphic-walker[kernel]."
        ) from exc

    _field_specs = [FieldSpec(**_convert_to_field_spec(spec)) for spec in field_specs]
    try:
        parser, name = _get_data_parser(object)
    except TypeError as exc:
        object_type = type(object)
        if is_dask_dataframe(object):
            DaskDataFrameParser = get_dask_dataframe_parser()
            __classname2method[object_type] = (DaskDataFrameParser, "dask")
        if is_ibis_table(object):
            IbisDataFrameParser = get_ibis_dataframe_parser()
            __classname2method[object_type] = (IbisDataFrameParser, "ibis")

        try:
            parser, name = __classname2method[object_type]
        except KeyError as exc:
            msg = f"Data type {type(object)} is currently not supported"
            raise NotImplementedError(msg) from exc

    return parser(
        object,
        _field_specs,
        infer_string_to_date,
        infer_number_to_dimension,
        other_params,
    )
