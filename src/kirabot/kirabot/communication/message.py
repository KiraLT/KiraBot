from __future__ import unicode_literals


class Message(object):

    def __init__(self, id, name, text):
        self.id = id
        self.name = name
        self.text = text.strip()
        self.reply_handler = None

    def reply(self, text):
        self.reply_handler(text)

    def register_reply_handler(self, handler):
        self.reply_handler = handler
