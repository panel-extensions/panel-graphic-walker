"""Run this script to generate py.cafe links for the examples in this repository.

Based on https://py.cafe/docs/api#snippet-links-with-code-and-requirements.
"""

from pathlib import Path
from urllib.parse import quote

GH_USER = "panel-extensions"
GH_REPO = "panel-graphic-walker"
GH_PREFIX = "refs/heads/main/examples/"

BASE_REQUIREMENTS = ["panel-graphic-walker>=0.4.0"]
PARQUET_REQUIREMENTS = BASE_REQUIREMENTS + ["fastparquet"]
SERVER_REQUIREMENTS = ["panel-graphic-walker[kernel]>=0.4.0", "fastparquet"]


EXAMPLES = [
    ("reference/basic.py", BASE_REQUIREMENTS),
    ("reference/spec.py", BASE_REQUIREMENTS),
    ("reference/renderer.py", BASE_REQUIREMENTS),
    ("reference/kernel_computation.py", SERVER_REQUIREMENTS),
    ("reference_app/reference_app.py", SERVER_REQUIREMENTS),
    ("bikesharing_dashboard/bikesharing_dashboard.py", SERVER_REQUIREMENTS),
    ("earthquake_dashboard/earthquake_dashboard.py", SERVER_REQUIREMENTS),
]


def create_pycafe_url(file: str, requirements: list[str] = BASE_REQUIREMENTS):
    root_url = f"https://raw.githubusercontent.com/{GH_USER}/{GH_REPO}/{GH_PREFIX}"
    url = root_url + file
    code = quote(url)

    text = "\n".join(requirements)
    text = quote(text)

    url = f"https://py.cafe/snippet/panel/v1#code={code}&requirements={text}"
    return url


def create_source_code_url(file: str):
    return f"https://github.com/panel-extensions/panel-graphic-walker/blob/main/examples/{file}"


def create_example(file, pycafe_url: str, source_code_url: str):
    badge = f"""\
{file}
[![py.cafe](https://py.cafe/badge.svg)]({pycafe_url}) [![Static Badge](https://img.shields.io/badge/source-code-blue)]({source_code_url})
"""
    return badge


def check_file(file):
    path = Path("examples") / file
    if not path.exists():
        raise FileNotFoundError(f"File {file} does not exist.")


def create_badges():
    for file, requirements in EXAMPLES:
        check_file(file)
        pycafe_url = create_pycafe_url(file, requirements)
        source_code_url = create_source_code_url(file)
        badges = create_example(file, pycafe_url, source_code_url)
        print(badges)


if __name__ == "__main__":
    create_badges()
