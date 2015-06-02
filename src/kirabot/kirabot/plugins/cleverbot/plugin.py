from __future__ import unicode_literals

from cleverbot import Cleverbot

from .. import BasePlugin


class Plugin(BasePlugin):

    def __init__(self, *args, **kwargs):
        super(Plugin, self).__init__(*args, **kwargs)
        self.bots = {}

    def handle_message(self, message):
        if message.text[0] != '!' and message.chat.private:
            if message.sender.id not in self.bots:
                self.bots[message.sender.id] = Cleverbot()
            bot = self.bots[message.sender.id]
            message.reply(bot.ask(message.text.encode('utf8')))
            return True
