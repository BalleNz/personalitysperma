import sys
from logging.config import dictConfig


def configure_logging():
    """Настройка логирования"""
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "routers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            },
        },
        "root": {
            "level": "INFO",
            "routers": ["console"],
        },
        "loggers": {
            "src": {
                "level": "INFO",
                "propagate": True
            },
            "bot": {
                "level": "INFO",
                "propagate": True
            }
        }
    })
