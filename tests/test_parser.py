import re
import unittest

from nginx_loganalyzer.log_regexp import LogReCollection
from nginx_loganalyzer.log_regexp import UIShort


class TestUIShort(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_line = '''1.194.135.240 -  - [29/Jun/2017:03:50:26 +0300] "GET /api/v2/group/7820986/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28 HTTP/1.1" 200 110 "-" "python-requests/2.13.0" "-" "1498697426-3979856266-4708-9752842" "8a7741a54297568b" 0.068'''  # noqa: E501
        cls.ui_short = UIShort()

    def test_ui_short_compiles(self):
        ui_short_re = self.ui_short.compile()
        self.assertIsInstance(ui_short_re, type(re.compile('.')))

    def test_ui_short_matches(self):
        self.assertRegexpMatches(self.test_line, self.ui_short.compile())

    def test_ui_short_captures(self):
        result = self.ui_short.compile('request time_local request_time http_referer'.split())\
            .match(self.test_line)
        self.assertEqual(result.group('time_local'), '[29/Jun/2017:03:50:26 +0300]')
        self.assertEqual(result.group('request'), '/api/v2/group/7820986/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28')  # noqa: E501
        self.assertEqual(result.group('request_time'), '0.068')
        self.assertEqual(result.group('http_referer'), '-')


class TestLogReCollection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reglib = LogReCollection()

    def test_prepare_regexps(self):
        # be sure that only remote_user uses named capture
        r = self.reglib._prepare_regexps(['remote_user'])
        for field, value in self.reglib.lib():
            assert r[field].startswith('(?P<remote_user>'
                                       if field == 'remote_user' else '(?:')

    def test_remote_user(self):
        self.assertRegexpMatches('0xdead-beaf11', self.reglib.item('remote_user'))

    def test_remote_user_empty(self):
        self.assertRegexpMatches('-', self.reglib.item('remote_user'))

    def test_remote_addr(self):
        self.assertRegexpMatches('127.0.0.1', self.reglib.item('remote_addr'))

    def test_fail_remote_addr(self):
        self.assertNotRegexpMatches('127.0.259.1', self.reglib.item('remote_addr'))

    def test_x_realip(self):
        self.assertRegexpMatches('-', self.reglib.item('http_x_real_ip'))

    def test_time_local(self):
        self.assertRegexpMatches('[29/Jun/2017:03:50:24 +0300]', self.reglib.item('time_local'))

    def test_time_local2(self):
        self.assertRegexpMatches('[29/Jun/2017:23:59:59 -0000]', self.reglib.item('time_local'))

    def test_request_time(self):
        self.assertRegexpMatches('0.000', self.reglib.item('request_time'))

    def test_request_time2(self):
        self.assertRegexpMatches('50.100', self.reglib.item('request_time'))

    def test_x_rb_user(self):
        self.assertRegexpMatches('"-"', self.reglib.item('http_x_rb_user'))

    def test_x_rb_user_spaces(self):
        self.assertRegexpMatches('Vassily Poupkin', self.reglib.item('http_x_rb_user'))
