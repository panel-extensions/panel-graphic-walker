from typing import Any

import bokeh.core.properties as bp
import narwhals as nw
import param
from bokeh.core.property.bases import Property
from bokeh.models import ColumnDataSource
from narwhals.dependencies import (
    is_dask_dataframe,
    is_duckdb_relation,
    is_ibis_table,
    is_into_dataframe,
    is_polars_lazyframe,
)
from narwhals.typing import FrameT, IntoFrame
from panel.io.datamodel import PARAM_MAPPING

from ._utils import cast_to_supported_dtypes

TabularDataType = IntoFrame


def _validate(val: Any):
    # is_into_dataframe does not support dataframe interchange protocol in general
    # https://github.com/narwhals-dev/narwhals/issues/1337#issuecomment-2466142486
    if (
        is_into_dataframe(val)
        or is_dask_dataframe(val)
        or is_polars_lazyframe(val)
        or is_duckdb_relation(val)
        or is_ibis_table(val)
    ):
        return

    msg = f"Expected object that can be converted into Narwhals Dataframe but got '{type(val)}'"
    raise ValueError(msg)


class TabularData(param.Parameter):
    def _validate(self, val):
        super()._validate(val=val)
        _validate(val)


# See https://github.com/holoviz/panel/issues/7468
@nw.narwhalify
def _column_datasource_from_tabular_df(data: FrameT):
    if isinstance(data, nw.LazyFrame):
        data = data.collect()
    data = cast_to_supported_dtypes(data.to_pandas())
    return ColumnDataSource._data_from_df(data)


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
            [(BkTabularData, _column_datasource_from_tabular_df)],
        ),
    }
)
