import dask.dataframe as dd
import duckdb
import pytest

from panel_gwalker._gwalker import get_data_parser


def test_get_data_parser(data):
    if isinstance(data, (dd.DataFrame, duckdb.duckdb.DuckDBPyRelation)):
        pytest.xfail(f"Unsupported data type: {type(data)}")

    assert get_data_parser(data, [], False, False, {})
