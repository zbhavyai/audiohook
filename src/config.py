import importlib.metadata
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# get scm version
try:
    VERSION = importlib.metadata.version("audiohook")
except importlib.metadata.PackageNotFoundError:
    VERSION = "0.0.0-dev"


# configure output and log directories
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "output"
LOG_DIR = BASE_DIR.parent / "logs"
LOG_FILE = LOG_DIR / "script.log"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


def configure_logging() -> None:
    """
    Configures logging for the application.
    """

    log_level: int = logging.INFO
    log_file: Path = LOG_FILE
    log_file_max_size: int = 25 * 1024 * 1024
    log_file_backup_count: int = 7
    log_format: str = "%(asctime)s %(levelname)-7s [%(name)s] (%(threadName)s) %(message)s"

    log_handlers: list[logging.Handler] = [
        # logging.StreamHandler(),
        RotatingFileHandler(log_file, maxBytes=log_file_max_size, backupCount=log_file_backup_count),
    ]

    logging.basicConfig(level=log_level, format=log_format, handlers=log_handlers)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with the given name.
    """
    return logging.getLogger(name)


configure_logging()
