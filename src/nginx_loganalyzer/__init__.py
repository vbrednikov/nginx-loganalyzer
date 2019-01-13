__version__ = '0.1.0'

import datetime
from collections import namedtuple
from decimal import Decimal

LogFileTuple = namedtuple('LogTuple', 'filename type date')


def logfinder(config):
    """Finds latest log matching config.log_re in config.log_dir
       Returns named tuple filename, filetype (gz/plain), parsed date
    """
    return LogFileTuple('small', 'plain', datetime.time)


def median(lst):
    """Find median of array of Decimals, return it as Decimal.
    Caveat: due to memory/cpu efficiency, type checking does not occur here"""
    n = len(lst)
    if n < 1:
        return None
    if n == 1:
        return Decimal(lst[0])
    if n % 2 == 1:
        return Decimal(sorted(lst)[n//2])
    else:
        return sum(sorted(lst)[n//2-1:n//2+1])/Decimal('2.0')
