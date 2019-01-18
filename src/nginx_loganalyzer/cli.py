# -*- coding: utf-8 -*-

"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mnginx_loganalyzer` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``nginx_loganalyzer.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``nginx_loganalyzer.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import ConfigParser
import logging
import os
import sys
# import decimal
# import json
from pprint import pprint

from log_parse import LogReqtimeStat

from nginx_loganalyzer import get_latest_filename

config = {
    "REPORT_SIZE": '1000',
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "ANALYZER_LOG_FILE": None,
}


def threshold_t(string):
    try:
        value = int(string)
    except ValueError:
        raise argparse.ArgumentTypeError('must be an integer')
    if (value < 0) or (value > 100):
        raise argparse.ArgumentTypeError('must be between 0 and 100')
    return value


def parse_args(args, default_config=None):
    parser = argparse.ArgumentParser(description='Find nginx log file,'
                                     ' parse it and produce the html report.')
    parser.add_argument('--config', default=default_config,
                        type=argparse.FileType('r'),
                        help="Path to the config file")
    parser.add_argument('--err-threshold', dest='threshold', default=66,
                        type=threshold_t, help="Parsing error threshold")
    return parser.parse_args(args)


class ConfigDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


def main(args=None):
    logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        level=logging.INFO)
    try:
        args = parse_args(args=args, default_config='~/.analyzer.cfg')
        c = ConfigParser.ConfigParser(config)
        section = 'DEFAULT'
        if args.config:
            c.readfp(args.config)
            section = c.sections()[0]
            args.config.close()
        the_conf = ConfigDict(c.items(section))
        logging.info('%s launched in %s with config file %s' %
                     (sys.argv[0], os.getcwd(), args.config.name,))
        logging.info('parsed configuration from file %s: %s' %
                     (args.config.name, the_conf))
        logfile_pattern = r'nginx-access-ui.log-' + \
                          r'(?P<yyyy>\d\d\d\d)(?P<mm>\d\d)(?P<dd>\d\d)' + \
                          r'(?P<ext>\.gz)?'

        files = (f for f in os.listdir(the_conf.log_dir))
        latest_tuple = get_latest_filename(logfile_pattern, files, the_conf.log_dir)
        logging.info('Parsing file %s' % latest_tuple.filename)

        log_parser = LogReqtimeStat(latest_tuple, the_conf)

        pprint(log_parser.parse_log())
    except Exception:
        logging.exception('Exception raised')
        raise
