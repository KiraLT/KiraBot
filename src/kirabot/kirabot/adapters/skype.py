from __future__ import unicode_literals

from Skype4Py import Skype, cmsReceived


class SkypeAdapter(object):

    name = 'skype'

    def __init__(self, app):
        self.app = app
        self.skype = Skype()
        self.skype.FriendlyName = 'KiraBot'
        self.skype.Attach()
        self.skype.RegisterEventHandler('MessageStatus', self.message_handler)

    def message_handler(self, message, status):
        data = {
            'skype_name': unicode(message._GetSender().Handle),
            'display_name': unicode(message._GetSender()._GetFullName()),
            'chat_name': unicode(message.ChatName),
            'body': unicode(message.Body)
        }
        if status == cmsReceived:
            self.app.logger.debug(data)
