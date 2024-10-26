import numpy as np
import pandas as pd
import pytest

from panel_gwalker import GraphicWalker


@pytest.fixture
def data():
    return pd.DataFrame({'a': [1, 2, 3]})

@pytest.fixture
def default_appearance():
    return "light"

def _get_params(gwalker):
    return {"object": gwalker.object, "fields": gwalker.fields, "appearance": gwalker.appearance, "config": gwalker.config}

def test_constructor(data, default_appearance):
    gwalker = GraphicWalker(object=data)
    assert gwalker.object is data
    assert not gwalker.fields
    assert not gwalker.config
    assert gwalker.appearance==default_appearance

def test_process_parameter_change(data, default_appearance):
    gwalker = GraphicWalker(object=data)
    params=_get_params(gwalker)

    result = gwalker._process_param_change(params)
    assert params["fields"]
    assert params["appearance"]==default_appearance
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
    params=_get_params(gwalker)

    result = gwalker._process_param_change(params)
    assert params["fields"] is fields
    assert params["appearance"]==default_appearance
    assert not params["config"]

def test_process_parameter_change_with_config(data, default_appearance):
    config = {
        "a": "b"
    }
    gwalker = GraphicWalker(object=data, config=config)
    params=_get_params(gwalker)

    result = gwalker._process_param_change(params)
    assert params["fields"]
    assert params["appearance"]==default_appearance
    assert params["config"] is config

def test_process_parameter_change_with_appearance(data):
    appearance="dark"
    gwalker = GraphicWalker(object=data, appearance=appearance)
    params=_get_params(gwalker)
    result = gwalker._process_param_change(params)
    assert result["appearance"]==appearance
