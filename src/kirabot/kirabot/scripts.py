from __future__ import unicode_literals

from .app import App
from .exceptions import ProgrammingException


def run():
    try:
        App().run()
    except ProgrammingException as e:
        exit(e)
    exit(0)
