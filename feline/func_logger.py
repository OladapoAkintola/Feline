import functools
import logging
import time

from ._log import BaseLogger


class FuncLogger(BaseLogger):



    def _decorator(self, level, enabled:bool = True):
        def decorator(func):
            if not enabled:
                return func
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                self.logger.log(level, f"{func.__name__} Called")
                try:
                    result = func(*args, **kwargs)
                    duration = time.perf_counter() - start_time
                    if self.time_tracking:
                        self.logger.log(logging.INFO, f"{func.__name__} Finished in {duration:.4f} seconds")
                    return result

                except Exception as e:
                    duration = time.perf_counter() - start_time
                    if self.time_tracking:
                        self.logger.log(logging.ERROR, f"{func.__name__} Finished in {duration:.4f} seconds")
                    self.logger.exception(f"Exception in {func.__name__}: {e}")
                    raise

            return wrapper
        return decorator

    @property
    def debug(self, level: int = logging.DEBUG, enabled:bool = True):
        self._decorator(level, enabled)

    @property
    def info(self, level: int = logging.INFO, enabled:bool = True):
        self._decorator(level, enabled)

    @property
    def warning(self, level: int = logging.WARNING, enabled:bool = True):
        self._decorator(level, enabled)

    @property
    def error(self, level: int = logging.ERROR, enabled:bool = True):
        self._decorator(level, enabled)

    @property
    def critical(self, level: int = logging.CRITICAL, enabled:bool = True):
        self._decorator(level, enabled)



