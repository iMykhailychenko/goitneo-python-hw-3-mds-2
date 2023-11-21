import logging

import colorlog

# Configure the logger with colorlog
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(message)s",
        log_colors={"INFO": "green", "WARNING": "yellow", "ERROR": "red"},
    )
)
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
