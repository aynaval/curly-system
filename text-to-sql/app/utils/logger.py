import logging
import sys
from .config_loader import config


def setup_logger():
    logger = logging.getLogger('Agent Assist')
    log_level = config.get("logging_level", 'INFO')
    logger.setLevel(log_level)

    # Create a console handler and set its level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    # ch.setLevel(logger.DEBUG)

    # Create a formatter
    format_pattern = '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s'
    formatter = logging.Formatter(format_pattern)

    # Add the formatter to the handler
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger


logger = setup_logger()