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


def parse_line(line, regexp):
    """Parse the line with regexp, return tuple consisting of matches"""
    m = regexp.match(line)
    # print "match %s against %s" % (line, regexp.pattern)
    if m:
        return m


def readlines(log_tuple, log_regexp):
    """Opens and parses log described by namedtuple('LogTuple',
       'filename type date')"""
    opener = gzip.open if log_tuple.type == 'gz' else open
    with opener(log_tuple.filename) as log:
        total = processed = 0
        for line in log:
            parsed_line = parse_line(line, log_regexp)
            total += 1
            if parsed_line:
                processed += 1
                yield parsed_line
        print "{} of {} lines processed".format(processed, total)


def parse_log(log_tuple, config, log_regexp=log_regexp):
    for line in readlines(log_tuple, log_regexp):
        pass
        # print line
