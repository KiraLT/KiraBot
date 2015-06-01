from __future__ import unicode_literals

import re
from pydoc import locate

from ..exceptions import ProgrammingException, ConfigException
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
            Plugin = locate(name)
            if Plugin is None:
                raise ImportError
        except ImportError:
            raise ConfigException('Plugin %s not found' % name)
        if not issubclass(Plugin, BasePlugin):
            raise ProgrammingException(
                'Plugin %s must be subclass of BasePlugin' % name)
        self.plugins[name] = Plugin(self.app, self, name)

    def message_handler(self, message):
        for plugin in self.plugins.itervalues():
            if plugin.handle_message(message):
                break

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

    def __init__(self, app, manager, name):
        self.app = app
        self.manager = manager
        self.name = name

    def handle_message(self, message):
        return False


class CommandPlugin(BasePlugin):

    def generate_regex(self, text):
        if text.startswith('<') and text.endswith('>'):
            re_type = text[1:-1]
            if re_type[0] == '?':
                optional = True
                re_type = re_type[1:]
            else:
                optional = False
            if ':' in re_type:
                re_type, re_group = re_type.split(':', 2)
            else:
                re_group = None
            re_map = {
                'string': '[^ ]',
                'text': '.',
                'int': '[0-9]'
            }
            if re_type in re_map:
                regex = re_map[re_type]
                if optional:
                    regex += '*'
                else:
                    regex += '+'
                if re_group is not None:
                    return '(?P<{}>{})'.format(re_group, regex)
                return '({})'.format(regex)
            else:
                raise ProgrammingException('Unknow regex type %s' % re_type)
        return re.escape(text)

    def handle_message(self, message):
        for command_text, params in self.get_commands().iteritems():
            command_list = command_text.split()
            regex = r'^\s*!{}\s*$'.format(r' \s*'.join([
                self.generate_regex(command_part)
                for command_part in command_list]))
            match = re.match(regex, message.text + ' ')
            if match:
                kwargs = match.groupdict()
                response = None
                if 'response' in params:
                    response = params['response'].format(**kwargs)
                if 'callback' in params:
                    response = params['callback'](message, **kwargs)
                if response is not None:
                    message.reply(response)
                    return True

    def get_commands(self):
        raise NotImplementedError()
