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
- **Scales to your Data:** Designed for diverse data backends and scalable, so you can explore even larger datasets seamlessly. *(Features Coming Soon)*

## Pin your version!

This project is **in early stages**, so if you find a version that suits your needs, it’s recommended to **pin your version**, as updates may introduce changes.

Please note that displaying larger datasets (>= 10 MB) may currently not be possible depending on the limits of your environment.

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

### Configuring the Appearance

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAMfaHGcAA42SQY_aMBCF_0rkEysFk4RCIBI9tKracw_dw2a1MnggVoPttYewLOK_d5yQpUi7YpMcMuOXec-fc2QrI4EVTG2tcRhZoaXwET1WlvrShLrt6ZLutTPbrve02Yv6L7joLPzphK3U6r5tBqnVHF4QtFdGD-5CR66jBc3mDoR8WvlmUOqIrpJViNYXo5EUKDyg55WpTaNeuXGb0V5piTu3VBr8qEmvak5T-Oa1ZHGkndn7RZrQVerW7irRQK7jSFgLwgm9gkXJtiCVKNkd9-AasayhC8li5uB5pxxsQaMnPGvh0Qr3vAMsaWft7s8vxOutNdx0fsOOy9dFwjOehGUaiQcbSLdCKinIHwV7VqxF7SFmFAV_6BCCFeh21LEHrIwOnxyMVBKGDY2b8pQ-rsXB7JAVR9aAC3RZkVFoY_C3oZHH3oyAkHpVqVo6INHD2wqKJWGmxb2SWLEinSQx2yp935XjrvoFalORTyiVDCBUDd8CZnDfjUZBJ-A-cAjS4bLTksSKMJex0-MpfifF2Wg649Nxlid5nn_J57P5-MP0l5FEktsDux57Wf7_KDm-4HWCjlBvn45TPp7m2TzLskmWpMnsBr3bxM4EbtHqQb2Pp-rz5ZPPeCI4aov6lmmvC67hPsXtqdEf__B4-gduo4LZHAQAAA)

By default, the appearance is determined by `pn.config.theme`. However, you can manually change this, for example, to `media`, which corresponds to the user's preference as set in the browser.

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

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAEkeHmcAA51SXW_aMBT9K5GfQAomCSuBSOyh1bRpD5u0SetDUyGDDbEWbNe-SUor_vuuk1CG1IqqCQ_cz3Ny7nkma80FyYjcGW0hMExx5gL8GZ6rU1KUbU7l-G6s3nW55bZh5V9hg77xq2WmkOvbNulbjaLiEYRyUqvB0Gf4JljgbmoF48u1qwc5KQCMy8ZjzoA5AY4WutS1fKLabseNVBwqu5JKuHEdn8UU5-n2KSdhoKxu3CKO8GlhctUzW5yTGvAN1pHWjS6rnRrkKsCn6w27AIu_dNNX-kQj-dYzu64AtKJegaVhlu0G3ShtA_xWL8NyXTALYSDXWi1ywnWjSs14Toah3-WVo99___xxPtsPcWGgWCTDnszH8ZeldB8j0U92TCZHJijbkDpha7YqRXdLEhIrHippxU4ocOiiDXOAmx4qATkaoDVJ_wdt9ZIabbubjDrwz4uIJjTyZVwJe-MN2TZiyIz5I0VDsg0rnQiJ4BK-KE-CZGArzJg9FFr5kb3mkotRjeumNMbhku11BSR7JrWw3oQkS5C01oAn9ukeDN2D3etCltwKbLp7qQBboSexiCeAgmTxVRSSnVS3XTjpom9CbgvE8aHkXghZimvvSWFvtAKGdrVvIPjW0arrxRbD_F5CDveH8BUWPdB0RqeTJI3SNP2UzmfzyZvsTytRSWr25Hztqfz_KSk8wjmDTqEjfDyJ6WSaJvMkSa6SKI5mF9S7rFivwCW1jkK9Lk9x5JdevQcThMU0Ky-BHvs8qn8PYXs1dPzd_eEfYFOR40MFAAA)

You can *export the current chart* from the client to the server by triggering the parameter `export_chart`. The chart is exported to the `chart` parameter:

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
        pn.widgets.Button(icon="download", on_click=export),
        exported,
    )
).servable()
```

### Scale with Server-Side Computation

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIANV3IGcAA41SwY7aMBD9lci9sFIwEAqBSPTQVdWeq6p72KyQiSeJ1cT22g4si_j3jpOwgLormuSQmXl-b-aNDyRTHEhCRK2VcYFmkjMb4Kd5Ks9JqNqcTPHNjaq73LrYseoPmKAHfjdMlyJ7aJMeqiWFFwfSCiUHdz7D82CF3NQA4-vMbgcpKZ3TNhmNOHPMgrO0VJXaileqTDHaCcldYzZCgh1tJ1cxxfO0eE1Jy_wp-CbZpoLAgtmCGVrBIchUrRvHHOoHuTKBzVjVgrxYoI3KwFohi1T2k6yuhxjwPOwJ1xdcq1-mgVYVJ7xXVVPLQSoDfDqa8DKgmhlW039ZEHXXpn1HnT0kJAaeG2GgBuksLiZn1iHBcwMuRU9b3_sf3NRbalh0bQ87zS-rMY3o2JeR0u2133ELxJBp_VvAjiQ5qyyEBLhwnXckcThYSPTelUr6I3vF0cfhFunmdIKHK7ZXjSPJgeA0fq8kibBppdxPhZSHk5jBKCRZKSpuAEGPbxXHNrhmLO4EdyVJJrNxSGohH7pw2kU_QBQl6vhQcG-EqOArsqJh90o6hjfAfKDgocNNh0WIZp6XkOPTMXyni15ovqDzaRSP4zj-HC8Xy-mH3Z8p0Umq9-Sa9ly-XCV1L-66g86hk_xkOqHTeRwtoyiaRePJeHHDvduO9Q7ccutk1Pv2lKf-4tn_aDowmGbVLdETzqv69xi2W8Mb__h0_AtVJe61lgQAAA)

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

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/app_demo.py&requirements=panel-graphic-walker%0Afastparquet) [![Static Badge](https://img.shields.io/badge/source-code-blue)](examples/app_demo.py)

![Panel Graphic Walker App Demo](static/panel-graphic-walker-app-fileupload.gif)

## API

### Parameters

#### Core

- `object` (DataFrame): The data for exploration. Please note that if you update the `object`, then the existing chart(s) will not be deleted and you will have to create a new one manually to use the new dataset.
- `fields` (list): Optional specification of fields (columns).
- `server_computation` (bool): Optional. If True the computations will take place on the Panel server or in the Jupyter kernel instead of the client to scale to larger datasets. Default is False.

#### Style

- `appearance` (str): Optional dark mode preference: 'light', 'dark' or 'media'. If not provided the appearance is derived from `pn.config.theme`.
- `theme` (str): Optional chart theme: 'vega' (default), 'g2' or 'streamlit'.

#### Other

- `config` (dict): Optional additional configuration for Graphic Walker. See the [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details.

### Methods

- `calculated_fields()`: Returns a dictionary of `fields` calculated from the `object`. This is a
great starting point if you want to provide custom `fields`.
- `export(mode: 'code' | 'svg' = 'svg', scope: 'current' | 'all', timeout: int = 5000)`
  Returns chart(s) from the frontend exported either as Vega specifications or as SVG strings.

## Vision

Our dream is that this package is super simple to use and supports your use cases:

- Great documentation including examples.
- Supports your preferred data backend including Pandas, Polars and DuckDB.
- Supports persisting and reusing Graphic Walker specifications.
- Scales to even the largest datasets only limited by your server or cluster.

## ❤️ Contributions

Contributions and co-maintainers are very welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/panel-extensions/panel-graphic-walker). Check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for more information.
