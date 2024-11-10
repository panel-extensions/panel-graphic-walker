from typing import Any, Dict, List

import duckdb
import pandas as pd
import pytest


class Connector:
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


@pytest.fixture(params=["in-memory", "persistent"])
def con(request, tmp_path):
    if request.param == "in-memory":
        database = ":memory:"
    else:
        database = (tmp_path / "tmp.db").as_posix()
    con = duckdb.connect(database)
    con.execute("CREATE TABLE df_pandas (a INTEGER)")
    con.execute("INSERT INTO df_pandas VALUES (1), (2), (3)")
    return con


@pytest.fixture
def data(con):
    return con.sql("SELECT * FROM df_pandas")


def test_connector_simple_works():
    df_pandas = pd.DataFrame({"a": [1, 2, 3]})
    data = duckdb.sql("SELECT * FROM df_pandas")
    connector = Connector(data)
    assert connector.dialect_name == "duckdb"
    assert connector.query_datas("SELECT * FROM __relation") == [
        {"a": 1},
        {"a": 2},
        {"a": 3},
    ]


def test_connector_advanced_which_does_not_work(data):
    connector = Connector(data)
    assert connector.dialect_name == "duckdb"
    assert connector.query_datas("SELECT * FROM __relation") == [
        {"a": 1},
        {"a": 2},
        {"a": 3},
    ]
