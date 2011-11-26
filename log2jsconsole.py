from logging import (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL,
                     Handler, getLogger)
from werkzeug.local import LocalStack
from werkzeug.utils import cached_property
try:
    from simplejson import dumps
except ImportError:
    from json import dumps


class WSGIHandler(Handler):

    def __init__(self, middleware, level=NOTSET):
        super(WSGIHandler, self).__init__(level)
        self.middleware = middleware

    def emit(self, record):
        records = self.middleware.context.top
        if records is not None:
            records.append(record)


class LoggingMiddleware(object):

    def __init__(self, app, auto_install=True):
        self.app = app
        self.context = LocalStack()
        if auto_install:
            logger = getLogger()
            logger.setLevel(DEBUG)
            logger.addHandler(self.handler)

    @cached_property
    def handler(self):
        return WSGIHandler(self)

    def __call__(self, environ, start_response):
        html = [False]
        def start(status, headers):
            headers = list(headers)
            replaced_headers = []
            for k, v in headers:
                name = k.lower().strip()
                if name == 'content-type':
                    content_type = v.lower().split(';')[0]
                    content_type = content_type.strip().lower()
                    html[0] = content_type == 'text/html'
                if name != 'content-length':
                    replaced_headers.append((k, v))
            return start_response(status, replaced_headers)
        self.context.push([])
        result = self.app(environ, start)
        if html:
            return self.inject_log_html(result)
        return result

    def inject_log_html(self, iterable):
        injected = False
        for chunk in iterable:
            if not injected and '</body>' in chunk:
                a, b = chunk.split('</body>', 1)
                yield a
                for subchunk in self.log_html():
                    yield subchunk
                yield b
                injected = True
            else:
                yield chunk
        if not injected:
            for chunk in self.log_html():
                yield chunk

    def log_html(self):
        level_map = {DEBUG: 'debug', INFO: 'info', WARNING: 'warn',
                     ERROR: 'error', CRITICAL: 'error'}
        records = self.context.pop()
        yield '<script>\n//<![CDATA[\nif (console) {\n'
        for record in records:
            yield 'console.'
            yield level_map[record.levelno]
            yield '('
            yield dumps(record.name)
            yield ' + ": " + '
            yield dumps(str(record.getMessage()))
            yield ');'
        yield '\n}\n// ]]>\n</script>'

