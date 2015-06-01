from __future__ import unicode_literals

from time import time

from .. import BasePlugin


class Plugin(BasePlugin):

    def handle_message(self, message):
        if message.text.startswith('!test'):
            if 'last_check' not in message.sender.storage:
                message.sender.storage['last_check'] = int(time())
            message.reply("""
message.text: {}
message.sender: {}
message.sender.chat: {}
message.chat: {}

Last check: {}s ago
"""         .format(
                message.text, message.sender, message.sender.chat,
                message.chat,
                int(time()) - message.sender.storage['last_check']).strip())
            message.sender.storage['last_check'] = int(time())
            return True
