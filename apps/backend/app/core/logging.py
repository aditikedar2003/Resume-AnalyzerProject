# app/core/logging.py
import logging
import coloredlogs

def setup_logging() -> None:
    fmt = "%(asctime)s %(levelname)s %(message)s"
    coloredlogs.install(fmt=fmt)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
