import functools
import time
from ._log import BaseLogger, INFO, WARNING, ERROR, CRITICAL, DEBUG


class FuncLogger(BaseLogger):

    def _make_decorator(self, level: int, enabled: bool = True):
        def decorator(func):
            if not enabled:
                return func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                self.logger.log(level, f"{func.__name__} called")
                try:
                    result = func(*args, **kwargs)
                    if self.time_tracking:
                        self.logger.log(level, f"{func.__name__} finished in {time.perf_counter() - start:.4f}s")
                    return result
                except Exception as e:
                    if self.time_tracking:
                        self.logger.error(f"{func.__name__} raised after {time.perf_counter() - start:.4f}s")
                    self.logger.exception(f"Exception in {func.__name__}: {e}")
                    raise

            return wrapper

        return decorator

    def debug(self, func=None, *, enabled: bool = True):
        """

            :param func: function to be decorated
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(DEBUG, enabled)
        return dec(func) if func is not None else dec

    def info(self, func=None, *, enabled: bool = True):
        """

            :param func: function to be decorated
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(INFO, enabled)
        return dec(func) if func is not None else dec

    def warning(self, func=None, *, enabled: bool = True):
        """

            :param func: function to be decorated
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(WARNING, enabled)
        return dec(func) if func is not None else dec

    def error(self, func=None, *, enabled: bool = True):
        """

            :param func: function to be decorated
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(ERROR, enabled)
        return dec(func) if func is not None else dec

    def critical(self, func=None, *, enabled: bool = True):
        """

            :param func: function to be decorated
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(CRITICAL, enabled)
        return dec(func) if func is not None else dec





