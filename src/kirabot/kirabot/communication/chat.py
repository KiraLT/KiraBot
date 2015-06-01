from __future__ import unicode_literals


class Chat(object):

    def __init__(self, app, id, name, adapter, private=False):
        self.app = app
        self.id = id
        self.name = name
        self.private = private
        self.adapter = adapter
        self.storage = app.get_storage('communication:{}:chats:{}'.format(
            self.adapter.name, self.id))

    def __unicode__(self):
        return '{} ({}, private={})'.format(
            self.name, self.id, self.private)

    def send_message(self, text):
        self.adapter.send_message(self, text)
