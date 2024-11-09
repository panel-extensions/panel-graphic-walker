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

from panel_gwalker import GraphicWalker
from panel_gwalker._utils import _raw_fields


@pytest.fixture(params=["pandas", "polars", "dask", "duckdb"])
def data(request, tmp_path):
    if request.param == "pandas":
        return pd.DataFrame({"a": [1, 2, 3]})
    if request.param == "polars":
        return pl.DataFrame({"a": [1, 2, 3]})
    if request.param == "dask":
        return dd.from_pandas(pd.DataFrame({"a": [1, 2, 3]}), npartitions=1)
    if request.param == "duckdb":
        df_pandas = pd.DataFrame({"a": [1, 2, 3]})
        return duckdb.sql("SELECT * FROM df_pandas")
    else:
        raise ValueError(f"Unknown data type: {request.param}")
