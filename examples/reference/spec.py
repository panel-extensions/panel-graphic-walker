import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

SPEC = "https://cdn.jsdelivr.net/gh/panel-extensions/panel-graphic-walker@main/examples/reference/spec.json"

pn.extension(sizing_mode="stretch_width")

df = pd.read_csv(
    "https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000
)

GraphicWalker(df, spec=SPEC).servable()
