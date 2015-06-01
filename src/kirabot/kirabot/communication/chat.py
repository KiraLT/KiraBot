from __future__ import unicode_literals


class Chat(object):

    def __init__(self, id, name, adapter, private=False):
        self.id = id
        self.name = name
        self.private = private
        self.adapter = adapter
        self.message_handler = None

    def __unicode__(self):
        return '{} ({}, private={})'.format(
            self.name, self.id, self.private)

    def send_message(self, text):
        self.adapter.send_message(self, text)
