import re


class LogReCollection(object):
    _digit_re = r'(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})'
    _ipv4_re = r'{dig}(?:\.{dig}){{3}}'.format(dig=_digit_re)
    _quoted_re = r'[^"]+'

    remote_addr = (_ipv4_re,)
    remote_user = (r'-|\S+',)
    http_x_real_ip = ('-|{}'.format(_ipv4_re),)
    datetime = ('[^]]+',)
    request_method = (r'[A-Z]+',)
    request = (r'[^"]+',)
    request_protocol = (r'HTTP/\d+\.\d+',)
    status = (r'\d+',)
    body_bytes_sent = (r'\d+',)
    http_referer = (_quoted_re,)
    http_user_agent = (_quoted_re,)
    http_x_forwarded_for = (_quoted_re,)
    http_x_request_id = (_quoted_re,)
    http_x_rb_user = (_quoted_re,)
    request_time = (r'\d+\.\d+',)
    time_local = (r'\[\d{2}\/\w{3}\/\d{4}(?::\d{2}){3} [-+]\d{4}\]',)

    def lib(self):
        """Returns all tuple arguments of the class (that are considered as
           elements of regexps library"""
        for name in dir(self):
            if not name.startswith('__') and type(getattr(self, name)) == tuple:
                yield name, getattr(self, name)[0]

    def _prepare_regexps(self, fields):
        regexps = {}
        for name, regexp in self.lib():
            regexps[name] = '(?{0}{1})'.format(
                'P<%s>' % name if name in fields else ':',
                regexp
            )
        return regexps

    def item(self, name):
        """returns compiled regexp for the named item"""
        if not name.startswith('__') and type(getattr(self, name)) == tuple \
                and name != 'log_format':
            return re.compile(getattr(self, name)[0])

    def compile(self, fields=[]):
        """Prepares and compiles log_format attribute.
           If fields is not empty, each named attribute from fields
           becomes a named capture"""
        regexps = self._prepare_regexps(fields)
        return re.compile(self.log_format.format(**regexps))


class UIShort(LogReCollection):
    log_format = r'{remote_addr}\s+{remote_user}\s+{http_x_real_ip}\s+{time_local}\s+"{request_method} {request} {request_protocol}"\s+' \
                 r'{status}\s+{body_bytes_sent}\s+"{http_referer}"\s+' \
                 r'"{http_user_agent}"\s+"{http_x_forwarded_for}"\s+"{http_x_request_id}"\s+"{http_x_rb_user}"\s+' \
                 r'{request_time}'
