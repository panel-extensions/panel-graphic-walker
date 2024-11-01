import numpy as np
import pandas as pd
import pytest
from param.parameterized import Event

from panel_gwalker import GraphicWalker
from panel_gwalker._utils import _raw_fields


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
