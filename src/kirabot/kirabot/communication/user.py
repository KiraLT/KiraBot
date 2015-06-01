from __future__ import unicode_literals


class User(object):

    def __init__(self, id, name, adapter):
        self.id = id
        self.name = name
        self.chat = adapter.create_chat_with(self.id)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.id)
