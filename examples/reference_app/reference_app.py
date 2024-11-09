from io import StringIO
from pathlib import Path

import pandas as pd
import panel as pn
import requests

from panel_gwalker import GraphicWalker

pn.extension("filedropper", sizing_mode="stretch_width", notifications=True)

ROOT = Path(__file__).parent
PANEL_GW_URL = "https://github.com/panel-extensions/panel-graphic-walker"
GW_LOGO = "https://kanaries.net/_next/static/media/kanaries-logo.0a9eb041.png"
GW_API = "https://github.com/Kanaries/graphic-walker"
GW_GUIDE_URL = "https://docs.kanaries.net/graphic-walker/data-viz/create-data-viz"
SPEC_CAPACITY_STATE_URL = "https://cdn.jsdelivr.net/gh/panel-extensions/panel-graphic-walker@main/examples/reference_app/spec_simple.json"
SPEC_SIMPLE_URL = "https://cdn.jsdelivr.net/gh/panel-extensions/panel-graphic-walker@main/examples/reference_app/spec_capacity_state.json"
ACCENT = "#5B8FF9"


def _label(value):
    return pn.pane.Markdown(value, margin=(-20, 5))


def _section_header(value):
    return pn.pane.Markdown(value, margin=(-5, 5))


@pn.cache
def get_data():
    return pd.read_parquet(
        "https://datasets.holoviz.org/windturbines/v1/windturbines.parq"
    )


@pn.cache
def get_spec(url):
    return requests.get(url).json()


SPEC_CAPACITY_STATE = get_spec(SPEC_CAPACITY_STATE_URL)
SPEC_SIMPLE = get_spec(SPEC_SIMPLE_URL)


def get_example_download():
    df = pd.DataFrame(
        {"country": ["Denmark", "Germany"], "population": [5_000_000, 80_000_000]}
    )
    sio = StringIO()
    df.to_csv(sio, index=False)
    sio.seek(0)
    return sio


button_style = dict(button_type="primary", button_style="outline")

walker = GraphicWalker(
    get_data(),
    spec=SPEC_CAPACITY_STATE,
    sizing_mode="stretch_both",
    kernel_computation=True,
)
core_settings = pn.Column(
    walker.param.kernel_computation,
    walker.param.spec,
    walker.param.config,
    walker.param.renderer,
    pn.widgets.IntInput.from_param(
        walker.param.page_size, visible=walker.is_enabled("page_size")
    ),
    pn.widgets.Checkbox.from_param(
        walker.param.hide_profiling, visible=walker.is_enabled("hide_profiling")
    ),
    pn.widgets.IntInput.from_param(
        walker.param.index, visible=walker.is_enabled("index")
    ),
    pn.widgets.RadioButtonGroup.from_param(
        walker.param.tab,
        visible=walker.is_enabled("tab"),
        button_type="primary",
        button_style="outline",
    ),
    pn.widgets.TextInput.from_param(
        walker.param.container_height, visible=walker.is_enabled("container_height")
    ),
    name="Core",
)
style_settings = pn.Column(
    _label("Appearance"),
    pn.widgets.RadioButtonGroup.from_param(walker.param.appearance, **button_style),
    _label("Theme Key"),
    pn.widgets.RadioButtonGroup.from_param(walker.param.theme_key, **button_style),
    name="Style",
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

export_controls = walker.export_controls()
exported = pn.rx("""
```bash
{value}
```
""").format(value=export_controls.param.value)
export_section = pn.Column(export_controls, exported, name="Export")
save_section = pn.Column(walker.save_controls(), name="Save")
docs_section = f"## Docs\n\n- [panel-graphic-walker]({PANEL_GW_URL})\n- [Graphic Walker Usage Guide]({GW_GUIDE_URL})\n- [Graphic Walker API]({GW_API})"


def _apply_spec(value):
    if walker.spec == value:
        walker.param.trigger("spec")
    else:
        walker.spec = value


simple_spec = pn.widgets.Button(
    name="Simple",
    button_type="primary",
    button_style="outline",
    on_click=lambda event: _apply_spec(SPEC_SIMPLE),
)
initial_spec = pn.widgets.Button(
    name="Initial",
    button_type="primary",
    button_style="outline",
    on_click=lambda event: _apply_spec(SPEC_CAPACITY_STATE),
)
no_spec = pn.widgets.Button(
    name="No Spec",
    button_type="primary",
    button_style="outline",
    on_click=lambda event: _apply_spec(None),
)


@pn.depends(file_upload, watch=True)
def _update_walker(value):
    if value:
        text = next(iter(value.values()))
        df = pd.read_csv(StringIO(text))
        if not df.empty:
            walker.object = df
        # Can be removed once https://github.com/panel-extensions/panel-graphic-walker/issues/33 is resolved
        pn.state.notifications.success(
            "New dataset uploaded. Add a new chart to use it.", duration=5000
        )


pn.template.FastListTemplate(
    logo=GW_LOGO,
    title="Panel Graphic Walker Reference App",
    sidebar=[
        "## Data Input",
        file_upload,
        file_download,
        "## Spec Input",
        pn.Row(simple_spec, no_spec, initial_spec),
        "## Settings",
        pn.Accordion(
            core_settings,
            style_settings,
            export_section,
            save_section,
            width=320,
            active=[0],
        ),
        docs_section,
    ],
    main=[walker],
    main_layout=None,
    accent="#5B8FF9",
).servable()
