from __future__ import unicode_literals

from difflib import SequenceMatcher

from .. import BasePlugin


class Plugin(BasePlugin):

    def relevance(self, text, commands):
        return sorted([
            (
                command,
                SequenceMatcher(
                    None, command[1:], text[1:]).ratio()
            )
            for command in commands
        ], key=lambda x: x[1])

    def handle_message(self, message):
        help_plugin = 'kirabot.plugins.help.plugin.Plugin'
        help_commands = self.manager.plugins[help_plugin].get_commands().keys()
        commands = [
            help_command[0]
            for help_command in self.relevance(message.text, help_commands)
            if help_command[1] > 0.3
        ]
        if message.text.startswith('!'):
            response = 'Unknown command, !help for list of commands'
            if commands:
                response += ' or try !{}'.format(commands[-1])
            message.reply(response)
            return True
