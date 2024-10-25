from panel_gwalker import GraphicWalker


def test_constructor():
    df = pd.DataFrame({'a': [1, 2, 3]})
    gwalker = GraphicWalker(object=df)
    assert gwalker.object is df
