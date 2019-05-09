
import json
import logging
import logging.config
import os

from config.config import LOGGING

if os.path.exists(LOGGING["config"]):
    with open(LOGGING["config"], "rt") as fin:
        config = json.load(fin)

    logging.config.dictConfig(config)
else:
    logging.basicConfig(
        filename=LOGGING["logfile"],
        filemode="a",
        format="[%(asctime)s:%(msecs)d] [%(levelname)s] %(module)s.%(funcName)s():%(lineno)d > %(message)s",
        datefmt='%H:%M:%S',
        level=logging.DEBUG
    )

_logger = logging.getLogger("__name__")
_logger.info(f"Logger {__name__} configured.")

# __init__.py
