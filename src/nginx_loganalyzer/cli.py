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

from nginx_loganalyzer import logfinder
from nginx_loganalyzer import parse_log
from nginx_loganalyzer.config import Config
from nginx_loganalyzer.parser import UIShort

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}


def threshold_t(string):
    try:
        value = int(string)
    except ValueError:
        raise argparse.ArgumentTypeError('must be an integer')
    if (value < 0) or (value > 100):
        raise argparse.ArgumentTypeError('must be between 0 and 100')
    return value


def parse_args(args):
    parser = argparse.ArgumentParser(description='Find nginx log file,'
                                     ' parse it and produce the html report.')
    parser.add_argument('--config', default=None, type=argparse.FileType('r'),
                        help="Path to the config file")
    parser.add_argument('--err-threshold', dest='threshold', default=66,
                        type=threshold_t, help="Parsing error threshold")

    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args=args)
    the_conf = Config(config, args.config)
    # дальше работаем с the_conf.report_size, the_conf.report_dir etc.

    # ищем лог-файл для обработки
    log_tuple = logfinder(the_conf)
    log_regexp = UIShort.compile(['request', 'request_time'])
    parse_log(log_tuple, config, log_regexp)

    # парсим файл
