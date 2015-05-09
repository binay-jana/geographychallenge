import sys
import os
_root = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
sys.path.extend([os.path.sep.join(_root)])

if __name__ == '__main__':
    print >> sys.stderr, """\
use: gunicorn -c gunicorn.conf.py start_app
"""
    sys.exit(1)

from flask_challenge_app.challenge import app as application
