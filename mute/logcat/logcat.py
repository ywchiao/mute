
from . import _logger

class LogCat:
    @staticmethod
    def dump_obj(obj):
        _logger.debug(f'Dump_Obj: {str(obj)}')

    @staticmethod
    def log(string):
        _logger.debug(string)

    @staticmethod
    def log_func(func):
        def wrapped_func(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
            signature = ', '.join(args_repr + kwargs_repr)

            _logger.info(f'{func.__qualname__}({signature})')

            return func(*args, **kwargs)

        return wrapped_func

# logcat.py
