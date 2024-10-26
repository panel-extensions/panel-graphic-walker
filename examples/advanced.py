import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension(sizing_mode="stretch_width")

LOGO = "https://kanaries.net/_next/static/media/kanaries-logo.0a9eb041.png"

df = pd.read_csv(
    "https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000
)

walker = GraphicWalker(df, sizing_mode="stretch_both")
settings = pn.Column(walker.param.appearance, walker.param.config)

pn.template.FastListTemplate(
    logo=LOGO,
    title="Panel Graphic Walker",
    sidebar=[settings],
    main=[walker],
    main_layout=None,
).servable()