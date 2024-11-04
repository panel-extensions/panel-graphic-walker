# ✨ Welcome to Panel Graphic Walker

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)
[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAB5hHGcAA42ST2_iMBDFvwryBSoFQ8JCIFIvu1rtnvewPZQKGTwQa4Pt2kNoivjuO86fUqRWVMkh8zx-b_xzTmxjJLCMqb01DntWaCl8j14rl_oiQlFreqm3zuwbZbU7iuIfuF7b9ssJm6vNQy0uqdVqDi8I2iujB3dBkdvePTlzB0KurHDPB8BBP0e0PhuNpEDhAT3PTWFK9cqN242OSks8uLXS4EdlfFXzYNGvna_CB3Ib9bx6VXq32tP57vseHeAmX60N5v077sGVYl1AMxWLmIPng3KwB42eaGyFx3a8JR2lPm77QXjepOGuSR02IIJOXljZQLTuoFJY-1fBkWVbUXiIGEiFP3VIZxm6Aym2wtzosKUyUkkYlmOezHhMmwtRmQOy7MRKcIEjyxKa1hj8Y8jy1IU5qiK2yVUhHVDT49sKijUxpcWjkpizLJ6OI7ZX-qEpJ031G9Qup5xQKhkIqAK-kyuR-mE0CsLtPkkIrcN100stVgRfxs5P5-iDKdqg2ZzPJkk6TtP0W7qYLyafTn-xJJLcVuza9rL8_g45vuD1BA2hLj6exHwyS5NFkiTTZByP5zfo3SbWErhFqwP1MZ68my-dfiUTwZEsiluhXV9IDc85qm-NfvXHp_N_IeI7ygQEAAA)

**A simple way to explore your data through a *[Tableau-like](https://www.tableau.com/)* interface directly in your [Panel](https://panel.holoviz.org/) data applications.**

![panel-graphic-walker-plot](https://github.com/panel-extensions/panel-graphic-walker/blob/main/static/panel-graphic-walker_plot.png?raw=true)

## What is Panel Graphic Walker?

`panel-graphic-walker` brings the power of [Graphic Walker](https://github.com/Kanaries/graphic-walker) to your data science workflow, seamlessly integrating interactive data exploration into notebooks and [Panel](https://panel.holoviz.org/) applications. Effortlessly create dynamic visualizations, analyze datasets, and build dashboards—all within a Pythonic, intuitive interface.

## Why choose Panel Graphic Walker?

- **Simplicity:** Just plug in your data, and `panel-graphic-walker` takes care of the rest.
- **Quick Data Exploration:** Start exploring in seconds, with instant chart and table rendering via a *[Tableau-like](https://www.tableau.com/)* interface.
- **Integrates with Python Visualization Ecosystem:** Easily integrates with [Panel](https://panel.holoviz.org/index.html), [HoloViz](https://holoviz.org/), and the broader [Python Visualization](https://pyviz.org/tools.html) ecosystem.
- **Scales to your Data:** Designed for diverse data backends and scalable, so you can explore even larger datasets seamlessly. *(More Features Coming Soon)*

## Pin your version!

This project is **in early stages**, so if you find a version that suits your needs, it’s recommended to **pin your version**, as updates may introduce changes.

## Installation

Install `panel-graphic-walker` via `pip`:

```bash
pip install panel-graphic-walker
```

## Usage

### Basic Graphic Walker Pane

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAB5hHGcAA42ST2_iMBDFvwryBSoFQ8JCIFIvu1rtnvewPZQKGTwQa4Pt2kNoivjuO86fUqRWVMkh8zx-b_xzTmxjJLCMqb01DntWaCl8j14rl_oiQlFreqm3zuwbZbU7iuIfuF7b9ssJm6vNQy0uqdVqDi8I2iujB3dBkdvePTlzB0KurHDPB8BBP0e0PhuNpEDhAT3PTWFK9cqN242OSks8uLXS4EdlfFXzYNGvna_CB3Ib9bx6VXq32tP57vseHeAmX60N5v077sGVYl1AMxWLmIPng3KwB42eaGyFx3a8JR2lPm77QXjepOGuSR02IIJOXljZQLTuoFJY-1fBkWVbUXiIGEiFP3VIZxm6Aym2wtzosKUyUkkYlmOezHhMmwtRmQOy7MRKcIEjyxKa1hj8Y8jy1IU5qiK2yVUhHVDT49sKijUxpcWjkpizLJ6OI7ZX-qEpJ031G9Qup5xQKhkIqAK-kyuR-mE0CsLtPkkIrcN100stVgRfxs5P5-iDKdqg2ZzPJkk6TtP0W7qYLyafTn-xJJLcVuza9rL8_g45vuD1BA2hLj6exHwyS5NFkiTTZByP5zfo3SbWErhFqwP1MZ68my-dfiUTwZEsiluhXV9IDc85qm-NfvXHp_N_IeI7ygQEAAA)

Here’s an example of how to create a simple `GraphicWalker` pane:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000)

GraphicWalker(df).servable()
```

![panel-graphic-walker-table](https://github.com/panel-extensions/panel-graphic-walker/blob/main/static/panel-graphic-walker_table.png?raw=true)
![panel-graphic-walker-plot](https://github.com/panel-extensions/panel-graphic-walker/blob/main/static/panel-graphic-walker_plot.png?raw=true)

### Configuring Fields

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAHraHGcAA71TXW-bMBT9K8hPrUQcIGtokbKHTdP2PE3rQ6kqB5tgDWzXvpDSKP9915A0Tb-yp0Ek43uP7zk5vndDCs0FyYhsjLYQGKY4cwH-DM_VISjqIaZyfEurmzF2t1qz-o-wwQ743TJTyeJ6CHqoUVQ8gFBOanV27iO8DBZYm1rB-F3hurOcVADGZdMpZ8CcAEcrXetOPlJtV9O1VBxau5RKuGkXH-0pnqerx5yEgbJ67RZxhM9AU0pRc4dUN7kK8NmMi39yUkqekww_4K7QrYIeKzzPK9aIDwFONEyBLH71ZgdUupGK1S9wDEP9EY7LZnTjCbndre8pbPB-XtZ9LvCt_P_UVzDzkX2vsq-13bc-AAxkh5ETAhvBXGsPOC_v1t_4Ue-d8TIMxh5YjMs5dcJ2bFmLsQ9JSKy4b6UV-IfB4QSUzIFh9r4VkGPzDg2--8CReApNViPRZGz9z4uIJjTyaSwJqBNLDUDcMmN-S7EmWclqJ0IiuIRvyosgGdgWI6aHSit_pNdccjHpsNycxni4Zr1ugWQb0gnrr4RkCYrWGn5qLLnZk2HnI7qoZM2tQNDNUwbYEucJk2vJoSJZfBGFBPvgetzOxt0PIVcV8vit5N4IWYsvfp6E_aoVMBw1-w6Dh06WIxYhhvm6hGxvt-EbKnZE80s6nyVplKbpp_Tq8mr2rvpDSXSSmp4clz2kn18lhQc4VjA6tKePZzGdzdPkKkmSiySKo8sT7p12bOfAKbf2Rr1tT7XXl178CycIO4z0KdI9zrP6dxsOt4Ydf3O7_QvsHT_k_wUAAA)

You may also configure the `fields` (data columns) manually:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000)

fields = [
    {
        "fid": "t_county",
        "name": "t_county",
        "semanticType": "nominal",
        "analyticType": "dimension",
    },
    {
        "fid": "t_model",
        "name": "t_model",
        "semanticType": "nominal",
        "analyticType": "dimension",
    },
    {
        "fid": "t_cap",
        "name": "t_cap",
        "semanticType": "quantitative",
        "analyticType": "measure",
    },
]

GraphicWalker(df, fields=fields).servable()
```

You can get the full list of fields via `GraphicWalker(df).calculated_fields()`.

### Configuring the Appearance

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAMfaHGcAA42SQY_aMBCF_0rkEysFk4RCIBI9tKracw_dw2a1MnggVoPttYewLOK_d5yQpUi7YpMcMuOXec-fc2QrI4EVTG2tcRhZoaXwET1WlvrShLrt6ZLutTPbrve02Yv6L7joLPzphK3U6r5tBqnVHF4QtFdGD-5CR66jBc3mDoR8WvlmUOqIrpJViNYXo5EUKDyg55WpTaNeuXGb0V5piTu3VBr8qEmvak5T-Oa1ZHGkndn7RZrQVerW7irRQK7jSFgLwgm9gkXJtiCVKNkd9-AasayhC8li5uB5pxxsQaMnPGvh0Qr3vAMsaWft7s8vxOutNdx0fsOOy9dFwjOehGUaiQcbSLdCKinIHwV7VqxF7SFmFAV_6BCCFeh21LEHrIwOnxyMVBKGDY2b8pQ-rsXB7JAVR9aAC3RZkVFoY_C3oZHH3oyAkHpVqVo6INHD2wqKJWGmxb2SWLEinSQx2yp935XjrvoFalORTyiVDCBUDd8CZnDfjUZBJ-A-cAjS4bLTksSKMJex0-MpfifF2Wg649Nxlid5nn_J57P5-MP0l5FEktsDux57Wf7_KDm-4HWCjlBvn45TPp7m2TzLskmWpMnsBr3bxM4EbtHqQb2Pp-rz5ZPPeCI4aov6lmmvC67hPsXtqdEf__B4-gduo4LZHAQAAA)

By default, the appearance is determined by the value of [`pn.config.theme`](https://panel.holoviz.org/how_to/styling/themes.html). However, you can manually change this, for example, to `dark` or `media`. `media` corresponds to the user's preference as set in the browser.

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv(
    "https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000
)

GraphicWalker(df, appearance="media").servable()
```

### Additional Configuration

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAOfaHGcAA41SUW_aMBD-K5GfqBRMEgaBSOxh07Rp2sO0h_WhriqDL4m3YLu2CaWI_75zAmVIragdKbm7z993_i57stICSEHk2mjrI8OV4C7CxwimzkloupxiuEur133uodry5i_Y6Aj8armp5eq2SwaoURSePCgntRrchIwoowVyUwtcPKxcO2AqwsVI7b1xxWgkuOcOvKO1bnQrn6m21WgrlfAbu5QK3KhNL2KKLLR6ZiSOlNVbt0gTXEx1ciutSlmh5L7TYUSmM_WDq4qRAqM_fPj9JyNMHQL4ov2BKOOoP77oXzfUgW35soH-KiQmFh430sIalHdoYsmdN9w-bsAzvH_n0fEDXX1JDateaNi793GR0IwmoYyUfmfCPDoghtyY3xK2pCh54yAmIKT_okITpPB2gxmz87VW4chOCylg2CLdlKZ4uOE7vfGk2JMWbJgBKTJsWmv_SyPl_iSGtiF6VctGWEDQ3UvF8yUOA4tbKXxNinSSxGQt1W0fjvvoG8iqRp0QShGMkA18CsMA-1krz3FO9g2FAB0ueyxCDA-8hBzuD_ErXRyFpjM6HWd5kuf5h3w-m4_f7P5MiU5SsyOXtOfy_6Ok_slfdtA7dJJPxykdT_NsnmXZJEvSZHbFveuOHR245tbJqNftqU_95ZP3aHqwmObNNdETLqiGfYi7qeEff3d_-Ad2-7s-QgQAAA)

Extra configuration options are available via the [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api). For instance, you can change the language to Japanese:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv(
    "https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000
)

config = {
   "i18nLang": "ja-JP"
}

GraphicWalker(df, config=config).servable()
```

### Export the Chart(s)

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAPQXIWcAA41STW-bQBD9K2gvtSW8tnFjEiR6SFT149BKrdQcQmSt2TFsg3fJMkCcyP-9s4CTWErkgmUxM2_mvX07Tyw1EljE1LY0Fr1SaCkqj36lTPRLEooupxN6N9Zs-9wqa0VxB9YbgF-sKHOVXndJBy01hwcEXSmjR2OXkRsvptncgpCrtGpGCcsRyyqaTqVAUQFWPDeFadQjNzabtkpLrO1aaaimzfwo5tTPs8eE-Z62pq3i-YyejmbQFR9LGskNVeHBiQXphGjuDsK___75YyShxDxedP2i2unUk7DxevRoNY4S7dFz6OZm_RdSpCGiFQq9npGO28G7ITT9yhT1Vo_61h7i9wEVf5l2qAyJVsnMGXBZIxr9LSXTFP3FCZOm1YUR0p3V6FVaqPQu7rl8T6SoGlh10A9pDundB99Dk2UFrGRtBZL7nTfjgfv1OYYUCR7zCmwj1gX08pnPLNzXysIWNFa0JBtRYSnsfQ2Y0P12OzB80NY8pyZZb_qkP_CneMYDPnNlGom70u1bB6RQlOUfBS2LNqKowGcgFX7WTgSL0NaUKXeYG-1adkYqCZOGxi35nJoLsTM1suiJNWDdjrEoINHGIFnr0gMZLQeh01wV0gKBbp4rKNa0clQk6zFn0fxs5rOt0td9uOijr6CynHhcqKQzQhVw6VYO7JXRKGgb7TsMDjpZ91iClMLNZWx_u_ffUDEQLc_5chGEszAMP4YX5xeLd9W_jCQnebljx2Nfyq-vkuMDHivoHTrQzxdzvliGwUUQBGfBbD47P-HeaccGB065dTDqbXvyg77w7H84ESylRXGK9IBzrO7d-92t0cbf3O7_AZ8QF94iBQAA)

You can *export the current chart(s)* from the client to the server by running the *asynchronous* `export` method:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000)

walker = GraphicWalker(df)
exported = pn.pane.JSON(depth=3)

async def export(_):
    exported.object = await walker.export()

pn.Column(
    walker,
    pn.Row(
        pn.widgets.ButtonIcon(icon="download", on_click=export, active_icon='check', toggle_duration=1000),
        exported,
    )
).servable()
```

### Scale with Server-Side Computation

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAEAYIWcAA41SwY7aMBD9lci9sFIwJBQCkeihq6o9V1X3sFkhEw-J1cT22g4si_j3jpOwgLormuSQmXl-b-aNDyRXHEhKRK2VcYFmkjMb4Kd5Js9JqNqczPDdGFV3uVWxY9UfMEEP_G6YLkX-0CY9VEsKLw6kFUoO7nyGb4IlclMDjK9yux1kpHRO23Q04swxC87SUlVqK16pMsVoJyR3jVkLCXa0ja5iiudp8ZqRlvlT8E2ydQWBBbMFM7SCQ5CrWjeOOdQPNsoENmdVC_JigTYqB2uFLDLZT7K8HmLAN2FPuLrgWv4yDbSqOOG9qppaDjIZ4NPRhJcB1cywmv7Lgqi7Nu076uwhITHw3AgDNUhncTEbZh0SPDfgMvS09b3_wU29pYZF1_aw0_yyHNMJjXwZKd1e-x23QAyZ1r8F7Ei6YZWFkAAXrvOOpA4HC4neu1JJf2SvOPo43I5pPKMRHq7YXjWOpAeC0_i9kjTGppVyPxVSHk5iBqOQ5KWouAEEPb5VHFvjmrG4E9yVJI2m45DUQj504aSLfoAoStTxoeDeCFHBV2RFw-6VdAxvgPlAwUOH6w6LEM08LyHHp2P4The90GxOZ5M4GSdJ8jlZzBeTD7s_U6KTVO_JNe25fLlK6l7cdQedQyf5aBLRySyJF3EcT-NxNJ7fcO-2Y70Dt9w6GfW-PeWpv2T6P5oODKZZdUv0hPOq_j2G7dbwxj8-Hf8C2Bsh_pYEAAA)

In some environments you may meet message or client side data limits. To handle larger datasets, you can offload the *computation* to the *server*.

First you will need to install extra dependencies:

```bash
pip install panel-graphic-walker[server]
```

Then you can use server side computation with `server_computation=True`:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz")

# Enable server-side computation for scalable data processing
walker = GraphicWalker(df, server_computation=True)

pn.Column(
    walker,
    walker.param.server_computation,
).servable()
```

This setup allows your application to manage larger datasets efficiently by leveraging server resources for data processing.

Please note that if running on Pyodide the computations will always take place on the client.

### App Demo

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/app_demo.py&requirements=panel-graphic-walker%3E%3D0.3.2%0Afastparquet) [![Static Badge](https://img.shields.io/badge/source-code-blue)](examples/app_demo.py)

![Panel Graphic Walker App Demo](https://raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/static/panel-graphic-walker-app-demo.gif)

## API

### Parameters

#### Core

- `object` (DataFrame): The data for exploration. Please note that if you update the `object`, then the existing chart(s) will not be deleted and you will have to create a new one manually to use the new dataset.
- `fields` (list): Optional specification of fields (columns).
- `spec` (str, dict, list): Optional chart specification as url, json, dict or list. Can be generated via the `export` method.
- `server_computation` (bool): Optional. If True the computations will take place on the Panel server or in the Jupyter kernel instead of the client to scale to larger datasets. Default is False.
- `renderer` (str): How to display the data. One of 'GraphicRenderer', 'GraphicWalker (default), 'PureRenderer' or 'TableWalker'.
- `page_size` (int): The number of rows per page in the table of the `TableWalker`. Has no effect on other renderers.
- `index` (int): The index of the chart to display in the `PureRenderer`. Default i 0.

#### Style

- `appearance` (str): Optional dark mode preference: 'light', 'dark' or 'media'. If not provided the appearance is derived from `pn.config.theme`.
- `theme_key` (str): Optional chart theme: 'g2' (default), 'streamlit' or 'vega'. Try combining the `theme_key` 'streamlit' and the [`FastListTemplate`](https://panel.holoviz.org/reference/templates/FastListTemplate.html) `accent` color <div style="display:inline;background-color:#ff4a4a;color:white;padding:0 5px;border-radius:3px;">#ff4a4a</div>. Looks great.

#### Export and Save

- `export_mode` ('spec' | 'svg'): Used as default by `export` and `save`. Default is 'spec'.
- `export_scope` ('all' | 'current'): Used as default scope for `export` and `save`.
- `export_timeout` (int): Exports timeout in milliseconds. Used as default for `export` and `save`.
- `export` (action): Export the chart(s) as either a spec or SVG.
- `save_path` (str | PathLike): Used as default path for save. Default is 'tmp_graphic_walker.json'.
- `save` (action): Saves the chart(s) as either a spec or SVG.

#### Other

- `config` (dict): Optional additional configuration for Graphic Walker. See the [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details.

### Methods

#### Clone

- `clone`: Clones the `GraphicWalker`. Takes additional keyword arguments. Example: `walker.clone(renderer='PureRenderer', index=1)`.
- `chart`: Clones the `GraphicWalker` and sets `renderer=PureRenderer`. Example: `walker.chart(0)`.
- `explorer`: Clones the `GraphicWalker` and sets `renderer=GraphicWalker`.Example: `walker.explorer()`.
- `viewer`: Clones the `GraphicWalker` and sets `renderer=TableWalker`. Example: `walker.viewer()`.

#### Export and Save Methods

- `export`: Returns chart(s) from the frontend exported either as Vega specifications or as SVG strings. Uses the `export_mode`, `export_scope` or `export_timeout` values as defaults if `None` is provided as argument.
- `save`: Saves chart(s) from the frontend exported either as Vega specifications or as SVG strings.Uses the `save_path`, `export_mode`, `export_scope` or `export_timeout` values as defaults if `None` is provided as argument.
- `create_export_settings`: Returns a UI component to set the `export_scope`, `export_mode` and `export_timeout` parameters.
- `create_export_button`: Returns a UI component to export the chart(s) as either a spec or SVG.
The `value` parameter will hold the exported spec.
- `create_save_button`: Returns a UI component to save the chart(s) as either a spec or SVG. Will save to `save_path` path.

#### Other Methods

- `calculated_fields`: Returns a list of `fields` calculated from the `object`. This is a
great starting point if you want to provide custom `fields`.

## Vision

Our dream is that this package is super simple to use and supports your use cases:

- Great documentation including examples.
- Supports your preferred data backend including Pandas, Polars and DuckDB.
- Supports persisting and reusing Graphic Walker specifications.
- Scales to even the largest datasets only limited by your server or cluster.

## ❤️ Contributions

Contributions and co-maintainers are very welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/panel-extensions/panel-graphic-walker). Check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for more information.
