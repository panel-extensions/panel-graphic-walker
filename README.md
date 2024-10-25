# ✨ panel-graphic-walker

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)

`panel-graphic-walker` provides the `GraphicWalker` *pane* to leverage the [Graphic Walker](https://github.com/Kanaries/graphic-walker) data exploration tool in [Panel](https://panel.holoviz.org/) data apps.

## Installation

You can install `panel-graphic-walker` using `pip`:

```bash
pip install panel-graphic-walker
```

## Usage

### Basic Graphic Walker Pane

Here’s how to create a simple `GraphicWalker` pane:

```python
import panel as pn
from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_parquet('https://datasets.holoviz.org/windturbines/v1/windturbines.parq')

GraphicWalker(df).servable()
```

![panel-graphic-walker-table](https://github.com/philippjfr/panel-graphic-walker/blob/main/static/panel-graphic-walker_table.png?raw=true)

![panel-graphic-walker-table](https://github.com/philippjfr/panel-graphic-walker/blob/main/static/panel-graphic-walker_plot.png?raw=true)

## Api

### Parameters

- `object` (str): The DataFrame to explore.

## ❤️ Contributions

Contributions and co-maintainers are very welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/philippjfr/panel-graphic-walker). Check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for more information.

----
