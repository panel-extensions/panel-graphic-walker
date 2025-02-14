from pathlib import Path

import pytest

from panel.io.mime_render import exec_with_return

EXAMPLE_APP_PATHS = list(Path("examples").rglob("*.py"))


@pytest.mark.parametrize("path", EXAMPLE_APP_PATHS)
def test_apps(path):
    exec_with_return(path.read_text(encoding='utf-8'))
