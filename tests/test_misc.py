#!/usr/bin/env python
import datetime
import os
import re
import shutil
import tempfile
import unittest

from nginx_loganalyzer import LogFileTuple
from nginx_loganalyzer import get_latest_filename
from nginx_loganalyzer import setup_reports


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


class TestSetupReports(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_existing_reports_dir(self):
        rep_dir_name = os.path.join(self.tmp_dir, 'reports')
        os.mkdir(rep_dir_name)
        self.assertTrue(setup_reports(rep_dir_name))
        self.assertTrue(os.path.exists(os.path.join(rep_dir_name, 'jquery.tablesorter.min.js')))

    def test_new_reports_dir(self):
        rep_dir_name = os.path.join(self.tmp_dir, 'reports')
        self.assertTrue(setup_reports(rep_dir_name))
        self.assertTrue(os.path.exists(os.path.join(rep_dir_name, 'jquery.tablesorter.min.js')))


if __name__ == '__main__':
    unittest.main()
