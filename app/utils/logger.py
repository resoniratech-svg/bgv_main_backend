import logging
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    handler = RotatingFileHandler(
        "bgv_service.log",
        maxBytes=1000000,
        backupCount=5
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)