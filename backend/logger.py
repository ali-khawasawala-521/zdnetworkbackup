import os
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER_PATH = os.path.join(BASE_DIR, "logs/request.log")

# Set up logger
os.makedirs(os.path.dirname(LOGGER_PATH), exist_ok=True)
logger = logging.getLogger("backup_logger")
logger.setLevel(logging.INFO)

# Rotating handler (5MB per file, 3 backups)
handler = RotatingFileHandler(LOGGER_PATH, maxBytes=5_000_000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.handlers:
    logger.addHandler(handler)
