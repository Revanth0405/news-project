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
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "werkzeug": {  # Disable Werkzeug logs or control its level
            "handlers": ["console"],
            "level": "WARNING",  # Only log WARNING and above for Werkzeug
            "propagate": False,
        },
        "flask": {  # Control Flask logs separately if needed
            "handlers": ["console"],
            "level": "WARNING",  # Log only warnings and errors
            "propagate": False,
        },
    },
}


def get_logger(name: str = __name__):
    """
    Setup logging with default config for the application
    """
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)

