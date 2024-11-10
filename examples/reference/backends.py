import dask.dataframe as dd
import duckdb
import pandas as pd
import panel as pn
import polars as pl

from panel_gwalker import GraphicWalker

pn.extension()


DATA = "https://datasets.holoviz.org/significant_earthquakes/v1/significant_earthquakes.parquet"
df_pandas = pd.read_parquet(DATA)
duckdb_in_memory_relation = duckdb.sql("SELECT * FROM df_pandas")

con = duckdb.connect("tmp.db")
duckdb_persistent_storage_relation = con.sql("SELECT * FROM df_pandas")

DATAFRAMES = {
    "pandas": df_pandas,
    "polars": pl.read_parquet(DATA),
    "dask": dd.read_parquet(DATA, npartitions=1),
    "duckdb in-memory": duckdb_in_memory_relation,
    "duckdb persistent": duckdb_persistent_storage_relation,
}

select = pn.widgets.Select(options=list(DATAFRAMES), name="Data Source")
kernel_computation = pn.widgets.Checkbox(name="Kernel Computation", value=False)

if pn.state.location:
    pn.state.location.sync(select, {"value": "backend"})
    pn.state.location.sync(kernel_computation, {"value": "kernel_computation"})


@pn.depends(select, kernel_computation)
def get_data(value, kernel_computation):
    data = DATAFRAMES.get(value, None)
    if data is None:
        return "Not a valid option"
    if not kernel_computation:
        try:
            data = data.head(10)
        except:
            data = data.df().head(10)
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
