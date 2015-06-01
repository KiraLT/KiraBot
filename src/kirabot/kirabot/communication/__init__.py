from __future__ import unicode_literals

from pydoc import locate

from kirabot.exceptions import ConfigException

from .adapters.skype import SkypeAdapter


class Communication(object):

    adapter_classes = [SkypeAdapter]

    def __init__(self, app):
        self.app = app
        self.adapters = {}
        for adapter_string in app.config['COMMUNICATION_ADAPTERS']:
            Adapter = locate(adapter_string)
            if Adapter is None:
                raise ConfigException('Adapter %s not found' % adapter_string)
            self.adapters[Adapter.name] = Adapter(self.app)

    def register_message_handler(self, handler):
        for adapter in self.adapters.itervalues():
            adapter.register_message_handler(handler)
