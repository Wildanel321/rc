import logging
import sys

class CustomFormatter(logging.Formatter):
    """Format logs as requested in specifications: [LEVEL] message"""
    def format(self, record):
        levelname = record.levelname
        msg = record.getMessage()
        return f"[{levelname}] {msg}"

def setup_logger(name: str = "rc_controller", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(numeric_level)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)

    return logger

logger = setup_logger()
