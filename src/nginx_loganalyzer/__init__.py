__version__ = '0.1.0'

import datetime
import logging
import os.path
import re
import shutil
from collections import namedtuple
from decimal import Decimal
from string import Template

LogFileTuple = namedtuple('LogTuple', 'filename type date')


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


def get_latest_filename(pattern, filenames, dir='.'):
    """Returns tuple (filename, date, extension) for the latest filename from
    filenames generator matching the pattern.  The pattern must contain named
    groups "yyyy", "mm", "dd", "ext" in order to capture them"""
    if pattern.__class__ != '_sre.SRE_Pattern':
        pattern = re.compile(pattern)
    max_filedate = None
    max_file = None
    for filename in filenames:
        if filename is None:
            continue
        match = pattern.match(filename)
        if not match:
            continue
        filedate = datetime.date(int(match.group('yyyy')), int(match.group('mm')), int(match.group('dd')))
        if max_filedate is None or filedate > max_filedate:
            max_filedate = filedate
            max_file = LogFileTuple(os.path.join(dir, filename), match.group('ext'), filedate)
    return max_file


def render_report(template_file, data, report_file):
    with open(template_file, 'r') as tpl:
        tpl_string = Template(tpl.read())
    with open(report_file, 'w') as r:
        r.write(tpl_string.safe_substitute(table_json=data))


def setup_reports(report_dir):
    """Create reports dir if not exists and copy jquery.tablesorter.min.js"""
    if not os.path.isdir(report_dir):
        logging.info('creating report dir %s' % report_dir)
        os.makedirs(report_dir)
        tablesorter_js = os.path.join(os.path.dirname(__file__), "jquery.tablesorter.min.js")
    if not os.path.exists(os.path.join(report_dir, 'jquery.tablesorter.min.js')):
        shutil.copy(tablesorter_js, report_dir)
    return True


def median(lst):
    """Find median of array of Decimals, return it as Decimal.
    Caveat: due to memory/cpu efficiency, type checking does not occur here"""
    n = len(lst)
    if n < 1:
        return None
    if n == 1:
        return Decimal(lst[0])
    if n % 2 == 1:
        return Decimal(sorted(lst)[n//2])
    else:
        return sum(sorted(lst)[n//2-1:n//2+1])/Decimal('2.0')
