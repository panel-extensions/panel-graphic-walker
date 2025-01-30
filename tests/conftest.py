import dask.dataframe as dd
import duckdb
import ibis
import pandas as pd
import polars as pl
import pytest

# Using duckdb relation as fixtures requires special care
# See https://github.com/duckdb/duckdb/issues/14771


@pytest.fixture(scope="session")
def memory_conn():
    con = duckdb.connect()
    con.execute("CREATE TABLE df_pandas (a INTEGER)")
    con.execute("INSERT INTO df_pandas VALUES (1), (2), (3)")
    return con


@pytest.fixture()
def persistent_conn(tmp_path):
    database = (tmp_path / "tmp.db").as_posix()
    con = duckdb.connect(database)
    con.execute("CREATE TABLE df_pandas (a INTEGER)")
    con.execute("INSERT INTO df_pandas VALUES (1), (2), (3)")
    return con


@pytest.fixture(
    params=[
        "pandas",
        "polars",
        "dask",
        "ibis-sqlite",
        "duckdb-simple",
        "duckdb-in-memory",
        "duckdb-persistent",
    ]
)
def data(request, tmp_path, memory_conn, persistent_conn):
    if request.param == "pandas":
        return pd.DataFrame({"a": [1, 2, 3]})
    if request.param == "polars":
        return pl.DataFrame({"a": [1, 2, 3]})
    if request.param == "dask":
        return dd.from_pandas(pd.DataFrame({"a": [1, 2, 3]}), npartitions=1)
    if request.param == "ibis-duckdb-persistent":
        path = (tmp_path / "tmp.ibis.db").as_posix()
        con = ibis.duckdb.connect(path)
        table = con.create_table("my_table", schema=ibis.schema(dict(a="int64")))
        con.insert("my_table", obj=[(1,), (2,), (3,)])
        return table
    if request.param == "ibis-sqlite":
        path = (tmp_path / "tmp.ibis.db").as_posix()
        con = ibis.sqlite.connect(path)
        table = con.create_table("my_table", schema=ibis.schema(dict(a="int64")))
        con.insert("my_table", obj=[(1,), (2,), (3,)])
        return table
    if request.param == "duckdb-simple":
        df_pandas = pd.DataFrame({"a": [1, 2, 3]})
        return duckdb.sql("SELECT * FROM df_pandas")
    if request.param == "duckdb-in-memory":
        return memory_conn.sql("SELECT * FROM df_pandas")
    if request.param == "duckdb-persistent":
        return persistent_conn.sql("SELECT * FROM df_pandas")
    else:
        raise ValueError(f"Unknown data type: {request.param}")
