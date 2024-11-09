from pathlib import Path

import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

ROOT = Path(__file__).parent
CSS = """
body {
  position: relative;
  background: none;
}

body::after {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("https://i.ytimg.com/vi/1YLStcrROgw/hq720.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-position: center;
  opacity: 0.3; /* Adjust transparency level here (0 = fully transparent, 1 = fully opaque) */
  z-index: -1;
}
"""
DATASET = "https://datasets.holoviz.org/significant_earthquakes/v1/significant_earthquakes.parquet"
# https://cdn.jsdelivr.net/gh/panel-extensions/panel-graphic-walker@main/examples/earthquake_dashboard/earthquake_dashboard.json
SPEC = ROOT / "earthquake_dashboard.json"


@pn.cache
def get_df() -> pd.DataFrame:
    df = pd.read_parquet(DATASET)
    df["Time"] = pd.to_datetime(df["Time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    return df


pn.extension(raw_css=[CSS], theme="dark", sizing_mode="stretch_width")

df = get_df()


description = pn.pane.Markdown(
    f"""
# 🌋 Earthquake Visualization (1900-2023)

## Use [panel-graphic-walker]() or [pygwalker](https://github.com/kanaries/pygwalker) for interactive visualization of geospatial data.

Source: [Data]({DATASET}), Credits: [earthquake-dashboard-pygwalker](https://earthquake-dashboard-pygwalker.streamlit.app/)
""",
    sizing_mode="fixed",
    styles={"background": "black", "border-radius": "4px", "padding": "25px"},
    margin=25,
    stylesheets=["""* {--design-primary-color: #B22222;}"""],
)

walker = GraphicWalker(
    df,
    kernel_computation=True,
    theme_key="g2",
    appearance="dark",
    spec=SPEC,
    margin=(0, 25, 25, 25),
)

# Arrange components in a Panel layout
app = pn.Column(
    description,
    walker,
    styles={"margin": "auto"},
    sizing_mode="stretch_both",
    max_width=1600,
)

# Display the app
app.servable()
