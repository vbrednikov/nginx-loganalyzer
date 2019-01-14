# import datetime
import re
import unittest

# from nginx_loganalyzer import LogFileTuple
# from nginx_loganalyzer.log_parse import LogProc
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


# class TestLogProc(unittest.TestCase):
#    def setUp(self):
#        class SimpleLog(LogProc):
#            def set_regexp(self, log_regexp):
#                self.log_regexp = log_regexp

#            def parse_line(self, line):
#                res = parse_line_regexp(line, self.log_regexp, self.fields)
#                if not res:
#                    return None

#        log_tuple = LogFileTuple('test', 'plain', datetime.time)
#        self.log_proc = SimpleLog(log_tuple)
#        self.log_proc.set_regexp(re.compile(r'line[12]'))
#        self.gen = (x for x in ['line1', 'line2', 'line3'])

#    def test_simple_log(self):
#        self.log_proc.parse_log(log_gen=self.gen)
#        self.assertEqual(self.log_proc.processed, 3)


if __name__ == '__main__':
    unittest.main()
