import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


_LOGGERS: dict[str, logging.Logger] = {}

INFO = logging.INFO
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
WARNING = logging.WARNING
DEBUG = logging.DEBUG

def check_prod() -> bool:
    """
    Checks if app is still in development or production mode
    :return: True if app is not in development or production mode
    :rtype: bool
    """

    if getattr(sys, "frozen", False):
        return True
    return False

console_mode = check_prod()
def get_logger(
    name: str,
    level: int = INFO,
    filename: str = "app.log",
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 5,
    console: bool = not console_mode,
    log_dir: str | Path = "logs",
) -> logging.Logger:
    """
    Create or retrieve a configured logger.

    :param name: Logger name (e.g. "player", "storage", "ui")
    :param log_dir: Directory where logs are stored
    :param level: Logging level
    :param filename: Log file name
    :param max_bytes: Max size before rotation
    :param backup_count: Number of rotated files to keep
    :param console: Also log to stdout
    """

    if name in _LOGGERS:
        return _LOGGERS[name]

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # critical: prevents duplicate logs

    log_file = log_dir / filename

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    logger.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)

    _LOGGERS[name] = logger
    return logger


class BaseLogger:
    def __init__(
            self, name: str = __name__, time_tracking: bool = True, log_level: int = logging.INFO,
            filename: str = "app.log", max_bytes: int = 5 * 1024 * 1024,
            backup_count: int = 5, console: bool = not console_mode, log_dir: str | Path = "logs",
    ):
        """
        Base decorator class
        :param name: function name
        :param time_tracking: whether to track execution time, time would be tracked internally either way, this just specifies if it should be displayed. It won't be stored in log files
        :param log_level: default logging level
        :param filename: log file name
        :param max_bytes: maximum number of bytes to store in log file
        :param backup_count: how many times to store in log file
        :param console: whether to display in console
        :param log_dir: directory to store logs
        """
        self.time_tracking = time_tracking
        self.logger = get_logger(
            name, log_level, filename, max_bytes, backup_count, console,
            log_dir
        )

    def _make_decorator(self, level: int, enabled: bool = True):
        pass