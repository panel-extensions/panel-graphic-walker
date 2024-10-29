import param

_VALID_CLASSES = (
    "<class 'pandas.core.frame.DataFrame'>",
    "<class 'polars.dataframe.frame.DataFrame'>",
    "<class 'pygwalker.data_parsers.database_parser.Connector'>",
)

class TabularData(param.Parameter):
    def _validate(self, val):
        super()._validate(val=val)
        try:
            if str(val.__class__) in _VALID_CLASSES:
                return
        except:
            pass
        msg=f"A value of type '{type(val)}' is not valid"
        raise ValueError(msg)
