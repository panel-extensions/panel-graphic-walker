try:
    import pyodide
    IS_RUNNING_IN_PYODIDE=True
except ImportError:
    IS_RUNNING_IN_PYODIDE=False
