from typing import TYPE_CHECKING, Any, Union

import bokeh.core.properties as bp
import param
from bokeh.core.property.bases import Property
from bokeh.models import ColumnDataSource
from panel.io.datamodel import PARAM_MAPPING

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl
    from pygwalker.data_parsers.database_parser import Connector

TabularDataType = Union["pd.DataFrame", "pl.DataFrame", "Connector"]

_VALID_CLASSES = (
    "<class 'pandas.core.frame.DataFrame'>",
    "<class 'polars.dataframe.frame.DataFrame'>",
    "<class 'pygwalker.data_parsers.database_parser.Connector'>",
)


def _validate(val):
    try:
        if str(val.__class__) in _VALID_CLASSES:
            return
    except:
        pass

    msg = f"Expected TabularDataType but got '{type(val)}'"
    raise ValueError(msg)


class TabularData(param.Parameter):
    def _validate(self, val):
        super()._validate(val=val)
        _validate(val)


# See https://github.com/holoviz/panel/issues/7468
def _column_datasource_from_polars_df(df):
    df = df.to_pandas()
    return ColumnDataSource._data_from_df(df)


class BkTabularData(Property["TabularDataType"]):
    """Accept TabularDataType values.

    This property only exists to support type validation, e.g. for "accepts"
    clauses. It is not serializable itself, and is not useful to add to
    Bokeh models directly.

    """

    def validate(self, value: Any, detail: bool = True) -> None:
        super().validate(detail)

        _validate(value)


PARAM_MAPPING.update(
    {
        TabularData: lambda p, kwargs: (
            bp.ColumnData(bp.Any, bp.Seq(bp.Any), **kwargs),
            [(BkTabularData, _column_datasource_from_polars_df)],
        ),
    }
)
