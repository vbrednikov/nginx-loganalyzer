import re


class Config(object):
    def __init__(self, config, config_file=None):
        self.report_size = config['REPORT_SIZE']
        self.report_dir = config['REPORT_DIR']
        self.log_dir = config['LOG_DIR']
        self.log_re = re.compile(r'^nginx-access-ui.log-(20170630)(.gz)?$')
