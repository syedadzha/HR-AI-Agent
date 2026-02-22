import logging
import logging.config
import os

# Go up one directory from 'backend/' to the project root, then to 'logs'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": os.path.join(LOG_DIR, "backend.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "hr_policy_rag": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
    "root": {"level": "WARNING", "handlers": ["console"]},
}

def setup_logging():
    """Initializes logging for the application."""
    logging.config.dictConfig(LOGGING_CONFIG)
