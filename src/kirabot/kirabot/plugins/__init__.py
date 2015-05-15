from __future__ import unicode_literals

from importlib import import_module
import re

from ..exceptions import ProgrammingException
from ..communication import Communication


class PluginsManager(object):

    def __init__(self, app):
        self.app = app
        self.plugins = {}
        self.communication = Communication(self.app)
        self.communication.register_message_handler(self.message_handler)

    def run_plugin(self, name):
        if name in self.plugins:
            raise ProgrammingException('Plugin %s already runnning' % name)
        try:
            module = import_module('.%s.plugin' % name, __package__)
            if not hasattr(module, 'Plugin'):
                raise ImportError
        except ImportError:
            raise ProgrammingException('Plugin %s not found' % name)
        if not issubclass(module.Plugin, BasePlugin):
            raise ProgrammingException(
                'Plugin %s must be subclass of BasePlugin' % name)
        if module.Plugin.name is None:
            raise ProgrammingException(
                'Plugin %s must have specified name' % name)
        plugin = module.Plugin(self.app, self)
        self.plugins[plugin.name] = plugin

    def message_handler(self, message):
        for plugin in self.plugins.itervalues():
            plugin.handle_message(message)

    def stop_plugin(self, name):
        if name not in self.plugins:
            raise ProgrammingException('Plugin %s is not runnning' % name)
        raise NotImplementedError()

    def stop_all_plugins(self, name):
        for plugin in self.plugins.itervalues():
            self.stop_plugin(plugin.name)

    def run_all_plugins(self):
        for plugin_name in self.app.config['PLUGINS']:
            self.run_plugin(plugin_name)


class BasePlugin(object):

    name = None

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

    def handle_message(self, message):
        pass


class CommandPlugin(BasePlugin):

    def generate_regex(self, text):
        return re.escape(text)

    def handle_message(self, message):
        for command_text, params in self.get_commands().iteritems():
            command_list = command_text.split()
            regex = r'^!{}$'.format(r' \s*'.join([
                self.generate_regex(command_part)
                for command_part in command_list]))
            match = re.match(regex, message.text)
            args = []
            kwargs = {}
            if match:
                if 'response' in params:
                    message.reply(params['response'])
                if 'callback' in params:
                    message.reply(params['callback'](*args, **kwargs))

    def get_commands(self):
        raise NotImplementedError()
