# app/core/logger.py

"""
Application Logging Configuration
---------------------------------

This module configures centralized logging for the application.

Features:
- Structured logging format
- Separate log handlers
- Console + File logging support
- Different log levels
- Production-ready configuration

All modules should import logger from here:
    from app.core.logger import logger
"""
# app/core/logger.py
import logging
import logging.config
import os
from pathlib import Path



# Create logs directory automatically
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)



# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

   
    # Formatters
    "formatters": {
        "standard": {
            "format": (
                "%(asctime)s | %(levelname)s | "
                "%(name)s | %(message)s"
            )
        },
        "detailed": {
            "format": (
                "%(asctime)s | %(levelname)s | %(name)s | "
                "%(filename)s:%(lineno)d | %(message)s"
            )
        },
    },

   
    # Handlers
    "handlers": {

        # Console logs 
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        },

        # App logs
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "app.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5MB
            "backupCount": 5,
            "formatter": "detailed",
            "level": "INFO",
        },

        # Error logs
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "error.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "detailed",
            "level": "ERROR",
        },
    },


    # Root Logger
    "root": {
        "handlers": ["console", "file", "error_file"],
        "level": "INFO",
    },
}


logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("app")
