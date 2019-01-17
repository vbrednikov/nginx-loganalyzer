#!/usr/bin/env python
import datetime
import re
import unittest

from nginx_loganalyzer import LogFileTuple
from nginx_loganalyzer import get_latest_filename


class TestReaddir(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pattern = re.compile(r'^bbb.(?P<mm>\d\d)(?P<dd>\d\d)-(?P<yyyy>\d\d\d\d)(?P<ext>\.gz)?$')

    def test_get_latest_filename_plain(self):
        files = (filename for filename in [
            '.',
            '',
            None,
            'bbb.1229-2001',
            'bbb.0102-2002',
            'aaa.0101-2003',
            ])
        self.assertEqual(get_latest_filename(self.pattern, files),
                         LogFileTuple('./bbb.0102-2002', None, datetime.date(2002, 1, 2)))

    def test_get_latest_filename_mixed_gz(self):
        files = (filename for filename in [
            'bbb.0102-2002.gz',
            'bbb.0103-2002',

            ])
        self.assertEqual(get_latest_filename(self.pattern, files, '/path/to/dir'),
                         LogFileTuple('/path/to/dir/bbb.0103-2002', None, datetime.date(2002, 1, 3)))

    def test_get_latest_filename_mixed_plain(self):
        files = (filename for filename in [
            'bbb.0502-2001',
            'bbb.0103-2002.gz',

            ])
        self.assertEqual(get_latest_filename(self.pattern, files, '/'),
                         LogFileTuple('/bbb.0103-2002.gz', '.gz', datetime.date(2002, 1, 3)))

    def test_get_latest_filename_mixed_bz_gz(self):
        files = (filename for filename in [
            'bbb.0502-2003.bz2',
            'bbb.0103-2002.gz',
            ])
        self.assertEqual(get_latest_filename(self.pattern, files),
                         LogFileTuple('./bbb.0103-2002.gz', '.gz', datetime.date(2002, 1, 3)))


if __name__ == '__main__':
    unittest.main()
