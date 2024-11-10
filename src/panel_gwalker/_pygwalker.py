import sys
from typing import TYPE_CHECKING, Any, Dict, List, Protocol, runtime_checkable

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


@runtime_checkable
class ConnectorP(Protocol):
    def query_datas(self, sql: str) -> List[Dict[str, Any]]: ...

    @property
    def dialect_name(self) -> str: ...


def _get_data_parser_non_pygwalker(
    object, fields_specs, infer_string_to_date, infer_number_to_dimension, other_params
):
    if isinstance(dataset, ConnectorP):
        from pygwalker.data_parsers.database_parser import DatabaseDataParser

        __classname2method[DatabaseDataParser] = (DatabaseDataParser, "connector")
        return __classname2method[DatabaseDataParser]

    return object, parser, name


class DuckDBPyRelationConnector(ConnectorP):
    def __init__(self, relation):
        self.relation = relation
        self.view_sql = "SELECT * FROM __relation"

    def query_datas(self, sql: str) -> List[Dict[str, Any]]:
        __relation = self.relation

        result = self.relation.query("__relation", sql).fetchall()
        columns = self.relation.query("__relation", sql).columns
        records = [dict(zip(columns, row)) for row in result]
        return records

    @property
    def dialect_name(self) -> str:
        return "duckdb"


def get_data_parser(
    object,
    field_specs: List[dict],  # FieldSpec
    infer_string_to_date: bool,
    infer_number_to_dimension: bool,
    other_params: Dict[str, Any],
) -> "BaseDataParser":
    try:
        from pygwalker.data_parsers.base import FieldSpec
        from pygwalker.data_parsers.database_parser import DatabaseDataParser
        from pygwalker.services.data_parsers import (
            __classname2method,
        )
        from pygwalker.services.data_parsers import (
            _get_data_parser as _get_data_parser_pygwalker,
        )
    except ImportError as exc:
        raise ImportError(
            "Server dependencies are not installed. Please: pip install panel-graphic-walker[kernel]."
        ) from exc

    custom_connector = None
    if "duckdb" in sys.modules:
        from duckdb.duckdb import DuckDBPyRelation

        if isinstance(object, DuckDBPyRelation):
            custom_connector = DuckDBPyRelationConnector(object)

    if custom_connector:
        object = custom_connector
        __classname2method[DatabaseDataParser] = (DatabaseDataParser, "connector")
        parser, name = __classname2method[DatabaseDataParser]
    else:
        try:
            parser, name = _get_data_parser_pygwalker(object)
        except TypeError as exc:
            msg = f"Data type {type(object)} is currently not supported"
            raise NotImplementedError(msg) from exc

    _field_specs = [FieldSpec(**_convert_to_field_spec(spec)) for spec in field_specs]
    return parser(
        object,
        _field_specs,
        infer_string_to_date,
        infer_number_to_dimension,
        other_params,
    )
