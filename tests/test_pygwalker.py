import pandas as pd
import pytest
from panel_gwalker import GraphicWalker

@pytest.fixture
def data():
    return pd.DataFrame({'a': [1, 2, 3]})

def test_constructor(data):
    gwalker = GraphicWalker(object=data)
    assert gwalker.object is data
    assert not gwalker.fields
    assert not gwalker.config

def test_process_parameter_change(data):
    gwalker = GraphicWalker(object=data)
    params={"object": gwalker.object, "fields": gwalker.fields, "config": gwalker.config}
    
    result = gwalker._process_param_change(params)
    assert params["fields"]
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
    params={"object": gwalker.object, "fields": gwalker.fields, "config": gwalker.config}
    
    result = gwalker._process_param_change(params)
    assert params["fields"] is fields
    assert not params["config"]

def test_process_parameter_change_with_config(data):
    config = {
    "appearance": "dark"
    }
    gwalker = GraphicWalker(object=data, config=config)
    params={"object": gwalker.object, "fields": gwalker.fields, "config": gwalker.config}
    
    result = gwalker._process_param_change(params)
    assert params["fields"]
    assert params["config"] is config

