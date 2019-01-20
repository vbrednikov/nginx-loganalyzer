#!/usr/bin/env python
import datetime
import os
import re
import shutil
import tempfile
import unittest

from nginx_loganalyzer import ConfigDict
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


class TestLogFileTuple(unittest.TestCase):
    def test_logfile_tuple(self):
        lft = LogFileTuple('name', 'gz', datetime.date(2017, 12, 31))
        self.assertEqual(lft.filename, 'name')
        self.assertEqual(lft.type, 'gz')
        self.assertEqual(lft.date.strftime('%m/%d/%Y'), '12/31/2017')


class TestConfigDict(unittest.TestCase):
    def setUp(self):
        self.config = ConfigDict({'a': 2, 'b': 3, 'd': 4, 'e': 9})

    def tearDown(self):
        del(self.config)

    def test_access_attr(self):
        self.assertEqual(self.config.a, 2)

    def test_access_non_existing_attr(self):
        with self.assertRaises(AttributeError):
            self.config.x

    def test_access_key(self):
        self.assertEqual(self.config['a'], 2)

    def test_update_attr(self):
        self.config.b = 5
        self.assertEqual(self.config.b, 5)

    def test_update_key(self):
        self.config['d'] = 8
        self.assertEqual(self.config.d, 8)

    def test_delete_key(self):
        del(self.config['e'])
        self.assertFalse(hasattr(self.config, 'e'))

    def test_delete_attr(self):
        del(self.config.e)
        self.assertFalse(hasattr(self.config, 'e'))

    def test_delete_non_existing_attr(self):
        with self.assertRaises(AttributeError):
            del(self.config.y)


if __name__ == '__main__':
    unittest.main()
