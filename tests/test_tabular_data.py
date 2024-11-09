import pandas as pd
import param
import polars as pl
import pytest
from pygwalker.data_parsers.database_parser import Connector as DatabaseConnector

from panel_gwalker._tabular_data import TabularData, _column_datasource_from_tabular_df


class MyClass(param.Parameterized):
    value = TabularData()


def test_tabular_data(data):
    my_class = MyClass(value=data)


def test_tabular_data_raises():
    data = [{"a": [1, 2, 3]}]
    with pytest.raises(ValueError):
        my_class = MyClass(value=data)


def test_column_datasource_from_tabular_df(data):
    assert _column_datasource_from_tabular_df(data)
