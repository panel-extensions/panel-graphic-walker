# ✨ Welcome to Panel Graphic Walker

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)
[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAB5hHGcAA42ST2_iMBDFvwryBSoFQ8JCIFIvu1rtnvewPZQKGTwQa4Pt2kNoivjuO86fUqRWVMkh8zx-b_xzTmxjJLCMqb01DntWaCl8j14rl_oiQlFreqm3zuwbZbU7iuIfuF7b9ssJm6vNQy0uqdVqDi8I2iujB3dBkdvePTlzB0KurHDPB8BBP0e0PhuNpEDhAT3PTWFK9cqN242OSks8uLXS4EdlfFXzYNGvna_CB3Ib9bx6VXq32tP57vseHeAmX60N5v077sGVYl1AMxWLmIPng3KwB42eaGyFx3a8JR2lPm77QXjepOGuSR02IIJOXljZQLTuoFJY-1fBkWVbUXiIGEiFP3VIZxm6Aym2wtzosKUyUkkYlmOezHhMmwtRmQOy7MRKcIEjyxKa1hj8Y8jy1IU5qiK2yVUhHVDT49sKijUxpcWjkpizLJ6OI7ZX-qEpJ031G9Qup5xQKhkIqAK-kyuR-mE0CsLtPkkIrcN100stVgRfxs5P5-iDKdqg2ZzPJkk6TtP0W7qYLyafTn-xJJLcVuza9rL8_g45vuD1BA2hLj6exHwyS5NFkiTTZByP5zfo3SbWErhFqwP1MZ68my-dfiUTwZEsiluhXV9IDc85qm-NfvXHp_N_IeI7ygQEAAA)

**A simple way to explore your data through a *[Tableau-like](https://www.tableau.com/)* interface directly in your [Panel](https://panel.holoviz.org/) data applications.**

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

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAEkeHmcAA51SXW_aMBT9K5GfQAomCSuBSOyh1bRpD5u0SetDUyGDDbEWbNe-SUor_vuuk1CG1IqqCQ_cz3Ny7nkma80FyYjcGW0hMExx5gL8GZ6rU1KUbU7l-G6s3nW55bZh5V9hg77xq2WmkOvbNulbjaLiEYRyUqvB0Gf4JljgbmoF48u1qwc5KQCMy8ZjzoA5AY4WutS1fKLabseNVBwqu5JKuHEdn8UU5-n2KSdhoKxu3CKO8GlhctUzW5yTGvAN1pHWjS6rnRrkKsCn6w27AIu_dNNX-kQj-dYzu64AtKJegaVhlu0G3ShtA_xWL8NyXTALYSDXWi1ywnWjSs14Toah3-WVo99___xxPtsPcWGgWCTDnszH8ZeldB8j0U92TCZHJijbkDpha7YqRXdLEhIrHippxU4ocOiiDXOAmx4qATkaoDVJ_wdt9ZIabbubjDrwz4uIJjTyZVwJe-MN2TZiyIz5I0VDsg0rnQiJ4BK-KE-CZGArzJg9FFr5kb3mkotRjeumNMbhku11BSR7JrWw3oQkS5C01oAn9ukeDN2D3etCltwKbLp7qQBboSexiCeAgmTxVRSSnVS3XTjpom9CbgvE8aHkXghZimvvSWFvtAKGdrVvIPjW0arrxRbD_F5CDveH8BUWPdB0RqeTJI3SNP2UzmfzyZvsTytRSWr25Hztqfz_KSk8wjmDTqEjfDyJ6WSaJvMkSa6SKI5mF9S7rFivwCW1jkK9Lk9x5JdevQcThMU0Ky-BHvs8qn8PYXs1dPzd_eEfYFOR40MFAAA)

You can *export the current chart* from the client to the server by triggering the parameter `export_chart`. The chart is exported to the `chart` parameter:

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
        pn.widgets.Button.from_param(walker.param.export_chart, icon="download"), pn.pane.JSON(walker.param.chart, depth=2),
        pn.widgets.Button.from_param(walker.param.export_chart_list, icon="download"), pn.pane.JSON(walker.param.chart_list, depth=3),
    )
).servable()
```

### App Demo

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAI4eHmcAA6VW7VLbOBR9FY_7J5lxnARIoZnxztICabe0MLRdfmDGo9hKomJLriyHpAzvvufacnC6YejshtKg-3l0dO-VHtxYJdwduzOtMkcoR2S50sb5YrSQ8w8XoQylFeVMJqxw8C9P2kKeVjIYhrKKUsmi-T1L77huAk40yxcivq6EZJpLn68Ml4VQshO6M5HyRKs8h9b1nEL8RP4oA7ggdAujuYkX0b1IzCJ0u-R_efz59DyaXEffrs6dwAndhTF5Me7358Isyqkfq6yPjKnI8-8z3a9A9eY1il6NLXRDiQDnF5OLrQh3TDIteOFLbvqRBMx-YZgRcT_jiWAbfS9Vc-UP2Bs-HRwM_VzObcTjyw_PQfpoffvbUPrYIe9nTMhXLBc2zOTbh5PTf-0vUXHhb0H8JVTCDOstxc9-rDkzvNesKSr9_AnqYxYveCgTPnPm3ERk0umOQ-ngA65LLXHKPvyTKC6WnVpBnxYO-BTcFP5CpQrhfaXn_XshE3hPhcQWl8OttY9I_hwwPEdqdV8EwwE-dejqSJ_w8BXL8pRHibqXqWLJBlsyAxdAdoLkZ5plvAXtIUQxl9LodeiOnZvQPeEyY_qOEobuhOuMSahuaZWrvExxpEpWtqMISOjXc46qb_q9fdxgoy8UKnI3jdGx0mTmG1VxBL3nYLt8FZyxtOBPbn7B-V1nYAWWXsjrPds-CbZbpPN0LM91w1TZZsApGOgLokb671RaZmipKhnWVPn-J_BAZKLTXr1yvlgHYgYMzYUMOtj6qNv1Nm7oNUAo_CuWCPW2NEbJiVZl7lOPRzkD-S3u600gF8Q-QxfjDxlzz5lWnpFZ5wQ91wL5cAgbRWHWKWlUaVIUCdVoxbkFshU3VnIm5tBgzzQvojKn4qi33eA9g-KkHiQWH4tjnhueRORDQIoAxWGorXFuVBC1XVamRqDq6uNrhGxV-UU4A8I5-vQW6O3REvYiQN1NlU5onoxRWsN85WBQLnjiTFMW2_KrLXoabJbgnQwP8lXoPtpYCy7mCxMcjVrba6p_xwabvqidY5amU6QKdvWO51AwiV4BfKukViSqkYmvaD5HBY-pG367hE4rt98poLp22mWzdag2f7xg2qB_cMaA2WBHeXsbAH99ufi87WudEhzvItj7f7mjVBT_DYD1rFHsEwrQSlO6ReqsIu0EwhA9H8qec7PrRrrt2Gvt6vjyfXR9fP7x9IougG7tYieEU48I51vB5tyZlCLht532fbHbHLdSZYbvbvsuAHAuk6LTaikPjYcRE3zVJc0xGsvQYBzxqAbaWbIUKjuVxcyp1nZJH2ov7Jsuz44wjYNf_V90ul07DNszfXPbbGYsBWlbIo9UhmYuz3KzbqVrzQo1_Q7aETKZ1XvEFg3sMe65f8YKc47j-moFtsbpIg_sU8BWkRGmGkyX1Qtnm8qnCQDqp0xjnmyQtFn8RbrpyCd5M7pbou2GbCnaJWXFm9GFh0NwY2uoJYtStsZkDT4rSQOti5tIL9k05XR9uZ6r-Y9SaJ5xaQp6BIIdFPaPkpsQj7SqQu0fmGgb0S9F-0cw8Pf8AakRkgYsQlWGWOIu-Fvwe3c8q4aqiweUOZUEwR0bVJfn5muzUJJc1ioBn70lwr32h3Cu0bvjB3fJNT0U3fEeQCtlrhRCPjTJ8JqAdYzXXqI5jG42GsOmoBjK6unojoejgedmQl7Xy_169b4avvVSJEQEjustvVG4fqekAZNcP5OBTHvT2hYmOaO4rvt4--jtQGETHe37h_ujg8Oj4WB0MBruvXkW_VNIMOnna1wYu9Xto_TNymwjqBlq0g-Hr0HxwWhvePTmYHRwdDh8gb2XGbMMvMRWQ9RueupLEPgOR7-TE2MFYpa-lLSxo6z08-hVp4aKv7l9_AdzCv4JAg0AAA) [![Static Badge](https://img.shields.io/badge/source-code-blue)](examples/app_demo.py)

![Panel Graphic Walker App Demo](static/panel-graphic-walker-app-fileupload.gif)

### App with File Upload

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#c=H4sIAErxHGcAA41WbVPbOBD-Kx73izMTnIQmhWbGN9eWQm9KX4b2jg-Y8ci2kqjYkirLISnDf79nbcU4PXrUISTaXe0-evZFufMzlXN_7i-MKj2hPFFqZaz3xRohl399imUsnUgzmbPKw5_O-0JeNDIYxrLx0siS5S0rbrjZOTwzTK9EdtkIyVTLkG8sl5VQMoj9hSh4bpTW0PpDrxI_ED8pAS6K_coabrNVcityu4r9Ae3__Orj2_Pk7DL5--Lci7zYX1mrq_lotBR2VadhpsoRIhZC628LM2pAHSxbFActttiPJRycfzr7tOfhhklmBK9Cye0okYA5qiyzIhuVPBes0x8UaqnCMXvJ0_F0Emq5dB7_B9J7t3f0Xyj0-hO0ZCxb8VjmfOEtuU1yZlkwmMfSwwMeaiORgdBwlidZtQ5aBT0PAWlPxW0VrlSh1uJHqMxydCtkjt2pkAi_nuytQ3gKlz-IemnUbRVNxnha1w3dD3j4hpW64EmubmWhWN5hyxc4NJCdIPipYSXvQbuLUWi1tGYb-3PvKvZPuCyZuaGAsX_GTckkVNe00krXBehWsrGdJUBC76F33HzS-_q-w0YfKCLE3hVt4KT5IrSq4Qj6oYfj8k10yoqKP2wLK85vgrETOHohb8_sajjaL9_gIS2_qtRUuUJFFiz0FVEjwzeqqEuUexMMa6rK8AN4IDLRBc-eeV_cBmIGDC2FjAIcfTYYDLtt6ANAqMILlgv1urZWyTOjah1S_yWagfwe9-0hEAvikKHD8EVmfOilzc7EbjVB10YgHpLQKSq7LUijalugSKhGG84dkD2_mZILsYQGZ6ZeTmpNxdEee4f3FIqTtskdPpZlXFueJ7SHgFQRisNSyyFvVBCtXVkXVqDq2vTthGzT7EuQA8I5-_Aa6F1qCXsVoe5SZXJqsDlKa6I3HobYiudeWrDMlV9rcWDAZg3eyXCqN7F_73ytuFiubHQ86x1vV_2PHHDXF-3mjBVFilDRY70z9MiZRK8AvlNSKxLVru1oIuRcc5lXQY_YIehHoUVfTU3VTM0JDYqSJ21egjUroHK9KRZes3ZLeohkoKfxFgi72xA2_6tgMHAt0e_sbuZ0nUZO-paII5WlzuOlttteuF7FqPQbzyh2vmjPiCNa2KPpeXjKKnsuKvvVCRyNNGojN6xdWqywTXl-bu4g16Geu2G6OhA5T5lBVXVI-iz-JO3y8iDfNXDftGnUE5VVMdDH8qp3ubh5fh24--ni1ed3yeWr8_dvL-hawMC4apA6nNdBN7LhLty7efZviEF3pK4nGGbDlYvXkyUF26Jlo49KUqcMMOLMmqUFp7noD33Dv9fC8JJLW9HND8LRw99rbmPczM1Z3Be0Sif66e78IxqHh-GY1HBJnQtXjSGWGDL_CH7rzxdNt_q4Ne1bSRD8uUXBDn29tSslactW5UjRwRruXoQTbG7R-_M7f80N_Trw54cArZS9UHB5twuGawrWGa743HAYXXUay1JkDcrm94I_n8zGQ78U8rJdPm9X75qubpciJyJQAa_p8uPmjZIWTHLziwhkepC2tjDRjPz6_v31_fARFC7Q8fPw6PlsenQ8Gc-ms8nhy1-if3AJJkO9xSR6XN1PZWg3dh9By9Au_GTyAhRPZ4eT45fT2fT4aPIEe08z5hh4iq0dUY_T005X4Dua_U5MTCqIWfFU0J0dRaXX_bDJGir-6vr-X8Gmewj3CgAA) [![Static Badge](https://img.shields.io/badge/source-code-blue)](examples/app_demo.py)

![Panel Graphic Walker Advanced Example](static/panel-graphic-walker-app-fileupload.gif)

## API

### Parameters

#### Core

- `object` (DataFrame): The data for exploration. Please note that if you update the `object`, then the existing chart(s) will not be deleted and you will have to create a new one manually to use the new dataset.
- `appearance` (string): Optional dark mode preference: 'media', 'dark', 'light' or 'panel' (default). If 'panel' the the appearance is derived from `pn.config.theme`.
- `server_computation` (bool): If True the computations will take place on the Panel server or in the Jupyter kernel instead of the client to scale to larger datasets. Default is False.
- `fields` (list): Optional specification of fields (columns).
- `config` (dict): Optional additional configuration for Graphic Walker. See the [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details.

#### Export Chart

- `chart (dict)`: The current chart. Only updated when `export_chart` is triggered.
- `export_chart` (event): Updates the chart.
- `chart_list` (list): The current chart list. Only updated when `export_chart_list` is triggered.
- `export_chart_list` (event): Updates the current chart list.

## Vision

Our dream is that this package is super simple to use and supports your use cases:

- Great documentation including examples.
- Supports your preferred data backend including Pandas, Polars and DuckDB.
- Supports persisting and reusing Graphic Walker specifications.
- Scales to even the largest datasets only limited by your server or cluster.

## ❤️ Contributions

Contributions and co-maintainers are very welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/philippjfr/panel-graphic-walker). Check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for more information.
