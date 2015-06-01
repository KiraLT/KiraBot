from __future__ import unicode_literals


class Message(object):

    def __init__(self, sender, chat, text):
        self.sender = sender
        self.chat = chat
        self.text = text

    def reply(self, text):
        self.chat.send_message(text)
