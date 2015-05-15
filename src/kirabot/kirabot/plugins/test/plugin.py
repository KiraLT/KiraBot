from __future__ import unicode_literals

from .. import BasePlugin


class Plugin(BasePlugin):

    name = 'test'

    def handle_message(self, message):
        if message.text == '!test':
            message.reply('Working')
