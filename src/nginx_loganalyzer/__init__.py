__version__ = '0.1.0'

import datetime
import os.path
import re
from collections import namedtuple
from decimal import Decimal

LogFileTuple = namedtuple('LogTuple', 'filename type date')


def get_latest_filename(pattern, filenames, dir='.'):
    """Returns tuple (filename, date, extension) for the latest filename from
    filenames generator matching the pattern.  The pattern must contain named
    groups "yyyy", "mm", "dd", "ext" in order to capture them"""
    if pattern.__class__ != '_sre.SRE_Pattern':
        pattern = re.compile(pattern)
    max_filedate = None
    max_file = None
    for filename in filenames:
        if filename is None:
            continue
        match = pattern.match(filename)
        if not match:
            continue
        filedate = datetime.date(int(match.group('yyyy')), int(match.group('mm')), int(match.group('dd')))
        if max_filedate is None or filedate > max_filedate:
            max_filedate = filedate
            max_file = LogFileTuple(os.path.join(dir, filename), match.group('ext'), filedate)
    return max_file


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
