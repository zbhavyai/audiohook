import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "output"
LOG_DIR = BASE_DIR.parent / "logs"
LOG_FILE = LOG_DIR / "script.log"
VERSION = "1.0.0"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)7s] %(module)8s (%(lineno)3d) %(funcName)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
    ],
)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with the given name.
    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: The logger object.
    """
    return logging.getLogger(name)
