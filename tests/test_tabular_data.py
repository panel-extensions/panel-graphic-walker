import decimal
import pandas as pd
import param
import pytest

from panel_gwalker._tabular_data import TabularData, _column_datasource_from_tabular_df
from panel_gwalker._utils import convert_decimals_to_float


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
    df = pd.DataFrame({
        'price': [decimal.Decimal('10.50'), decimal.Decimal('25.75')],
        'qty': [5, 10],
        'name': ['Item A', 'Item B']
    })
    
    converted_df = convert_decimals_to_float(df)
    
    assert isinstance(converted_df['price'][0], float)
    assert not isinstance(converted_df['price'][0], decimal.Decimal)
    assert converted_df['price'][0] == 10.5
