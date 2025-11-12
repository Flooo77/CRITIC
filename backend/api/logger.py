import logging
import sys

logger = logging.getLogger("LoraMessagingApp")
logger.setLevel(logging.INFO)

if not logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(stream_handler)