from __future__ import unicode_literals

from .. import BasePlugin


class Plugin(BasePlugin):

    def handle_message(self, message):
        if message.text == '!test':
            message.reply("""
message.text: {}
message.sender: {}
message.sender.chat: {}
message.chat: {}
"""         .format(
                message.text, message.sender, message.sender.chat,
                message.chat).strip())
