import pytest

from panel_gwalker._gwalker import get_data_parser


def test_get_data_parser(data):
    if str(type(data)) == "<class 'dask_expr._collection.DataFrame'>":
        pytest.xfail("Dask DataFrame is not supported yet")
    assert get_data_parser(data, [], False, False, {})
