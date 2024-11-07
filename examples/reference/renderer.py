from pathlib import Path

import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

ROOT = Path(__file__).parent
SPEC = ROOT / "spec.json"

pn.extension(sizing_mode="stretch_width")

df = pd.read_csv(
    "https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000
)

GraphicWalker(df, spec=SPEC, renderer="profiler").servable()
