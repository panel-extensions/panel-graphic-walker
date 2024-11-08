from pathlib import Path

import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension(sizing_mode="stretch_width")

ROOT = Path(__file__).parent
# Source: https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv
DATASET = "https://datasets.holoviz.org/significant_earthquakes/v1/significant_earthquakes.parquet"
SPEC_PATH = ROOT / "spec.json"
ACCENT = "#ff4a4a"

if pn.config.theme == "dark":
    BOX_SHADOW = "rgba(255, 255, 255, 0.95)"
else:
    BOX_SHADOW = "rgba(0, 0, 0, 0.1)"

CSS = """
.pn-gw-container {
    border: 1px solid #ff4a4a;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0px 4px 10px {BOX_SHADOW};
    margin: 10px;
    transition: box-shadow 0.3s ease;
}

/* Add a hover effect for a more interactive look */
.pn-gw-container:hover {
    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.15);
}
"""


@pn.cache
def get_data():
    return pd.read_parquet(DATASET)


data = get_data()

walker = GraphicWalker(
    data,
    theme="streamlit",
    spec=SPEC_PATH,
    sizing_mode="stretch_both",
)

main = pn.Tabs(
    walker.explorer(name="EXPLORER"),
    walker.profiler(name="PROFILER"),
    walker.viewer(
        name="VIEWER",
        index=[0, 1],
        sizing_mode="stretch_width",
        container_height="400px",
        height=1000,
        stylesheets=[CSS],
    ),
    walker.chart(
        [0, 1],
        object=data.sample(10000),
        sizing_mode="stretch_both",
        container_height="400px",
        name="CHART",
        stylesheets=[CSS],
    ),
    dynamic=True,
)


sidebar = pn.Column(
    "https://images.fastcompany.com/image/upload/f_webp,q_auto,c_fit/fc/3036624-poster-p-1-is-this-the-worlds-best-bike-share-bike.jpg",
    """## Bike Sharing

This is a dashboard for visualizing bike sharing data.

The data is sourced from the
[UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset).

## Panel-Graphic-Walker

This dashboard is built using the **[panel-graphic-walker](https://github.com/panel-extensions/panel-graphic-walker)** \
and inspired by a [similar Streamlit app](https://pygwalkerdemo-cxz7f7pt5oc.streamlit.app/).

## Notes

I've simplified the [spec.json](spec.json) file and inserted the `range` filter manually \
[#654](https://github.com/Kanaries/pygwalker/issues/654).
""",
)

pn.template.FastListTemplate(
    title="Bike Sharing Dashboard",
    main_layout=None,
    accent=ACCENT,
    sidebar=[sidebar],
    main=[main],
    main_max_width="1200px",
).servable()
