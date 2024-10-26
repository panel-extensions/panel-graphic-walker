# ✨ panel-graphic-walker

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)
[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAB5hHGcAA42ST2_iMBDFvwryBSoFQ8JCIFIvu1rtnvewPZQKGTwQa4Pt2kNoivjuO86fUqRWVMkh8zx-b_xzTmxjJLCMqb01DntWaCl8j14rl_oiQlFreqm3zuwbZbU7iuIfuF7b9ssJm6vNQy0uqdVqDi8I2iujB3dBkdvePTlzB0KurHDPB8BBP0e0PhuNpEDhAT3PTWFK9cqN242OSks8uLXS4EdlfFXzYNGvna_CB3Ib9bx6VXq32tP57vseHeAmX60N5v077sGVYl1AMxWLmIPng3KwB42eaGyFx3a8JR2lPm77QXjepOGuSR02IIJOXljZQLTuoFJY-1fBkWVbUXiIGEiFP3VIZxm6Aym2wtzosKUyUkkYlmOezHhMmwtRmQOy7MRKcIEjyxKa1hj8Y8jy1IU5qiK2yVUhHVDT49sKijUxpcWjkpizLJ6OI7ZX-qEpJ031G9Qup5xQKhkIqAK-kyuR-mE0CsLtPkkIrcN100stVgRfxs5P5-iDKdqg2ZzPJkk6TtP0W7qYLyafTn-xJJLcVuza9rL8_g45vuD1BA2hLj6exHwyS5NFkiTTZByP5zfo3SbWErhFqwP1MZ68my-dfiUTwZEsiluhXV9IDc85qm-NfvXHp_N_IeI7ygQEAAA)

`panel-graphic-walker` provides the `GraphicWalker` Pane to utilize the [Graphic Walker](https://github.com/Kanaries/graphic-walker) data exploration tool within notebooks and [Panel](https://panel.holoviz.org/) data applications.

This project is **in early stages**, so if you find a version that suits your needs, it’s recommended to **pin your version**, as updates may introduce changes. Please note that displaying larger datasets (>= 10 MB) may not be possible depending on your environment.

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

### App with File Upload

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIACbbHGcAA41Vf1PbOBD9Kh71H2cmOAlNCs2Mb46WH70pLQztHX_EjEexlETFllxZCQkM3_3e2kpIenDUEIi1q92nt29XDywzQrIhU0VprAtKrgWvAvyWItFPizKv13SCn4k1RbOWTu94fitt4B3PLC9nKruuF72jMmvrN2eVnv51QTFKHcmlk7pSRocJm6hcCmvKEttYO6jUPTzTAtDihFXOSpfN0jsl3CxhLdp_efT15Dw9u07_vjoP4iBhM-fKatjpTJWbzcdRZooOoOSqLH9MbKdGuzdt4O01oBOWaAQ4vzi72IlwyzW3SlaRlq6TasDsVI47lXUKKRTf2PdyMzVRl7-X426_F5V66iP-D6TPfm_nv1AS_SdIyXg2k4kWchJMpUsFdzxsDRMd4AELc6tRmMhKLtKsWoSNgZ6ndLSnkq6KZiY3C3UfGTvt3CktsHusNJIvejvvESJF03siXltzV8W9Lp4mdE32Go1c8qLMZSrMnc4NFxtkYoIDA9cxUp9aXsjwIYGw5trZVcKGwShhx1IX3N5SkoSdSVtwDdMNvZWmnOcg2Ojad5AiO33awWH9nz43j0BCqSAY5FpLKfSrYhI5UzMCezvA4eQyPuV5JZ-2RZWUt2HXL3gysU4n9DKOdxUcPpXgJU2OjZckGHewV0SEjj6afF7oEN9IedEXnJxIg9LfvAm-eVfiApxMlY7DbnvQQpIGBzaBxIijHfBFZ_IXQ2b0RE2RlNomnZdUiyYvWgSYq-gUhuOmn0KeZbJ0UqTk7ValrGLUw5GuQVhdg2KeO4XKNpQRqmXtneLQdNrBlw91W7pVjt2o7dhYQbIdony9chlgZsykCMY5z3yJG489y4Wa46Tk2C-XCXtsBzOppjMXHw7WJ1jr6ZkzrJWW8TwfI3j8nA7bAYXR0B2weiOJ2s8K6ishS6lFFW4xRqSihPF3OyeVkMhhQbll2rAdLngOk9e4mgT1u3-lhzgEZhoRoXLrDVH9twpbLS-17Q7ZdO5GwRRk2xN5tHGkaFmUbrWVjh6vAzP-ITMXiwmdr56mDt5oIhmd8sqdq8p99wt-RtCwiv24azdLTjmUPGGX9Xj3yg_88GbeqVJCjrmNRzvM7ZQNwvCKhqFW-LHJqgTAEj3amrx-2N2EfnhfHV1-Sq-Pzj-fXNHMhPxHNQgP4SbcTDSEi3bG8u74bJGIG7gFRzeNfKKttTTnKzN38VejJZZbGAZ2wce5pAnC2szKn3NlZSG1q3AbTkAieu3nXLoEF1l9CP8FUt8s_XKj_BF3o_2oS2aEpFZDqNoRr-jmf5S8Y8NJ3WMMd4k70QSBDR0k2Gblys2Mpi0rI0D73gLh3kU9bG7Qs-EDW0hLdyYb7gO0Me7KIOTDOhnGN7wzXHzCSjiNNhbHx6gSjPUtyoa9QbfNCqWvm9e3zdunujWbVyWICBT6A10K0n402oFJaV_IQK5748YXLiWnuIw93jy2n0HhEx2-jQ7eDvoHh73uoD_o7b9_Ef1TSDAZlStMkufN26WM3NLtImgYWqfv9d6B4v5gv3f4vj_oHx70XmHvdcY8A6-xtSbqeXqaEQl8B4PfyYnZg2Wev5Z07UdZ6eexXVcNih_dPP4LUjyTtAsKAAA) [![Static Badge](https://img.shields.io/badge/source-code-blue)](examples/app_demo.py)

![Panel Graphic Walker Advanced Example](static/panel-graphic-walker-app-fileupload.gif)

## API

### Parameters

- `object` (DataFrame): The data for exploration. Please note that if you update the `object`, then the existing chart(s) will not be deleted and you will have to create a new one manually to use the new dataset.
- `appearance` (string): Optional dark mode preference: 'media', 'dark', 'light' or 'panel' (default). If 'panel' the the appearance is derived from `pn.config.theme`.
- `computation` (str): The computation configuration. Currently only 'client' is supported.
- `fields` (list): Optional specification of fields (columns).
- `config` (dict): Optional additional configuration for Graphic Walker. See the [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details.

## Vision

Our dream is that this package is super simple to use and supports your use cases:

- Great documentation including examples.
- Supports your preferred data backend including Pandas, Polars and DuckDB.
- Supports persisting and reusing Graphic Walker specifications.
- Scales to even the largest datasets only limited by your server or cluster.


## ❤️ Contributions

Contributions and co-maintainers are very welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/philippjfr/panel-graphic-walker). Check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for more information.
