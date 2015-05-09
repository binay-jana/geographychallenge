# -*- coding: utf-8; Mode: python; tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
# ex: set softtabstop=4 tabstop=4 shiftwidth=4 expandtab fileencoding=utf-8:
import os, sys, logging, types, traceback
from logging.handlers import SysLogHandler, WatchedFileHandler
from cStringIO import StringIO

class _LogRotateFileHandler(WatchedFileHandler):
    def __init__(self, filename):
        WatchedFileHandler.__init__(self, filename, encoding='utf-8')

class Log(object):
    __file_path = None
    __file_level = logging.NOTSET
    __logging_handler_console = None
    __logging_handler_console_disabled = False

    @staticmethod
    def initialize(fmt,
                   level_console,
                   level_file, file_path,
                   level_syslog, syslog_host, syslog_port,
                   level_sentry, sentry_DSN):
        level_console = Log.__level(level_console)
        level_file = Log.__level(level_file)
        level_syslog = Log.__level(level_syslog)
        level_sentry = Log.__level(level_sentry)
        formatter = logging.Formatter(fmt)
        root = logging.getLogger('')
        root.setLevel(logging.ERROR)
        if level_console != logging.NOTSET:
            console = logging.StreamHandler()
            console.setLevel(level_console)
            console.setFormatter(formatter)
            if not Log.__logging_handler_console_disabled:
                root.addHandler(console)
            Log.__logging_handler_console = console
        if level_file != logging.NOTSET:
            file_path_keys = {
                # values to use for substition within the file_path
                'program': Log.getServerName().lower(),
                'version': Log.getVersionName(),
            }
            Log.__file_path = 'a.log'
            Log.__file_level = level_file
            file_output = _LogRotateFileHandler(Log.__file_path)
            file_output.setLevel(Log.__file_level)
            file_output.setFormatter(formatter)
            root.addHandler(file_output)
        if level_syslog != logging.NOTSET:
            syslog = SysLogHandler((syslog_host, syslog_port))
            syslog.setLevel(level_syslog)
            syslog.setFormatter(formatter)
            root.addHandler(syslog)
        if level_sentry != logging.NOTSET:
            from raven.handlers.logging import SentryHandler
            from raven.conf import setup_logging
            sentry = SentryHandler(sentry_DSN)
            sentry.setLevel(level_sentry)
            setup_logging(sentry)

    @staticmethod
    def allowConsole(status):
        Log.__logging_handler_console_disabled = not status
        if Log.__logging_handler_console is not None:
            root = logging.getLogger('')
            if status:
                root.addHandler(Log.__logging_handler_console)
            else:
                root.removeHandler(Log.__logging_handler_console)

    @staticmethod
    def getLoggerFilePath():
        return Log.__file_path

    @staticmethod
    def getLoggerFileLevel():
        return Log.__file_level

    @staticmethod
    def setLevel(level):
        root = logging.getLogger('')
        root.setLevel(Log.__level(level))

    @staticmethod
    def getLogger(name):
        [(filename, tmp, tmp, tmp), tmp] = traceback.extract_stack(limit=2)
        path = os.path.dirname(os.path.abspath(filename)).split(os.path.sep)
        prefix = path[len(name.split('.')) * -1]
        if name == '__main__':
            name = os.path.basename(sys.argv[0]).split('.')[0].lower()
        return logging.getLogger(prefix + '.' + name)

    @staticmethod
    def stacktrace(logger, exception=True, title=None, critical=False):
        stream = StringIO()
        if title is not None:
            stream.write(title + os.linesep)
        if exception:
            traceback.print_exc(file=stream)
        else:
            traceback.print_stack(file=stream)
        if critical:
            logger.critical(stream.getvalue())
        else:
            logger.error(stream.getvalue())
        stream.close()

    @staticmethod
    def __level(level):
        if level is None:
            logging_level = logging.NOTSET
        elif (type(level) == types.IntType or type(level) == types.LongType):
            levels = [
                logging.NOTSET,
                logging.CRITICAL,
                logging.ERROR,
                logging.WARNING,
                logging.INFO,
                logging.DEBUG,
            ]
            if level >= len(levels):
                logging_level = levels[-1]
            else:
                logging_level = levels[level]
        elif (type(level) == types.StringType or type(level) == types.UnicodeType):
            logging_level = {
                'critical': logging.CRITICAL,
                'error': logging.ERROR,
                'warning': logging.WARNING,
                'info': logging.INFO,
                'debug': logging.DEBUG,
            }.get(level.encode('ascii').lower(), logging.NOTSET)
        else:
            assert False
        return logging_level

    @staticmethod
    def getServerName():
        program = os.path.basename(sys.argv[0])
        if program == 'gunicorn':
            program = sys.argv[-1]
        elif program[-3:] == '.py':
            program = program[:-3]
        return program

    @staticmethod
    def getVersionName():
        config_version_text = '00'
        return config_version_text
