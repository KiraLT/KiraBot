from __future__ import unicode_literals

from .. import CommandPlugin


class Plugin(CommandPlugin):

    def format_command(self, command):
        return 'help {}'.format(' '.join([
            part
            for part in command.split()
            if not part.startswith('<') and not part.endswith('>')
        ]))

    def format_help_text(self, command, help_text):
        return "Usage: !{}\n{}".format(command, help_text)

    def get_commands(self):
        commands = {}
        for plugin in self.manager.plugins.itervalues():
            if plugin.name == self.name:
                continue
            if not isinstance(plugin, CommandPlugin):
                continue
            for command, params in plugin.get_commands().iteritems():
                if 'help' in params:
                    commands[self.format_command(command)] = {
                        'response': self.format_help_text(
                            command, params['help'])
                    }
        commands['help'] = {
            'response': 'Help commands:\n' + '\n'.join(sorted([
                '!{}'.format(command)
                for command in commands.keys()]))
        }
        return commands
