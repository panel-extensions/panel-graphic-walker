import datetime
import decimal

import numpy as np
import pandas as pd
import param
import pytest

from panel_gwalker._tabular_data import TabularData, _column_datasource_from_tabular_df
from panel_gwalker._utils import cast_to_supported_dtypes


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


def test_decimal_conversion():
    df = pd.DataFrame(
        {
            "price": [decimal.Decimal("10.50"), decimal.Decimal("25.75")],
            "qty": [5, 10],
            "name": ["Item A", "Item B"],
        }
    )

    converted_df = cast_to_supported_dtypes(df)

    assert isinstance(converted_df["price"][0], float)
    assert not isinstance(converted_df["price"][0], decimal.Decimal)
    assert converted_df["price"][0] == 10.5


def test_date_conversion():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    datetime.date(2020, 1, 1) + datetime.timedelta(days=i)
                    for i in range(3)
                ]
            ),
            "value": np.random.randn(3).cumsum(),
        }
    )
    converted_df = cast_to_supported_dtypes(df)
    print(df)

    assert isinstance(converted_df["date"][0], pd.Timestamp)
    assert converted_df["date"][0] == pd.Timestamp("2020-01-01")
