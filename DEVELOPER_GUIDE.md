# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

## 🧳 Prerequisites

- A working [Python](https://www.python.org/downloads/) environment.
- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- [uv](https://astral.sh/)

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Install for Development

To install for development you will need to create a new environment

Then run

```bash
git clone https://github.com/awesome-panel/panel-graphic-walker.git
cd panel-graphic-walker
uv venv
source .venv/bin/activate # linux
uv pip install -e .[examples,dev,test]
pre-commit install
```

You can run all tests via

```bash
pre-commit run --all
pytest tests
```

### Serve the Examples

```bash
panel serve $(find examples -name "*.py") --dev
```

### 🚢 Release a new package on Pypi

Update the version in the [pyproject.toml](pyproject.toml).

Then run all tests as described above

Then you can build

```bash
uv build
```

and publish by setting your [`UV_PUBLISH_TOKEN`](https://docs.astral.sh/uv/guides/publish/#publishing-your-package) and running

```bash
uv publish
```

to publish the package 📦.
