import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Protocol

import pandas as pd
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
        from pygwalker.services.data_parsers import _get_data_parser
    except ImportError as exc:
        raise ImportError(
            "Server dependencies are not installed. Please: pip install panel-graphic-walker[kernel]."
        ) from exc

    _field_specs = [FieldSpec(**_convert_to_field_spec(spec)) for spec in field_specs]
    try:
        parser, name = _get_data_parser(object)
        return parser(
            object,
            _field_specs,
            infer_string_to_date,
            infer_number_to_dimension,
            other_params,
        )
    except TypeError as exc:
        msg = f"Data type {type(object)} is currently not supported"
        raise NotImplementedError(msg) from exc
