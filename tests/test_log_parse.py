import datetime
import logging
import pprint
import re
import unittest
from decimal import Decimal

from nginx_loganalyzer import ConfigDict
from nginx_loganalyzer import LogFileTuple
from nginx_loganalyzer.log_parse import LogProc
from nginx_loganalyzer.log_parse import LogReqtimeStat
from nginx_loganalyzer.log_parse import parse_line_regexp
from nginx_loganalyzer.log_regexp import LogReCollection


class TestParseLogRegexp(unittest.TestCase):

    def test_simple_regexp(self):
        line = 'ivan rodil devchonku'
        fields = 'subject name'.split()
        regexp = re.compile(r'(?P<name>\S+) (?:\S+) (?P<subject>\S+)')
        self.assertEqual(parse_line_regexp(line, regexp, fields), ('devchonku', 'ivan',))

    def test_simple_nomatch(self):
        line = 'ivan'
        fields = 'subject name'.split()
        regexp = re.compile(r'(?P<name>\S+) (?:\S+) (?P<subject>\S+)')
        self.assertIsNone(parse_line_regexp(line, regexp, fields))

    def test_lib_regexp(self):
        class TestFormat(LogReCollection):
            log_format = r'{remote_addr}\s+{time_local}'

        line = '127.0.0.2 [29/Jun/2017:03:50:26 +0300]'
        fields = ['time_local', 'remote_addr']
        regexp = TestFormat().compile(fields)

        self.assertEqual(parse_line_regexp(line, regexp, fields),
                         ('[29/Jun/2017:03:50:26 +0300]', '127.0.0.2',)
                         )


class TestLogProc(unittest.TestCase):
    def setUp(self):
        # inherit LogProc in a simple class
        class SimpleLog(LogProc):

            def set_fields(self, fields):
                self.fields = fields

            def parse_line(self, line):
                regexp = re.compile(r'^line(?P<id>[12])')
                res = parse_line_regexp(line, regexp, self.fields)
                self.total += 1
                if not res:
                    return None
                self.processed += 1
                return res

        log_tuple = LogFileTuple('test', 'plain', datetime.date.today())
        self.log_proc = SimpleLog(log_tuple)
        self.log_proc.set_fields(['id'])

    def test_simple_log(self):
        # just check that parse_log iterates over generator and sets total and processed variables
        gen = (x for x in ['line1', 'line2', 'line3', 'xxx'])

        self.log_proc.parse_log(log_gen=gen)
        self.assertEqual(self.log_proc.total, 4)
        self.assertEqual(self.log_proc.processed, 2)


class TestLogReqTimeStat(unittest.TestCase):

    def setUp(self):
        log_tuple = LogFileTuple('test', 'plain', datetime.date.today())
        config = ConfigDict([
                            ('threshold', 55),
                            ('report_size', 5),
                            ])
        self.parser = LogReqtimeStat(log_tuple, config)
        self.parser.set_regexp(re.compile(r'^(?P<request>\S+)\s+(?P<request_time>\d+\.\d+)$'))

    def tearDown(self):
        del(self.parser)

    def test_general_stat(self):
        # check that stats are calculated correctly
        gen = (r for r in ['r1 1.2',
                           'r2 1.5',
                           'r3 0.01',
                           'r3 0.02',
                           'r5 10.0',
                           'r3 1.6',
                           'r6 -',
                           'r5 9.99',
                           'r9 1.0',
                           'r10 2.0',
                           ])
        result = self.parser.parse_log(log_gen=gen)
        self.assertEqual(self.parser.total, 10)
        self.assertEqual(self.parser.processed, 9)
        logging.info(pprint.pprint(result))
        # the following numbers were verified by hand and guarantied to be correct
        self.assertEqual(result, [{'count': 2,
                                   'count_perc': 22.22,
                                   'time_avg': 9.99,
                                   'time_max': Decimal('10.0'),
                                   'time_med': 9.99,
                                   'time_perc': 73.17,
                                   'time_sum': Decimal('19.99'),
                                   'url': 'r5'},
                                  {'count': 1,
                                   'count_perc': 11.11,
                                   'time_avg': 2.0,
                                   'time_max': Decimal('2.0'),
                                   'time_med': 2.0,
                                   'time_perc': 7.32,
                                   'time_sum': Decimal('2.0'),
                                   'url': 'r10'},
                                  {'count': 3,
                                   'count_perc': 33.33,
                                   'time_avg': 0.54,
                                   'time_max': Decimal('1.6'),
                                   'time_med': 0.02,
                                   'time_perc': 5.97,
                                   'time_sum': Decimal('1.63'),
                                   'url': 'r3'},
                                  {'count': 1,
                                   'count_perc': 11.11,
                                   'time_avg': 1.5,
                                   'time_max': Decimal('1.5'),
                                   'time_med': 1.5,
                                   'time_perc': 5.49,
                                   'time_sum': Decimal('1.5'),
                                   'url': 'r2'},
                                  {'count': 1,
                                   'count_perc': 11.11,
                                   'time_avg': 1.2,
                                   'time_max': Decimal('1.2'),
                                   'time_med': 1.2,
                                   'time_perc': 4.39,
                                   'time_sum': Decimal('1.2'),
                                   'url': 'r1'}])

    def test_wrongline_stat(self):
        # check that stats are calculated correctly
        gen = (r for r in ['r1 1.2',
                           'r2 -',
                           'r3 -',
                           'r3 -',
                           'r5 -',
                           'r3 1.6',
                           'r6 -',
                           'r5 9.99',
                           'r9 1.0',
                           'r10 2.0',
                           ])
        self.assertIsNone(self.parser.parse_log(log_gen=gen))
        self.assertEqual(self.parser.total, 10)
        self.assertEqual(self.parser.processed, 5)

    def test_zero_stat(self):
        # check that stats are calculated correctly
        gen = (r for r in [])
        self.assertEqual(self.parser.parse_log(log_gen=gen), [])
        self.assertEqual(self.parser.total, 0)
        self.assertEqual(self.parser.processed, 0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
