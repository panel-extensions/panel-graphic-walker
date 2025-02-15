# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

`panel-graphic-walker` is automatically built, tested and released on Github Actions. The setup heavily leverages `pixi`, though we recommend using it you can also set up your own virtual environment.

While `panel-graphic-walker` is shipped with a compiled JavaScript bundle, during development the JS compiled is compiled on the fly in the browser. If you do decide to compile it locally you either have to enable `--dev` mode in the Panel CLI or use pixi commands suffixed with -dev (e.g. `serve-dev`).

## 🧳 Prerequisites

- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Install [Pixi](https://pixi.sh/latest/#installation)

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Install for Development

To install for development you will have to clone the repository with git:

```bash
git clone https://github.com/panel-extensions/panel-graphic-walker.git
cd panel-graphic-walker
```

If you want to manage your own environment, including installations of `nodejs` and `esbuild` (e.g. using conda) set up your development environment with:

```bash
pip install -e .
```

We recommend developing with pixi, as that it was our CI system uses. Pixi manages distinct environments for testing, compiling, and building packages.

## Development

To list available tasks run:

```bash
pixi task list
```

One quick way to test your development work is to start a server running all example apps, which will automatically reload as you make changes to the GraphicWalker component:

```bash
pixi run serve-dev
```

This starts a development server, equivalent to passing the `--dev` flag to `panel serve`.

```bash
panel serve $(find examples -name "*.py") --dev
```

### Testing

To run the test suite locally you can run linting and unit tests with:

```bash
pixi run pre-commit-run
pixi run -e test-312 test
```

### 🚢 Release a new package on Pypi

Releasing `panel-graphic-walker` is automated and is triggered in the CI on tags.
