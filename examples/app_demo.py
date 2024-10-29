from io import StringIO

import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension("filedropper", sizing_mode="stretch_width")

PANEL_GW_URL = "https://github.com/philippjfr/panel-graphic-walker"
GW_LOGO = "https://kanaries.net/_next/static/media/kanaries-logo.0a9eb041.png"
GW_API = "https://github.com/Kanaries/graphic-walker/tree/main#api"
GW_GUIDE_URL = "https://docs.kanaries.net/graphic-walker/data-viz/create-data-viz"


@pn.cache
def get_data():
    return pd.read_parquet(
        "https://datasets.holoviz.org/windturbines/v1/windturbines.parq"
    )


def get_example_download():
    df = pd.DataFrame(
        {"country": ["Denmark", "Germany"], "population": [5_000_000, 80_000_000]}
    )
    sio = StringIO()
    df.to_csv(sio, index=False)
    sio.seek(0)
    return sio

button_style = dict(button_type="primary", button_style="outline")

walker = GraphicWalker(get_data(), sizing_mode="stretch_both", server_computation=True)
settings = pn.Column(
    pn.pane.Markdown("## Settings", margin=(0, 5)),
    pn.widgets.RadioButtonGroup.from_param(walker.param.appearance, **button_style),
    walker.param.server_computation,
    walker.param.config,
)
file_upload = pn.widgets.FileDropper(
    accepted_filetypes=["text/csv"],
    multiple=False,
    max_file_size="5MB",
    styles={"border": "1px dashed black", "border-radius": "4px"},
    height=85,
)
file_download = pn.widgets.FileDownload(
    callback=get_example_download, filename="example.csv"
)

exported = pn.pane.JSON(depth=2)

mode = pn.widgets.RadioButtonGroup(
    options={'SVG': 'svg', 'Vega Spec': 'spec'}, value='spec', **button_style
)
scope = pn.widgets.RadioButtonGroup(
    options={'Current': 'current', 'All': 'all'}, value='current', **button_style
)

async def export(_):
    exported.object = await walker.export(mode=mode.value, scope=scope.value)

export_section = pn.Column(
    pn.pane.Markdown("## Export", margin=(0, 5)),
    mode,
    scope,
    pn.widgets.Button(icon="download", on_click=export),
    exported
)
docs_section = f"## Docs\n\n- [panel-graphic-walker](PANEL_GRAPH_WALKER_URL)\n- [Graphic Walker Usage Guide](GW_GUIDE_URL)\n- [Graphic Walker API](GW_API)"


@pn.depends(file_upload, watch=True)
def _update_walker(value):
    if value:
        text = next(iter(value.values()))
        df = pd.read_csv(StringIO(text))
        if not df.empty:
            walker.object = df


pn.template.FastListTemplate(
    logo=GW_LOGO,
    title="Panel Graphic Walker",
    sidebar=[
        file_upload,
        file_download,
        settings,
        export_section,
        docs_section,
    ],
    main=[walker],
    main_layout=None,
).servable()
