# Credits: https://pygwalkerdemo-cxz7f7pt5oc.streamlit.app/
# https://github.com/kanaries/pygwalker-in-streamlit/blob/main/pygwalker_demo.py
from pathlib import Path

import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension(sizing_mode="stretch_width")

ROOT = Path(__file__).parent
# Source: https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv
DATA_PATH = ROOT / "bike_sharing_dc.parquet"
SPEC_PATH = ROOT / "spec.json"
ACCENT = "#ff4a4a"


@pn.cache
def get_data():
    return pd.read_parquet(DATA_PATH)


data = get_data()

walker = GraphicWalker(
    data,
    theme_key="streamlit",
    spec=SPEC_PATH,
    save_path=SPEC_PATH.as_posix(),
    sizing_mode="stretch_both",
)

main = pn.Tabs(
    walker.explorer(name="explorer (GraphicWalker)"),
    # renderer.profiler(name="profiler (TableWalker)"),
    pn.Column(
        walker.viewer(
            name="viewer (GraphicRenderer)",
            # index=[0,1],
            sizing_mode="stretch_width",
            height=1000,
        ),
        walker.viewer(
            name="viewer (GraphicRenderer)",
            index=1,
            sizing_mode="fixed",
        ),
        name="viewer (GraphicRenderer)",
    ),
    # pn.Column(
    #     "### Registered per weekday",
    #     renderer.chart(0, object=data.sample(10000)),
    #     "### Registered per day",
    #     renderer.chart(1, object=data.sample(10000)),
    #     name="chart (PureRenderer)",
    # ),
    active=1,
    dynamic=True,
)

button = walker.create_save_button(
    include_settings=True, sizing_mode="fixed", width=300
)

app = pn.Column(
    walker,
    button,
)

pn.template.FastListTemplate(
    title="Bike Sharing Visualization with panel-graphic-walker",
    main_layout=None,
    accent=ACCENT,
    sidebar=[button, walker.param.index],
    main=[main],
).servable()
