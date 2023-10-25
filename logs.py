import logging
import logging.handlers
import os
import time


def setup_logger():
    """
    Set up a logger that writes to a file in a 'logs' directory.
    The file is named with the current timestamp to ensure uniqueness.
    A rotating file handler is used to keep the last 100 log files.

    Returns:
    logger: The logger.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("iafd_scraper")
    logger.setLevel(logging.ERROR)

    # Create a rotating file handler that keeps the last 100 log files
    handler = logging.handlers.RotatingFileHandler(
        filename=f'logs/{time.strftime("%Y%m%d-%H%M%S")}.log',
        maxBytes=10**6,  # 1MB
        backupCount=20,
    )
    handler.setLevel(logging.ERROR)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


logger = setup_logger()
