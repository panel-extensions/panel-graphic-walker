# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

## 🧳 Prerequisites

- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Install [Pixi](https://pixi.sh/latest/#installation)

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Install for Development

To install for development you will need to create a new environment

Then run

```bash
git clone https://github.com/panel-extensions/panel-graphic-walker.git
cd panel-graphic-walker
```

You can run all tests with:

```bash
pixi run pre-commit-run
pixi run -e test-312 test
```

### Serve the Examples

```bash
panel serve $(find examples -name "*.py") --dev
```

### 🚢 Release a new package on Pypi

Releasing `panel-graphic-walker` is automated and is triggered in the CI on tags.
