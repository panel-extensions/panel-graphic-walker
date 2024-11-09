# ✨ Welcome to Panel Graphic Walker

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)
[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/reference_app/reference_app.py&requirements=panel-graphic-walker%5Bkernel%5D%3E%3D0.4.0%0Afastparquet)

**A simple way to explore your data through a *[Tableau-like](https://www.tableau.com/)* interface directly in your [Panel](https://panel.holoviz.org/) data applications.**

![panel-graphic-walker-plot](https://github.com/panel-extensions/panel-graphic-walker/blob/main/static/panel-graphic-walker_plot.png?raw=true)

## What is Panel Graphic Walker?

`panel-graphic-walker` brings the power of [Graphic Walker](https://github.com/Kanaries/graphic-walker) to your data science workflow, seamlessly integrating interactive data exploration into notebooks and [Panel](https://panel.holoviz.org/) applications. Effortlessly create dynamic visualizations, analyze datasets, and build dashboards—all within a Pythonic, intuitive interface.

## Why choose Panel Graphic Walker?

- **Simplicity:** Just plug in your data, and `panel-graphic-walker` takes care of the rest.
- **Quick Data Exploration:** Start exploring in seconds, with instant chart and table rendering via a *[Tableau-like](https://www.tableau.com/)* interface.
- **Integrates with Python Visualization Ecosystem:** Easily integrates with [Panel](https://panel.holoviz.org/index.html), [HoloViz](https://holoviz.org/), and the broader [Python Visualization](https://pyviz.org/tools.html) ecosystem.
- **Scales to your Data:** Designed for diverse data backends and scalability, so you can explore even larger datasets seamlessly. *(More Features Coming Soon)*

## Pin your version!

This project is **in its early stages**, so if you find a version that suits your needs, it’s recommended to **pin your version**, as updates may introduce changes.

## Installation

Install `panel-graphic-walker` via `pip`:

```bash
pip install panel-graphic-walker
```

## Usage

### Basic Graphic Walker Pane

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/reference/basic.py&requirements=panel-graphic-walker%3E%3D0.4.0) [![Static Badge](https://img.shields.io/badge/source-code-blue)](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference/basic.py)

Here’s an example of how to create a simple `GraphicWalker` pane:

```python
import pandas as pd
import panel as pn

from panel_gwalker import GraphicWalker

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/windturbines/v1/windturbines.csv.gz", nrows=10000)

GraphicWalker(df).servable()
```

You can put the code in a file `app.py` and serve it with `panel serve app.py`.

![Basic Example](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference/basic.png)

### Setting the Chart Specification

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/reference/spec.py&requirements=panel-graphic-walker%3E%3D0.4.0) [![Static Badge](https://img.shields.io/badge/source-code-blue)](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference/spec.py)

In the `GraphicWalker` UI, you can save your chart specification as a JSON file. You can then open the `GraphicWalker` with the same `spec`:

```python
GraphicWalker(df, spec="spec.json")
```

![Spec Example](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference/spec.png)

### Changing the renderer

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/reference/renderer.py&requirements=panel-graphic-walker%3E%3D0.4.0) [![Static Badge](https://img.shields.io/badge/source-code-blue)](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference/renderer.py)

You may change the `renderer` to one of 'explorer' (default), 'profiler', 'viewer' or 'chart':

```python
GraphicWalker(df, renderer='profiler')
```

![renderer.png](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference/renderer.png)

### Scaling with Server-Side Computation

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/reference/kernel_computation.py&requirements=panel-graphic-walker%5Bkernel%5D%3E%3D0.4.0%0Afastparquet) [![Static Badge](https://img.shields.io/badge/source-code-blue)](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference/kernel_computation.py)

In some environments, you may encounter message or client-side data limits. To handle larger datasets, you can offload the *computation* to the *server* or Jupyter *kernel*.

First, you will need to install extra dependencies:

```bash
pip install panel-graphic-walker[kernel]
```

Then you can use server-side computation with `kernel_computation=True`:

```python
walker = GraphicWalker(df, kernel_computation=True)
```

This setup allows your application to manage larger datasets efficiently by leveraging server resources for data processing.

Please note that if running on Pyodide, computations will always take place on the client.

### Explore all the Parameters and Methods

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/reference_app/reference_app.py&requirements=panel-graphic-walker%5Bkernel%5D%3E%3D0.4.0%0Afastparquet) [![Static Badge](https://img.shields.io/badge/source-code-blue)](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference_app/reference_app.py)

To learn more about all the parameters and methods of `GraphicWalker`, try the `panel-graphic-walker` Reference App.

![Panel Graphic Walker Reference App](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/reference_app/reference_app.gif)

## Examples

### Bike Sharing Dashboard

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/bikesharing_dashboard/bikesharing_dashboard.py&requirements=panel-graphic-walker%5Bkernel%5D%3E%3D0.4.0%0Afastparquet) [![Static Badge](https://img.shields.io/badge/source-code-blue)](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/bikesharing_dashboard/bikesharing_dashboard.py)

![Bike Sharing Dashboard](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/bikesharing_dashboard/bikesharing_dashboard.png)

### Earthquake Dashboard

[![py.cafe](https://py.cafe/badge.svg)](https://py.cafe/snippet/panel/v1#code=https%3A//raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/earthquake_dashboard/earthquake_dashboard.py&requirements=panel-graphic-walker%5Bkernel%5D%3E%3D0.4.0%0Afastparquet) [![Static Badge](https://img.shields.io/badge/source-code-blue)](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/earthquake_dashboard/earthquake_dashboard.py)

![Earthquake Dashboard](https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/earthquake_dashboard/earthquake_dashboard.png)

## API

### Parameters

#### Core

- `object` (DataFrame): The data for exploration. Please note that if you update the `object`, the existing chart(s) will not be deleted, and you will have to create a new one manually to use the new dataset.
- `field_specs` (list): Optional specification of fields (columns).
- `spec` (str, dict, list): Optional chart specification as URL, JSON, dict, or list. Can be generated via the `export` method.
- `kernel_computation` (bool): Optional. If True, the computations will take place on the server or in the Jupyter kernel instead of the client to scale to larger datasets. The 'chart' renderer will only work with client side rendering. Default is False.

#### Renderer

- `renderer` (str): How to display the data. One of 'explorer' (default), 'profiler', 'viewer', or 'chart'. These correspond to `GraphicWalker`, `TableWalker`, `GraphicRenderer`, and `PureRender` in the `graphic-walker` React library.
- `container_height` (str): The height of a single chart in the `viewer` or `chart` renderer. For example, '500px' (pixels) or '30vh' (viewport height).
- `hide_profiling` (bool): Whether to hide the profiling part of the 'profiler' renderer. Default is False. Does not apply to other renderers.
- `index` (int | list): Optional index or indices to display. Default is None (all). Only applicable for the `viewer` or `chart` renderer.
- `page_size` (int): The number of rows per page in the table. Only applicable for the `profiler` renderer.
- `tab` ('data' | 'vis'): Set the active tab to 'data' or 'vis' (default). Only applicable for the `explorer` renderer. Not bi-directionally synced.

#### Style

- `appearance` (str): Optional dark mode preference: 'light', 'dark', or 'media'. If not provided, the appearance is derived from `pn.config.theme`.
- `theme_key` (str): Optional chart theme: 'g2' (default), 'streamlit', or 'vega'. If using the [`FastListTemplate`](https://panel.holoviz.org/reference/templates/FastListTemplate.html), try combining the `theme_key` 'g2' with the `accent` color <div style="display:inline;background-color:#5B8FF9;color:white;padding:0 5px;border-radius:3px;">#5B8FF9</div>, or 'streamlit' and <div style="display:inline;background-color:#ff4a4a;color:white;padding:0 5px;border-radius:3px;">#ff4a4a</div>, or 'vega' and <div style="display:inline;background-color:#4c78a8;color:white;padding:0 5px;border-radius:3px;">#4c78a8</div>.

#### Other

- `config` (dict): Optional additional configuration for Graphic Walker. For example `{"i18nLang": "ja-JP"}`. See the [Graphic Walker API](https://github.com/Kanaries/graphic-walker#api) for more details.

### Methods

#### Clone

- `clone`: Clones the `GraphicWalker`. Takes additional keyword arguments. Example: `walker.clone(renderer='profiler', index=1)`.
- `chart`: Clones the `GraphicWalker` and sets `renderer='chart'`. Example: `walker.chart(0)`.
- `explorer`: Clones the `GraphicWalker` and sets `renderer='explorer'`. Example: `walker.explorer(width=400)`.
- `profiler`: Clones the `GraphicWalker` and sets `renderer='profiler'`. Example: `walker.profiler(width=400)`.
- `viewer`: Clones the `GraphicWalker` and sets `renderer='viewer'`. Example: `walker.viewer(width=400)`.

#### Export and Save Methods

- `export_chart`: Returns chart(s) from the frontend exported as either Vega specifications or SVG strings.
- `save_chart`: Saves chart(s) from the frontend exported as either Vega specifications or SVG strings.
- `export_controls`: Returns a UI component to export the charts(s) and interactively set `scope`, `mode`, and `timeout` parameters. The `value` parameter will hold the exported spec.
- `save_controls`: Returns a UI component to export and save the chart(s) acting much like `export_controls`.

#### Other Methods

- `calculated_field_specs`: Returns a list of *fields* calculated from the `object`. This is a great starting point if you want to provide custom `field_specs`.

## Vision

Our dream is that this package is super simple to use and supports your use cases:

- Great documentation, including examples.
- Supports your preferred data backend, including Pandas, Polars, and DuckDB.
- Supports persisting and reusing Graphic Walker specifications.
- Scales to even the largest datasets, only limited by your server, cluster, or database.

## Supported Backends

| Name | `kernel_computation=False` | `kernel_computation=True` | Comment |
| ---- | - | - | - |
| Pandas | ✅ | ✅ | |
| Polars | ✅ | ✅ | |
| Dask | ✅ | ❌ | Not supported by Pygwalker |
| DuckDB Relation | ✅ | ❌ | Not supported by Pygwalker |
| Pygwalker Database Connector | ❌ | ❌ | [Not supported by Narwhals](https://github.com/narwhals-dev/narwhals/issues/1289) |

## ❤️ Contributions

Contributions and co-maintainers are very welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/panel-extensions/panel-graphic-walker). Check out the [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) for more information.
