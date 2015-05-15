from __future__ import unicode_literals

from md5 import md5

from Skype4Py import Skype, cmsReceived

from ..message import Message


class SkypeAdapter(object):

    name = 'skype'

    def __init__(self, app):
        self.app = app
        self.skype = Skype()
        self.skype.FriendlyName = self.app.config['BOT_NAME']
        self.skype.Attach()
        self.message_hanlder = None

    def register_message_handler(self, handler):
        self.message_hanlder = handler
        self.skype.RegisterEventHandler('MessageStatus', self.handle_message)

    def handle_message(self, skype_message, status):
        if status == cmsReceived:
            message = Message(
                id=md5(unicode(skype_message._GetSender().Handle)).hexdigest(),
                text=unicode(skype_message.Body),
                name=unicode(skype_message._GetSender()._GetFullName())
            )
            message.register_reply_handler(skype_message.Chat.SendMessage)
            self.message_hanlder(message)
