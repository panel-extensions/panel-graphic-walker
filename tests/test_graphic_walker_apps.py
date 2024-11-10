from pathlib import Path

import pytest

EXAMPLE_APP_PATHS = [str(path) for path in Path("examples").rglob("*.py")]


@pytest.mark.parametrize("path", EXAMPLE_APP_PATHS)
def test_apps(path):
    # Quick test that apps can run
    # Could be improved but I would like to keep theme relatively fast, i.e. without Playwrigth
    with open(path) as f:
        code = f.read()
        env = globals().copy()
        env["__file__"] = path
        try:
            exec(code, env)
        except:
            msg = f"Error running {path}"
            raise Exception(msg)
