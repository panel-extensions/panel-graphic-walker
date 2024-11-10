import json
import sys
import weakref
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Protocol, runtime_checkable

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


_DUCKDB_CONNECTIONS = weakref.WeakKeyDictionary()  # type: ignore[var-annotated]
_DEFAULT_DUCKDB_CONNECTION = None


def experimental_duckdb_registration(connection, relation=None):
    """Register the duckdb connection to be used by the GraphicWalker

    Will be deprecated the day we now how to solve https://github.com/duckdb/duckdb/discussions/14768
    or https://github.com/duckdb/duckdb/discussions/14772.

    Args:
        connection: The duckdb connection to be registered
        relation (duckdb.duckdb.DuckDBPyRelation): Optional relation to be registered. If None, the connection
        will be used as the default connection.
    ."""
    if relation is None:
        global _DEFAULT_DUCKDB_CONNECTION
        _DEFAULT_DUCKDB_CONNECTION = connection
    else:
        _DUCKDB_CONNECTIONS[relation] = connection


class DuckDBPyRelationConnector(ConnectorP):
    def __init__(self, relation):
        self.relation = relation
        # Might not work if duckdb is not in memory
        if relation in _DUCKDB_CONNECTIONS:
            self._connection = _DUCKDB_CONNECTIONS[relation]
        elif _DEFAULT_DUCKDB_CONNECTION:
            self._connection = _DEFAULT_DUCKDB_CONNECTION
        else:
            import duckdb

            self._connection = duckdb

        self._connection.register("__relation", self.relation)
        # Might not work if using multiple relations?
        self.view_sql = "SELECT * FROM __relation"

    def query_datas(self, sql: str) -> List[Dict[str, Any]]:
        connection = self._connection

        result = connection.sql(sql).fetchall()
        columns = connection.sql(sql).columns
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
