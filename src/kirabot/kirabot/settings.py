from __future__ import unicode_literals

DEBUG = True

BOT_NAME = 'KiraBot'
LOGGER_NAME = 'kirabot'
LOG_LEVEL = 'DEBUG'
CONSOLE_LOG_FORMAT = '[%(levelname)s]: %(message)s'
PLUGINS = [
    'kirabot.plugins.test.plugin.Plugin',
    'kirabot.plugins.help.plugin.Plugin',
    'kirabot.plugins.horriblesubs.plugin.Plugin',
    'kirabot.plugins.ping.plugin.Plugin',
    'kirabot.plugins.cleverbot.plugin.Plugin',
]
