import tempfile
import unittest

from nginx_loganalyzer.cli import parse_args


class TestCmdLineArgs(unittest.TestCase):
    def setUp(self):
        self.config_file = tempfile.NamedTemporaryFile(mode='r')

    def test_parse_args_empty(self):
        args = parse_args([])
        self.assertIsNone(args.config, 'config should be None by default'
                          'when unspecified in the args')

    def test_parse_args_config(self):
        args = parse_args(('--config %s' % self.config_file.name).split())
        self.assertEqual(args.config.name, self.config_file.name)

    def test_parse_args_nonexistant_config(self):
        with self.assertRaises(SystemExit):
            parse_args(['--config', '%s-11' % self.config_file.name])

    def test_parse_args_wrong_args(self):
        with self.assertRaises(SystemExit):
            parse_args(['test'])


if __name__ == '__main__':
    unittest.main()
