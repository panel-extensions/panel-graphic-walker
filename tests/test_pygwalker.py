import pytest

from panel_gwalker._gwalker import get_data_parser


def test_get_data_parser(data):
    assert get_data_parser(data, [], False, False, {})
