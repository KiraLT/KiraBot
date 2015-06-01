from __future__ import unicode_literals

import os.path

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
    'kirabot.plugins.unknown.plugin.Plugin',
]
COMMUNICATION_ADAPTERS = [
    'kirabot.communication.adapters.skype.SkypeAdapter'
]
STORAGE_FILE = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))), 'var/kirabot/data.json')
STORAGE = 'kirabot.storage.FileStorage'
