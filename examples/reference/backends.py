import os
import tempfile

import dask.dataframe as dd
import duckdb
import ibis
import pandas as pd
import panel as pn
import polars as pl

from panel_gwalker import GraphicWalker

pn.extension()


DATA = "https://datasets.holoviz.org/windturbines/v1/windturbines.parq"

df_pandas = pd.read_parquet(DATA)
duckdb_relation = duckdb.sql("SELECT * FROM df_pandas")

con = ibis.connect("duckdb://tmp.ibis.db")
if not "my_table" in con.list_tables():
    con.read_parquet(DATA, "my_table")
ibis_table = con.table("my_table").execute()


DATAFRAMES = {
    "pandas": df_pandas,
    "polars": pl.read_parquet(DATA),
    "dask": dd.read_parquet(DATA, npartitions=1),
    "duckdb": duckdb_relation,
    "ibis": ibis_table,
}

select = pn.widgets.Select(options=list(DATAFRAMES), name="Data Source")
kernel_computation = pn.widgets.Checkbox(name="Kernel Computation", value=False)


@pn.depends(select, kernel_computation)
def get_data(value, kernel_computation):
    data = DATAFRAMES[value]
    if not kernel_computation:
        try:
            data = data.head(1000)
        except:
            data = data.df().head(1000)
    try:
        return GraphicWalker(
            data,
            kernel_computation=kernel_computation,
            sizing_mode="stretch_width",
            tab="data",
        )
    except Exception as ex:
        msg = f"Combination of {value=} and {kernel_computation=} is currently not supported."
        return pn.pane.Alert(msg, alert_type="danger")


pn.Column(select, kernel_computation, get_data).servable()
