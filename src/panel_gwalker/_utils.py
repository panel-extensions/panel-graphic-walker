import logging
import sys

try:
    import pyodide
    IS_RUNNING_IN_PYODIDE=True
except ImportError:
    IS_RUNNING_IN_PYODIDE=False

FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def configure_logger(logger, format_=FORMAT, level=logging.INFO):
    logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setStream(sys.stdout)
    formatter = logging.Formatter(format_)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    logger.setLevel(level)
    logger.info("Logger successfully configured")
    return logger
