from decimal import Decimal
import decimal
import gzip
from pprint import pprint
import re

import nginx_loganalyzer.parser

decimal.getcontext().prec = 2

class LogProc(object):
    fields = []

    def __init__(self, log_tuple, config):
        print log_tuple
        self.log_tuple = log_tuple
        self.log_regexp = re.compile('.*')
        self.config = config
        self.stat = {}
        self.result = ""

    def parse_line(self, line):
        """Parse the line with regexp, return tuple consisting of matches"""
        m = self.log_regexp.match(line)
        if m:
            return tuple(map(lambda x: m.group(x), self.fields))

    def readlines(self):
        """Opens and parses log described by namedtuple('LogTuple',
           'filename type date')"""
        opener = gzip.open if self.log_tuple.type == 'gz' else open
        with opener(self.log_tuple.filename) as log:
            total = processed = 0
            for line in log:
                parsed_line = self.parse_line(line)
                total += 1
                if parsed_line:
                    processed += 1
                    yield parsed_line
        self.result = "{} of {} lines processed".format(processed, total)

    def parse_log(self):
        for line in self.readlines():
            pass

        print self.result


class LogTimeStat(LogProc):
    fields = ('request', 'request_time',)

    def __init__(self, *args, **kwargs):
        super(LogTimeStat, self).__init__(*args, **kwargs)
        self.log_regexp = nginx_loganalyzer.parser.UIShort().compile(self.fields)


    def parse_log(self):
        stat_data = {}
        stat = []
        total_time = 0
        total_count = 0
        for line in self.readlines():
            if line[0] not in stat_data:
                #self.stat_hash[line[0]] = {'count': 1, 'time_max': , 'time_avg': 0, 'time_med': 0, 'time_perc': 0,   'time_sum': Decimal(0) }
                stat_data[line[0]] = [Decimal(line[1])]
            else:
                stat_data[line[0]].append(Decimal(line[1]))
        #pprint(stat_data)
        for url, data in stat_data.iteritems():
            time_sum = sum(data)
            count = len(data)
            total_time += time_sum
            total_count += count

            stat.append({
                'url': url,
                'count':  count,
                'time_max': max(data),
                'time_avg': time_sum/len(data),
                'time_sum': time_sum,
                })

        for i, data in enumerate(stat):
            stat[i].update({
                'count_perc': 100 * Decimal(data['count'])/total_count,
                'time_perc': 100 * Decimal(data['time_sum'])/total_time,
                })

        return stat
