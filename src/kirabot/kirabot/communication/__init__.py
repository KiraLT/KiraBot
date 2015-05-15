from __future__ import unicode_literals

from .adapters.skype import SkypeAdapter


class Communication(object):

    adapter_classes = [SkypeAdapter]

    def __init__(self, app):
        self.app = app
        self.adapters = {
            adapter_class.name: adapter_class(app)
            for adapter_class in self.adapter_classes
        }

    def register_message_handler(self, handler):
        for adapter in self.adapters.itervalues():
            adapter.register_message_handler(handler)
