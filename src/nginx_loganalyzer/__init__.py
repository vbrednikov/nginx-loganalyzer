__version__ = '0.1.0'

import datetime
import gzip
from collections import namedtuple

from nginx_loganalyzer.parser import UIShort

LogFileTuple = namedtuple('LogTuple', 'filename type date')
# LogRecordTuple = namedtuple('LogRecordTuple', 'url', 'request_time')

log_regexp = UIShort().compile(['request', 'request_time'])


def logfinder(config):
    """Finds latest log matching config.log_re in config.log_dir
       Returns named tuple filename, filetype (gz/plain), parsed date
    """
    return LogFileTuple('small', 'plain', datetime.time)
