from __future__ import annotations

import os
import sys

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

BASE_DIR = Path(__file__).parent
GREEN, RED, RESET = "\033[0;32m", "\033[0;31m", "\033[0m"


def compile_bundle():
    from panel.io.compile import compile_components, find_module_bundles

    print(f"{GREEN}[PANEL-GRAPHIC-WALKER]{RESET} Compile panel_gwalker bundle", flush=True)
    panel_dir = BASE_DIR / "panel"

    sys.path.insert(0, str(BASE_DIR / "src"))
    module_bundles = find_module_bundles('panel_gwalker')
    errors = 0
    for bundle, components in module_bundles.items():
        ret = compile_components(
            components,
            outfile=bundle,
        )
        if ret is None:
            errors += 1
        else:
            errors += ret
    if sys.platform != "win32":
        # npm can cause non-blocking stdout; so reset it just in case
        import fcntl

        flags = fcntl.fcntl(sys.stdout, fcntl.F_GETFL)
        fcntl.fcntl(sys.stdout, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)

    if not errors:
        print(f"{GREEN}[PANEL-GRAPHIC-WALKER]{RESET} Finished building bundle", flush=True)
    else:
        print(f"{RED}[PANEL-GRAPHIC-WALKER]{RESET} Failed building bundle", flush=True)
        sys.exit(1)


class BuildHook(BuildHookInterface):
    """The hatch build hook."""

    PLUGIN_NAME = "install"

    def initialize(self, version: str, build_data: dict[str, t.Any]) -> None:
        """Initialize the plugin."""
        if self.target_name not in ["wheel", "sdist"]:
            return

        compile_bundle()
