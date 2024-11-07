import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension(sizing_mode="stretch_width")

df = pd.read_csv(
    "https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000
)

GraphicWalker(df).servable()
