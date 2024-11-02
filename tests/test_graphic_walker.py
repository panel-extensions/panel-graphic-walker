import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from param.parameterized import Event

from panel_gwalker import GraphicWalker
from panel_gwalker._utils import _raw_fields, process_spec


@pytest.fixture
def data():
    return pd.DataFrame({"a": [1, 2, 3]})


@pytest.fixture
def default_appearance():
    return "light"


def _get_params(gwalker):
    return {
        "object": gwalker.object,
        "fields": gwalker.fields,
        "appearance": gwalker.appearance,
        "config": gwalker.config,
        "server_computation": gwalker.server_computation,
    }


def test_constructor(data, default_appearance):
    gwalker = GraphicWalker(object=data)
    assert gwalker.object is data
    assert not gwalker.fields
    assert not gwalker.config
    assert gwalker.appearance == default_appearance


def test_process_parameter_change(data, default_appearance):
    gwalker = GraphicWalker(object=data)
    params = _get_params(gwalker)

    result = gwalker._process_param_change(params)
    assert params["fields"]==gwalker.calculated_fields()
    assert params["appearance"] == default_appearance
    assert not params["config"]


def test_process_parameter_change_with_fields(data, default_appearance):
    fields = fields = [
        {
            "fid": "t_county",
            "name": "t_county",
            "semanticType": "nominal",
            "analyticType": "dimension",
        },
    ]
    gwalker = GraphicWalker(object=data, fields=fields)
    params = _get_params(gwalker)

    result = gwalker._process_param_change(params)
    assert params["fields"] is fields
    assert params["appearance"] == default_appearance
    assert not params["config"]


def test_process_parameter_change_with_config(data, default_appearance):
    config = {"a": "b"}
    gwalker = GraphicWalker(object=data, config=config)
    params = _get_params(gwalker)

    result = gwalker._process_param_change(params)
    assert params["fields"]
    assert params["appearance"] == default_appearance
    assert params["config"] is config


def test_process_parameter_change_with_appearance(data):
    appearance = "dark"
    gwalker = GraphicWalker(object=data, appearance=appearance)
    params = _get_params(gwalker)
    result = gwalker._process_param_change(params)
    assert result["appearance"] == appearance

def test_process_parameter_change_resetting_server_computationt(data):
    gwalker = GraphicWalker(object=data, server_computation=True)
    gwalker.server_computation = False
    params = {"server_computation": gwalker.server_computation}
    result = gwalker._process_param_change(params)
    assert result["object"] is gwalker.object


def test_server_computation(data):
    gwalker = GraphicWalker(object=data, server_computation=True)
    gwalker.param.server_computation.constant=False
    gwalker.server_computation=True

    params = _get_params(gwalker)
    assert "object" not in gwalker._process_param_change(params)

    gwalker.server_computation=False
    params = _get_params(gwalker)
    assert "object" in gwalker._process_param_change(params)


def test_calculated_fields(data):
     gwalker = GraphicWalker(object=data)
     assert gwalker.calculated_fields() == _raw_fields(data)

def test_process_spec(tmp_path: Path):
    """If the spec is a string, it can be either a file path, a url path, or a JSON string."""

    # Test with a JSON string
    json_string = '{"key": "value"}'
    result = process_spec(json_string)
    assert result == {"key": "value"}, f"Expected JSON object, got {result}"

    # Test with a URL (assuming we are just checking format, not accessing the URL)
    url = "http://example.com/data.json"
    result = process_spec(url)
    assert result == url, f"Expected URL, got {result}"

    # Test with a file path by creating a temporary JSON file
    json_data = {"file_key": "file_value"}
    tmp_file = tmp_path/"data.json"

    with open(tmp_file) as file:
        json.dump(json_data, file)

    result = process_spec(tmp_file)
    assert result == json_data, f"Expected JSON content from file, got {result}"


    # Test with a file path string
    tmp_file_str = str(tmp_file.absolute())
    result = process_spec(tmp_file_str)
    assert result == json_data, f"Expected JSON content from file, got {result}"
