from __future__ import unicode_literals

from importlib import import_module


from ..exceptions import ProgrammingException
from ..communication import Communication


class PluginsManager(object):

    def __init__(self, app):
        self.app = app
        self.plugins = set()

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
        plugin = module.Plugin(self)
        plugin.run()
        self.plugins.add(plugin)

    def stop_plugin(self, name):
        if name not in self.plugins:
            raise ProgrammingException('Plugin %s is not runnning' % name)
        raise NotImplementedError()

    def stop_all_plugins(self, name):
        for plugin in self.plugins:
            self.stop_plugin(plugin.name)

    def run_all_plugins(self):
        for plugin_name in self.app.config['PLUGINS']:
            self.run_plugin(plugin_name)


class BasePlugin(object):

    name = None

    def __init__(self, manager):
        if self.name is None:
            ProgrammingException('Plugin must have specified name')
        self.manager = manager
        self.app = self.manager.app
        self.communication = Communication(self.app)

    def handle_message(self, message):
        pass

    def run(self):
        self.communication.register_message_handler(self.handle_message)
