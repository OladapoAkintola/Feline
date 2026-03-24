from ._log import BaseLogger
from .func_logger import FuncLogger
from .class_logger import MethodLogger, ClassLogger


__all__ = [
    'BaseLogger', 'FuncLogger', 'ClassLogger', 'MethodLogger',
]
__author__ = 'Oladapo Akintola'
__version__ = '0.1.0'