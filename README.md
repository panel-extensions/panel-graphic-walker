# ✨ Welcome to Panel Graphic Walker

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)
[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAB5hHGcAA42ST2_iMBDFvwryBSoFQ8JCIFIvu1rtnvewPZQKGTwQa4Pt2kNoivjuO86fUqRWVMkh8zx-b_xzTmxjJLCMqb01DntWaCl8j14rl_oiQlFreqm3zuwbZbU7iuIfuF7b9ssJm6vNQy0uqdVqDi8I2iujB3dBkdvePTlzB0KurHDPB8BBP0e0PhuNpEDhAT3PTWFK9cqN242OSks8uLXS4EdlfFXzYNGvna_CB3Ib9bx6VXq32tP57vseHeAmX60N5v077sGVYl1AMxWLmIPng3KwB42eaGyFx3a8JR2lPm77QXjepOGuSR02IIJOXljZQLTuoFJY-1fBkWVbUXiIGEiFP3VIZxm6Aym2wtzosKUyUkkYlmOezHhMmwtRmQOy7MRKcIEjyxKa1hj8Y8jy1IU5qiK2yVUhHVDT49sKijUxpcWjkpizLJ6OI7ZX-qEpJ031G9Qup5xQKhkIqAK-kyuR-mE0CsLtPkkIrcN100stVgRfxs5P5-iDKdqg2ZzPJkk6TtP0W7qYLyafTn-xJJLcVuza9rL8_g45vuD1BA2hLj6exHwyS5NFkiTTZByP5zfo3SbWErhFqwP1MZ68my-dfiUTwZEsiluhXV9IDc85qm-NfvXHp_N_IeI7ygQEAAA)

**A simple way to explore your data through a *[Tableaux-like](https://www.tableau.com/)* interface directly in your [Panel](https://panel.holoviz.org/) data applications.**

![panel-graphic-walker-plot](https://github.com/philippjfr/panel-graphic-walker/blob/main/static/panel-graphic-walker_plot.png?raw=true)

## What is Panel Graphic Walker?

`panel-graphic-walker` brings the power of [Graphic Walker](https://github.com/Kanaries/graphic-walker) to your data science workflow, seamlessly integrating interactive data exploration into notebooks and [Panel](https://panel.holoviz.org/) applications. Effortlessly create dynamic visualizations, analyze datasets, and build dashboards—all within a Pythonic, intuitive interface.

## Why choose Panel Graphic Walker?

- **Simplicity:** Just plug in your data, and `panel-graphic-walker` takes care of the rest.
- **Quick Data Exploration:** Start exploring in seconds, with instant chart and table rendering via a *[Tableau-like](https://www.tableau.com/)* interface.
- **Integrates with Python Visualization Ecosystem:** Easily integrates with [Panel](https://panel.holoviz.org/index.html), [HoloViz](https://holoviz.org/), and the broader [Python Visualization](https://pyviz.org/tools.html) ecosystem.
- **Scales to your Data:** Designed for diverse data backends and scalable, so you can explore even larger datasets seamlessly. *(Features Coming Soon)*

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

![panel-graphic-walker-table](https://github.com/philippjfr/panel-graphic-walker/blob/main/static/panel-graphic-walker_table.png?raw=true)
![panel-graphic-walker-plot](https://github.com/philippjfr/panel-graphic-walker/blob/main/static/panel-graphic-walker_plot.png?raw=true)

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

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAEHYHWcAA6VSXW_aMBT9K5GfQAomCSuBSOyh1bRpD5u0SetDUyGDDbEWbNe-SUor_vuuk1DG1IpJTZDgfp17OPc8k7XmgmRE7oy2EBimOHMBfgzP1Skpyjancnw3Vu-63HLbsPK3sEHf-NkyU8j1bZv0rUZR8QhCOanVYOgzfBMsEJtawfhy7epBTgoA47LxmDNgToCjhS51LZ-otttxIxWHyq6kEm5cx2cxxXm6fcpJGCirG7eII3zaNbnqmS3OSQ34ButI60aX1U4NchXg0_WGXYDFH7rpK32ikXzrmV1XAFpRr8DSMMt2g26UtgH-Vy_Dcl1ZKxR-F8xCGMi1VouccN2oUjOek2HoMb2C9OvP79_OMf4Z5sJAsUiGPbn381mW0r2PVI_QMZscmaGsQ-qErdmqFN2tSUiseKikFTscduiyDXOAiA-VgBwN0pqo_4G2e0mNtt3NRh2Jj4uIJjTyZYSEvfGGbRsxZMb8kqIh2YaVToREcAmflCdBMrAVZsweCq38yF5zycWoRrgpjXG4ZHtdAcmeSS2sNynJEiStNaAFfLpfhu7C7nUhS446kOzupQJshZ7FIp4ECpLFV1FIdlLdduGki74IuS1wjw8l90LIUlx7zwp7oxUwtLN9Y4NvHa26XmwxzOMScrg_hK-w6BdNZ3Q6SdIoTdMP6Xw2n7zJ_gSJSlKzJ-ewp_Lfp6TwCOcMOoWO6-NJTCfTNJknSXKVRHE0u6DeZcV6BS6pdRTqdXmKI7_06n92grCYZuWlpcc-v9W_h7C9Gjr-7v7wBw0Ywf5jBQAA)

You can *export the current* chart from the client to the server by triggering the parameter `export_current_chart`.
The chart is exported to the `current_chart` parameter:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000)


walker = GraphicWalker(df)
pn.Column(
    walker,
    pn.Row(
        pn.widgets.Button.from_param(walker.param.export_current_chart, icon="download"), pn.pane.JSON(walker.param.current_chart, depth=2),
        pn.widgets.Button.from_param(walker.param.export_current_chart_list, icon="download"), pn.pane.JSON(walker.param.current_chart_list, depth=3),
    )
).servable()
```

### Scale with Server-Side Computation

In some environments you may meet message or client side data limits. To handle larger datasets, you can offload the `computation` to the `"server"`:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

# Load a sample dataset with 10,000 rows
df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000)

# Enable server-side computation for scalable data processing
GraphicWalker(df, computation="server").servable()
```

This setup allows your application to manage larger datasets efficiently by leveraging server resources for data processing.

### App Demo

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIALXZHWcAA61WbVPbOBD-Kx73SzLjOAmQQjPjm6MF0l5pYWh7fMCMR7GVRMWWXFkOSRn--z1ry8HhYGDmLpQG7Wp3Hz37It25sUq4O3ZnWmWOUI7IcqWN881oIeefzkIZSivKmUxY4eBfnrSFPK1k2BjKyksli-a3LL3hunE40SxfiPiyEtLWXPp8ZbgshJKd0J2JlCda5Tm0rucU4jfiRxnABaFbGM1NvIhuRWIWodsl-_PDr8en0eQy-nFx6gRO6C6MyYtxvz8XZlFO_VhlfURMRZ7_nOl-Bao3r1H0amyhG0o4OD2bnG15uGGSacELX3LTjyRg9gvDjIj7GU8E2-h7qZorf8De8elgb-jncm49Hp5_eg7SZ2vb34bSxwl5P2NCvmG5sG4mPz4dHf_rfImKC38L4iNXCTOstxS_-7HmzPBesyav9PMnqI9ZvOChTPjMmXMT0ZZOdxxKBx9wXWqJLPuwT6K4WHZqBX1aOGBTcFP4C5UquPeVnvdvhUxgPRUSR1wOt9Y-PPlzwPAcqdVtEQwH-NSuq5Q-4OErluUpjxJ1K1PFkg22ZAYugOwIwU80y3gL2l2IYi6l0evQHTtXoXvEZcb0DQUM3QnXGZNQXdMqV3mZIqVKVntHEZDQr-ccVN_0e32_wUZfKFTEbhqjY6XJzDeq4gh6z8Fx-So4YWnBH8z8gvObzsAKLL2Q12e2fRJst0jnIS3PdcNU2WZAFgz0BVEj_Q8qLTO0VBUMa6p8_wt4IDLRaW_eON-sATEDhuZCBh0cfdTtehsz9BogFP4FS4R6Xxqj5ESrMvepx6OcgfwW9_UhEAtin6GL8YeMuedMK8vIrHOCnmuBeEjCRlGYdUoaVZoURUI1WnFugWz5jZWciTk0ODPNi6jMqTjqYzd4T6A4qgeJxcfimOeGJxHZEJAiQHEYamvkjQqi3peVqRGoujp9jZCtKrsIOSCcoy_vgd6mlrAXAepuqnRC82SM0hrmKweDcsETZ5qy2JZfvaOnwWYJ3mnjXr4K3Xvra8HFfGGCg1HreE31P3HApi9q45il6RShgqd6x3PImUSvAL5VUisS1YjEVzSfo4LH1A2vLqHjyuw1BVTXTrtstpJq48el1lzie8G0QR8h14DbnAFl7m2A_PXt7Ou2j0fGCdK9CHb-HyxRKor_Bsh6qFHtEirQTlO8RfqsIvUIwhAzIZQ956p1Y9nJft2xl97F4fnH6PLw9PPxBV0P3drAzg-nHiDOj4LNuTMpRcKvO-3b5OntuLOqbfjutm8KwOYyKTqthvPQlhhAwXdd0pSjoQ0NhhWPaqCdJUuhsjNbzJxqbZf0oebDqelq7QjTGPjV_0Wn27Wjsj3xN3fRZgKTk_ZOxJHK0ETmWW7WrXCtSaKmP0E6XCaz-ow4osF-XAbcP2GFOUWyvluB7QC65gP7ULA1ZYSpxtZ59f7ZpvJhPoD6KdOYNhskbRYfSTf9-iBvBntLtN2uLUW7oKx4M9jwrAiubA21ZFHK1pi7wVcladx1cU_pJZumnC4313M1_1UKzTNUckFPRLCD8v5VchPiCVfVp_0D824jevTI-iMY-Dv-gNRwSeMXrqqNWOKm-FvwW3c8q0aui-eVOZYEwR0bVJfn5muzUJJM1ioBn70l3L31hzCu0bvjO3fJNT0j3fEOQCtlLhRc3jXB8NbA7hhvwQRN6Y6vNhrDpqAYyuph6Y6Ho4HnZkJe1svdevWxGs31UiREBNL1nl4wXH9Q0oBJrp-JQFt703ovtuSM_Lru_fW99wQKG-hg19_fHe3tHwwHo73RcOfds-gfXIJJP1_jOnla3U6lb1ZmG0HNUBN-OHwLivdGO8ODd3ujvYP94QvsvcyYZeAlthqinqanviKBb3_0mpgYKxCz9KWgzT6KSj_3XpU1VPzV9f0_lWlZnyANAAA) [![Static Badge](https://img.shields.io/badge/source-code-blue)](examples/app_demo.py)

![Panel Graphic Walker App Demo](static/panel-graphic-walker-app-fileupload.gif)

## API

### Parameters

#### Core

- `object` (DataFrame): The data for exploration. Please note that if you update the `object`, then the existing chart(s) will not be deleted and you will have to create a new one manually to use the new dataset.
- `appearance` (string): Optional dark mode preference: 'media', 'dark', 'light' or 'panel' (default). If 'panel' the the appearance is derived from `pn.config.theme`.
- `computation` (str): The computation configuration. One of 'client' (default)` or 'server'.
- `fields` (list): Optional specification of fields (columns).
- `config` (dict): Optional additional configuration for Graphic Walker. See the [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details.

#### Export Chart

- `current_chart (dict)`: The current chart. Only updated when `export_current_chart` is triggered.
- `export_current_chart` (event): Updates the current chart.
- `current_chart_list` (list): The current chart list. Only updated when `export_current_chart_list` is triggered.
- `export_current_chart_list` (event): Updates the current chart list.

## Vision

Our dream is that this package is super simple to use and supports your use cases:

- Great documentation including examples.
- Supports your preferred data backend including Pandas, Polars and DuckDB.
- Supports persisting and reusing Graphic Walker specifications.
- Scales to even the largest datasets only limited by your server or cluster.

## ❤️ Contributions

Contributions and co-maintainers are very welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/philippjfr/panel-graphic-walker). Check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for more information.
