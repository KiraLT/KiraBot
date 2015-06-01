from __future__ import unicode_literals


class User(object):

    def __init__(self, app, id, name, adapter):
        self.app = app
        self.id = id
        self.name = name
        self.chat = adapter.create_chat_with(self.id)
        self.storage = app.get_storage('communication:{}:users:{}'.format(
            adapter.name, self.id))

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.id)
