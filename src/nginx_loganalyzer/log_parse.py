import gzip
import logging
from collections import defaultdict
from collections import namedtuple
from decimal import Decimal

import log_regexp

from nginx_loganalyzer import median


def parse_line_regexp(line, regexp, fields):
    """Given with regexp containing named capture groups, check the line
    against the regexp and return matches in the order specified by
    the "fields" argument (must be a list or tuple)"""
    m = regexp.match(line)
    if m:
        return tuple(map(lambda x: m.group(x), fields))
    return None


class LogProc(object):
    fields = []

    def __init__(self, log_tuple):
        self.log_tuple = log_tuple
        self.processed = 0
        self.total = 0

    def parse_line(self, line):
        return True

    def readlines(self):
        """Opens and parses log described by namedtuple('LogTuple',
           'filename type date')"""
        opener = gzip.open if self.log_tuple.type == 'gz' else open
        logging.info('readlines() for %s opened with %s' % (self.log_tuple.filename, opener))
        with opener(self.log_tuple.filename) as log:
            for line in log:
                yield(line)

    def parse_log(self, log_gen=None):
        logging.info('Enter parse_log')
        if log_gen is None:
            log_gen = self.readlines()
        logging.info("Using log_gen: %s" % log_gen)
        try:
            line = log_gen.next()
            while True:
                result = self.parse_line(line)
                line = log_gen.send(bool(result))
        except StopIteration:
            log_gen.close()


class LogReqtimeStat(LogProc):
    fields = ('request', 'request_time',)
    UrlReqTime = namedtuple('UrlReqTime', 'url request_time')

    def __init__(self, log_tuple, config):
        super(LogReqtimeStat, self).__init__(log_tuple)
        self.config = config
        self.log_regexp = log_regexp.UIShort().compile(self.fields)
        self.stat_data = defaultdict(dict)
        self.raw_data = defaultdict(list)
        self.total_time = 0
        self.total_count = 0
        self.threshold = 70
        if hasattr(self.config, 'threshold'):
            self.threshold = int(config.threshold)

    def set_regexp(self, log_regexp):
        self.log_regexp = log_regexp

    def parse_line(self, line):
        res = parse_line_regexp(line, self.log_regexp, self.fields)
        self.total += 1
        if not res:
            logging.info("Could not parse line: %s" % line.strip())
            return None
        self.processed += 1
        request_time = Decimal(res[1])
        self.total_time += request_time
        self.total_count += 1
        if res[0] not in self.stat_data:
            self.stat_data[res[0]] = {
                'url': res[0],
                'count': 1,
                'time_sum': request_time,
                'time_max': request_time,
                'time_avg': -1.0,
                'time_med': -1.0,
                'count_perc': -1.0,
                'time_perc': -1.0,
            }
            self.raw_data[res[0]].append(request_time)

        else:
            self.raw_data[res[0]].append(request_time)
            self.stat_data[res[0]]['count'] += 1
            self.stat_data[res[0]]['time_sum'] += request_time
            if request_time > self.stat_data[res[0]]['time_max']:
                self.stat_data[res[0]]['time_max'] = request_time
        return True

    def parse_log(self, *args, **kwargs):
        super(LogReqtimeStat, self).parse_log(*args, **kwargs)
        if self.total == 0:
            logging.info("Total zero came from the file")
            return []
        processed_percent = 100*(float(self.processed) / self.total)
        if processed_percent < self.threshold:
            logging.error("Parsed %s lines of %s (%s%%), but threshold is %s%%" %
                          (self.processed,
                           self.total,
                           round(processed_percent, 2),
                           self.threshold))
            return None
        logging.info("Parsed %s of total %s (%s%%) in %s" %
                     (self.processed, self.total, round(processed_percent, 2), self.log_tuple.filename))

        stat = []
        for url, url_data in sorted(self.stat_data.items(),
                                    key=lambda kv: kv[1]['time_sum'],
                                    reverse=True):
            url_data.update({
                'count_perc': round(100 * Decimal(url_data['count'])/self.total_count, 2),
                'time_perc': round(100 * Decimal(url_data['time_sum'])/self.total_time, 2),
                'time_med': round(median(self.raw_data[url]), 2),
                'time_avg': round(url_data['time_sum']/url_data['count'], 2)
                })
            stat.append(url_data)
            if len(stat) >= int(self.config.report_size):
                break

        return stat
