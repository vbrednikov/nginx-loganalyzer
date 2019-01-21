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
import json
import logging
import os
import re
import sys

from log_parse import LogReqtimeStat

from nginx_loganalyzer import ConfigDict
from nginx_loganalyzer import get_latest_filename
from nginx_loganalyzer import render_report
from nginx_loganalyzer import setup_reports

config = {
    "REPORT_SIZE": '1000',
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "ANALYZER_LOG_FILE": None,
    "threshold": '75',
}


def parse_args(args, default_config=None):
    parser = argparse.ArgumentParser(description='Find nginx log file,'
                                     ' parse it and produce the html report.')
    parser.add_argument('--config', default=default_config,
                        type=argparse.FileType('r'),
                        help="Path to the config file")
    return parser.parse_args(args)


def main(args=None):
    # setup some variables
    logfile_name_pattern = r'nginx-access-ui.log-' + \
                           r'(?P<yyyy>\d\d\d\d)(?P<mm>\d\d)(?P<dd>\d\d)' + \
                           r'(?P<ext>\.gz)?$'

    template_file = os.path.join(os.path.dirname(__file__), "report.html")

    # parse commandline args
    args = parse_args(args=args, default_config='~/.analyzer.cfg')

    # parse and merge config file
    c = ConfigParser.ConfigParser(config)
    section = 'DEFAULT'
    if args.config:
        c.readfp(args.config)
        section = c.sections()[0]
        args.config.close()
    the_conf = ConfigDict(c.items(section))
    logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        level=logging.INFO,
                        filename=the_conf.analyzer_log_file)

    try:
        # validate report_size parameter in the config
        if not re.match(r'^\d+$', the_conf.report_size):
            logging.error("Wrong format for report_size in %s: %s" %
                          (os.path.abspath(args.config.name), the_conf.report_size))
            raise ValueError

        # validate report_size parameter in the config
        if not (
                re.match(r'^\d+$', the_conf.threshold)
                and int(the_conf.threshold) <= 100 or int(the_conf.threshold) > 0):
            logging.error("Wrong format for report_size in %s: %s" %
                          (os.path.abspath(args.config.name), the_conf.report_size))
            raise ValueError

        logging.info('%s launched in %s with config file %s' %
                     (sys.argv[0], os.getcwd(), args.config.name,))
        logging.info('parsed configuration from file %s: %s' %
                     (args.config.name, the_conf))

        # get files list
        files = (f for f in os.listdir(the_conf.log_dir))

        # get latest file to parse, exit with success if nothing found
        latest_tuple = get_latest_filename(logfile_name_pattern, files, the_conf.log_dir)
        if latest_tuple is None:
            logging.info("No suitable log to parse found in %s" % the_conf.log_dir)
            sys.exit(0)

        logging.info('Got the file %s' % latest_tuple.filename)

        # create reports dir
        setup_reports(the_conf.report_dir)

        # get filename for the future report
        report_file = os.path.join(the_conf.report_dir,
                                   latest_tuple.date.strftime('report-%Y.%m.%d.html'))
        logging.info('report file: %s' % report_file)

        # exit with success if report file already exists
        if os.path.exists(report_file):
            logging.info('report file for %s already exists: %s' %
                         (latest_tuple.filename, report_file))
            sys.exit(0)

        # exit with error if there is no template file
        if not os.path.exists(template_file):
            logging.error('template file %s does not exist' % template_file)
            sys.exit(1)

        # create and invoke log_parser instance
        log_parser = LogReqtimeStat(latest_tuple, the_conf)
        log_stat = log_parser.parse_log()
        if log_stat is None:
            logging.error('Unable to parse the log')
            sys.exit(1)
        logging.info('finished')

        # generate the report
        logging.info('writing report to %s' % report_file)
        data = json.dumps(log_stat, default=str)
        render_report(template_file, data, report_file)
        logging.info('finished')
    except KeyboardInterrupt:
        logging.exception('KeyboardInterrupt')
        raise
    except Exception:
        logging.exception('Exception raised')
        raise
