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

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAErxHGcAA41WbVPbOBD-Kx73izMTnIQmhWbGN9eWQm9KX4b2jg-Y8ci2kqjYkirLISnDf79nbcU4PXrUISTaXe0-evZFufMzlXN_7i-MKj2hPFFqZaz3xRohl399imUsnUgzmbPKw5_O-0JeNDIYxrLx0siS5S0rbrjZOTwzTK9EdtkIyVTLkG8sl5VQMoj9hSh4bpTW0PpDrxI_ED8pAS6K_coabrNVcityu4r9Ae3__Orj2_Pk7DL5--Lci7zYX1mrq_lotBR2VadhpsoRIhZC628LM2pAHSxbFActttiPJRycfzr7tOfhhklmBK9Cye0okYA5qiyzIhuVPBes0x8UaqnCMXvJ0_F0Emq5dB7_B9J7t3f0Xyj0-hO0ZCxb8VjmfOEtuU1yZlkwmMfSwwMeaiORgdBwlidZtQ5aBT0PAWlPxW0VrlSh1uJHqMxydCtkjt2pkAi_nuytQ3gKlz-IemnUbRVNxnha1w3dD3j4hpW64EmubmWhWN5hyxc4NJCdIPipYSXvQbuLUWi1tGYb-3PvKvZPuCyZuaGAsX_GTckkVNe00krXBehWsrGdJUBC76F33HzS-_q-w0YfKCLE3hVt4KT5IrSq4Qj6oYfj8k10yoqKP2wLK85vgrETOHohb8_sajjaL9_gIS2_qtRUuUJFFiz0FVEjwzeqqEuUexMMa6rK8AN4IDLRBc-eeV_cBmIGDC2FjAIcfTYYDLtt6ANAqMILlgv1urZWyTOjah1S_yWagfwe9-0hEAvikKHD8EVmfOilzc7EbjVB10YgHpLQKSq7LUijalugSKhGG84dkD2_mZILsYQGZ6ZeTmpNxdEee4f3FIqTtskdPpZlXFueJ7SHgFQRisNSyyFvVBCtXVkXVqDq2vTthGzT7EuQA8I5-_Aa6F1qCXsVoe5SZXJqsDlKa6I3HobYiudeWrDMlV9rcWDAZg3eyXCqN7F_73ytuFiubHQ86x1vV_2PHHDXF-3mjBVFilDRY70z9MiZRK8AvlNSKxLVru1oIuRcc5lXQY_YIehHoUVfTU3VTM0JDYqSJ21egjUroHK9KRZes3ZLeohkoKfxFgi72xA2_6tgMHAt0e_sbuZ0nUZO-paII5WlzuOlttteuF7FqPQbzyh2vmjPiCNa2KPpeXjKKnsuKvvVCRyNNGojN6xdWqywTXl-bu4g16Geu2G6OhA5T5lBVXVI-iz-JO3y8iDfNXDftGnUE5VVMdDH8qp3ubh5fh24--ni1ed3yeWr8_dvL-hawMC4apA6nNdBN7LhLty7efZviEF3pK4nGGbDlYvXkyUF26Jlo49KUqcMMOLMmqUFp7noD33Dv9fC8JJLW9HND8LRw99rbmPczM1Z3Be0Sif66e78IxqHh-GY1HBJnQtXjSGWGDL_CH7rzxdNt_q4Ne1bSRD8uUXBDn29tSslactW5UjRwRruXoQTbG7R-_M7f80N_Trw54cArZS9UHB5twuGawrWGa743HAYXXUay1JkDcrm94I_n8zGQ78U8rJdPm9X75qubpciJyJQAa_p8uPmjZIWTHLziwhkepC2tjDRjPz6_v31_fARFC7Q8fPw6PlsenQ8Gc-ms8nhy1-if3AJJkO9xSR6XN1PZWg3dh9By9Au_GTyAhRPZ4eT45fT2fT4aPIEe08z5hh4iq0dUY_T005X4Dua_U5MTCqIWfFU0J0dRaXX_bDJGir-6vr-X8Gmewj3CgAA) [![Static Badge](https://img.shields.io/badge/source-code-blue)](examples/app_demo.py)

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
