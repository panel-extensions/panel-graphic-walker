import json
from asyncio import sleep
from pathlib import Path
from unittest.mock import patch

import dask.dataframe as dd
import duckdb
import pandas as pd
import param
import polars as pl
import pytest
from pygwalker.data_parsers.database_parser import Connector as DatabaseConnector
from sqlalchemy import create_engine, text

from panel_gwalker import GraphicWalker, experimental_duckdb_registration
from panel_gwalker._utils import _raw_fields

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
    if request.param == "duckdb-simple":
        df_pandas = pd.DataFrame({"a": [1, 2, 3]})
        return duckdb.sql("SELECT * FROM df_pandas")
    if request.param == "duckdb-in-memory":
        relation = memory_conn.sql("SELECT * FROM df_pandas")
        experimental_duckdb_registration(memory_conn, relation)
        return relation
    if request.param == "duckdb-persistent":
        relation = persistent_conn.sql("SELECT * FROM df_pandas")
        experimental_duckdb_registration(persistent_conn, relation)
        return relation
    else:
        raise ValueError(f"Unknown data type: {request.param}")
