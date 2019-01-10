import tempfile
import unittest

from nginx_loganalyzer.cli import parse_args


class TestCmdLineArgs(unittest.TestCase):
    def setUp(self):
        self.config_file = tempfile.NamedTemporaryFile(mode='r')

    def test_parse_args_empty(self):
        args = parse_args([])
        self.assertTrue(args.config is None, 'config should be None by default'
                        ' when unspecified in the args')
        self.assertEqual(args.threshold, 66)

    def test_parse_args_config(self):
        args = parse_args(('--config %s --err-threshold 59' % self.config_file.name).split())
        self.assertEqual(args.config.name, self.config_file.name)
        self.assertEqual(args.threshold, 59)

    def test_parse_args_nonexistant_config(self):
        with self.assertRaises(SystemExit):
            parse_args(['--config', '%s-11' % self.config_file.name])

    def test_parse_args_wrong_args(self):
        with self.assertRaises(SystemExit):
            parse_args(['test'])

    def test_parse_args_negative_threshold(self):
        with self.assertRaises(SystemExit):
            parse_args('--err-threshold -1'.split())

    def test_parse_args_threshold_101(self):
        with self.assertRaises(SystemExit):
            parse_args('--err-threshold 101'.split())

    def test_parse_args_threshold_string(self):
        with self.assertRaises(SystemExit):
            parse_args('--err-threshold test'.split())


if __name__ == '__main__':
    unittest.main()
