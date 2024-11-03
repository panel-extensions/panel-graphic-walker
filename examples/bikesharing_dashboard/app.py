# Credits: https://pygwalkerdemo-cxz7f7pt5oc.streamlit.app/
import json
from pathlib import Path

import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

DATA_URL = "https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv"


@pn.cache()
def get_data():
    data = pd.read_csv(DATA_URL)
    data.to_parquet("bike_sharing_dc.parquet")
    return data


data = get_data()

DEFAULT_BUTTON_PARAMS = {
    "button_type": "primary",
    "button_style": "outline",
    "icon": "download",
    "name": "",
}


def create_save_button(walker: GraphicWalker, path: str | Path, **params):
    path = Path(path)

    async def save_spec(event):
        spec = await walker.export(mode="spec", scope="all")
        with path.open("w") as file:
            json.dump(spec, file)
        logger.debug("Saved spec to %s", path)

    params = DEFAULT_BUTTON_PARAMS | params
    return pn.widgets.Button(**params, on_click=save_spec)


walker = GraphicWalker(data)
button = create_save_button(walker, "spec2.json")

app = pn.Column(button, walker).servable()
