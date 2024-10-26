import pandas as pd
import numpy as np
import pytest
from panel_gwalker import GraphicWalker

@pytest.fixture
def data():
    return pd.DataFrame({'a': [1, 2, 3]})

def _get_params(gwalker):
    return {"object": gwalker.object, "fields": gwalker.fields, "appearance": gwalker.appearance, "config": gwalker.config}

def test_constructor(data):
    gwalker = GraphicWalker(object=data)
    assert gwalker.object is data
    assert not gwalker.fields
    assert not gwalker.config
    assert not gwalker.appearance

def test_process_parameter_change(data):
    gwalker = GraphicWalker(object=data)
    params=_get_params(gwalker)
    
    result = gwalker._process_param_change(params)
    assert params["fields"]
    assert params["appearance"]==gwalker._THEME_CONFIG["default"]
    assert not params["config"]

def test_process_parameter_change_with_fields(data):
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
    assert params["appearance"]==gwalker._THEME_CONFIG["default"]
    assert not params["config"]

def test_process_parameter_change_with_config(data):
    config = {
        "a": "b"
    }
    gwalker = GraphicWalker(object=data, config=config)
    params=_get_params(gwalker)
    
    result = gwalker._process_param_change(params)
    assert params["fields"]
    assert params["appearance"]==gwalker._THEME_CONFIG["default"]
    assert params["config"] is config

def test_process_parameter_change_with_appearance(data):
    appearance="dark"
    gwalker = GraphicWalker(object=data, appearance=appearance)
    params=_get_params(gwalker)
    result = gwalker._process_param_change(params)
    assert result["appearance"]==appearance

