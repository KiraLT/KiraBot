from __future__ import unicode_literals

from .. import CommandPlugin


class Plugin(CommandPlugin):

    def get_commands(self):
        return {
            'ping': {
                'help': 'Play ping pong',
                'response': 'PONG'
            }
        }
