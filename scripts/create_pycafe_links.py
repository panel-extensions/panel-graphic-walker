"""Run this script to generate py.cafe links for the examples in this repository.

Based on https://py.cafe/docs/api#snippet-links-with-code-and-requirements.
"""
from urllib.parse import quote

BASE_REQUIREMENTS = ["panel-graphic-walker"]

ROOT_URL = "https://raw.githubusercontent.com/panel-extensions/panel-graphic-walker/refs/heads/main/examples/"

EXAMPLES = [
    ("app_basic.py", BASE_REQUIREMENTS),
    ("app_demo.py", BASE_REQUIREMENTS + ["fastparquet"]),
]

def create_pycafe_url(file: str, requirements: list[str]=BASE_REQUIREMENTS):
    url = ROOT_URL + file
    code = quote(url)

    text = "\n".join(requirements)
    text = quote(text)

    url = f"https://py.cafe/snippet/panel/v1#code={code}&requirements={text}"
    return url

def create_urls():
    for file, requirements in EXAMPLES:
        url = create_pycafe_url(file, requirements)
        print(file, url)

if __name__=="__main__":
    create_urls()
