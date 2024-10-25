import pandas as pd
import panel as pn
from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_parquet('https://datasets.holoviz.org/windturbines/v1/windturbines.parq')

GraphicWalker(df, sizing_mode='stretch_both').servable()
