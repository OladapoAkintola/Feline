import functools
import inspect
import time

from ._log import BaseLogger, INFO, WARNING, ERROR, CRITICAL, DEBUG



class MethodLogger(BaseLogger):
    def _make_decorator(self, level: int, enabled: bool = True):
        logger = self.logger
        time_tracking = self.time_tracking

        def decorator(meth):
            if not enabled:
                return meth

            @functools.wraps(meth)
            def wrapper(self, *args, **kwargs):
                start = time.perf_counter()
                logger.log(level, f"{self.__class__.__name__}.{meth.__name__} called")
                try:
                    result = meth(self, *args, **kwargs)
                    if time_tracking:
                        logger.log(level,
                                   f"{self.__class__.__name__}.{meth.__name__} finished in {time.perf_counter() - start:.4f}s")
                    return result
                except Exception as e:
                    if time_tracking:
                        logger.error(
                            f"{self.__class__.__name__}.{meth.__name__} raised after {time.perf_counter() - start:.4f}s")
                    logger.exception(f"Exception in {self.__class__.__name__}.{meth.__name__}: {e}")
                    raise

            return wrapper

        return decorator

    def debug(self, meth=None, *, enabled: bool = True):
        """

            :param meth: class method
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(DEBUG, enabled)
        return dec(meth) if meth is not None else dec

    def info(self, meth=None, *, enabled: bool = True):
        """

            :param meth: class method
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(INFO, enabled)
        return dec(meth) if meth is not None else dec

    def warning(self, meth=None, *, enabled: bool = True):
        """

            :param meth: class method
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """

        dec = self._make_decorator(WARNING, enabled)
        return dec(meth) if meth is not None else dec

    def error(self, meth=None, *, enabled: bool = True):
        """

            :param meth: class method
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """

        dec = self._make_decorator(ERROR, enabled)
        return dec(meth) if meth is not None else dec

    def critical(self, meth=None, *, enabled: bool = True):
        """

            :param meth: class method
            :param enabled: true by default, defines if decorator is enabled
            :return:
        """
        dec = self._make_decorator(CRITICAL, enabled)
        return dec(meth) if meth is not None else dec




class ClassLogger(MethodLogger):
    def __init__(self, skip_dunders:bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_dunders = skip_dunders


