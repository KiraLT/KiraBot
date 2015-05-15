from __future__ import unicode_literals

from .. import CommandPlugin


class Plugin(CommandPlugin):

    name = 'help'

    def get_commands(self):
        commands = {}
        for plugin in self.manager.plugins.itervalues():
            if plugin.name == self.name:
                continue
            if not isinstance(plugin, CommandPlugin):
                continue
            for command, params in plugin.get_commands().iteritems():
                if 'help' in params:
                    commands['help {}'.format(command)] = {
                        'response': params['help']
                    }
        commands['help'] = {
            'response': 'Help commands:\n' + '\n'.join([
                '!{}'.format(command)
                for command in commands.keys()])
        }
        return commands
