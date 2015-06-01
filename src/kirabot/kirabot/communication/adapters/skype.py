from __future__ import unicode_literals

from Skype4Py import Skype, cmsReceived

from kirabot.exceptions import ProgrammingException

from ..message import Message
from ..user import User
from ..chat import Chat


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
                app=self.app,
                sender=self.create_user(skype_message.Sender.Handle),
                chat=self.create_chat(skype_message.Chat.Name),
                text=unicode(skype_message.Body).strip()
            )
            self.message_hanlder(message)

    def get_skype_chat(self, chat_id):
        for skype_chat in self.skype.Chats:
            if chat_id == skype_chat.Name:
                return skype_chat
        else:
            raise ProgrammingException('Chat %s not found' % chat_id)

    def get_skype_user(self, user_id):
        for skype_user in self.skype.Friends:
            if skype_user.Handle == user_id:
                return skype_user
        else:
            raise ProgrammingException('User %s not found' % user_id)

    def send_message(self, chat, text):
        for skype_chat in self.skype.Chats:
            if chat.id == skype_chat.Name:
                skype_chat.SendMessage(text)
                break
        else:
            raise ProgrammingException('Chat %s not found' % chat.id)

    def create_chat_with(self, name):
        skype_chat = self.skype.CreateChatWith(name)
        return self.create_chat(skype_chat.Name)

    def create_chat(self, chat_id):
        skype_chat = self.get_skype_chat(chat_id)
        return Chat(
            app=self.app,
            id=unicode(skype_chat.Name),
            name=unicode(skype_chat.FriendlyName),
            adapter=self,
            private=len(skype_chat.Members) == 2)

    def create_user(self, user_id):
        skype_user = self.get_skype_user(user_id)
        return User(
            app=self.app,
            id=unicode(skype_user.Handle),
            name=unicode(skype_user.FullName),
            adapter=self
        )
