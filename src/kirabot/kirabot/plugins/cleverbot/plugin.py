from __future__ import unicode_literals

import cleverbot

from .. import BasePlugin


class Plugin(BasePlugin):

    def handle_message(self, message):
        if message.text[0] != '!' and message.chat.private:
            bot = cleverbot.Cleverbot()
            message.reply(bot.ask(message.text.encode('utf8')))
            return True
