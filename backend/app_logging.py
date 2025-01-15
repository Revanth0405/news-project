"""
To setup logging for our application
"""

import logging
import logging.config
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "app.log"),
            "formatter": "default",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "root.search_api": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "root.scraping": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


def setup_logging():
    """
    Setup logging with default config for the application
    """
    logging.config.dictConfig(LOGGING_CONFIG)
