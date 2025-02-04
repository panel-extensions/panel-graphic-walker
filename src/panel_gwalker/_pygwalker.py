from typing import TYPE_CHECKING, Any, Dict, List, Protocol, runtime_checkable

from narwhals.dependencies import is_duckdb_relation, is_ibis_table

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
        import pygwalker
    except ImportError as exc:
        raise ImportError(
            "Enabling panel-graphic-walker kernel computation requires server dependencies. "
            "Please pip install 'panel-graphic-walker[kernel]'"
        ) from exc
    if Version(pygwalker.__version__) >= Version('0.4.9'):
        raise ImportError(
            "Enabling panel-graphic-walker kernel computation requires pygwalker versions greater than 0.4.9."
        ) from exc
    from pygwalker.data_parsers.base import FieldSpec
    from pygwalker.data_parsers.database_parser import DatabaseDataParser
    from pygwalker.services.data_parsers import (
        __classname2method,
    )
    from pygwalker.services.data_parsers import (
        _get_data_parser as _get_data_parser_pygwalker,
    )
    object_type = type(object)

    if is_ibis_table(object):
        IbisDataFrameParser = get_ibis_dataframe_parser()
        __classname2method[object_type] = (IbisDataFrameParser, "ibis")

    if is_duckdb_relation(object):
        object = DuckDBPyRelationConnector(object)
        object_type = type(object)
        __classname2method[object_type] = (DatabaseDataParser, "duckdb")

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
