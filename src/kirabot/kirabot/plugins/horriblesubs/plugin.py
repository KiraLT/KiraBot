from __future__ import unicode_literals

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from .. import CommandPlugin


class Plugin(CommandPlugin):

    name = 'horriblesubs'

    def get_commands(self):
        return {
            'horriblesubs new': {
                'help': 'Play ping pong',
                'callback': self.get_new
            }
        }

    def get_new(self):
        try:
            r = requests.get('http://horriblesubs.info/lib/latest.php')
            if not r.ok:
                raise RequestException()
        except RequestException:
            return 'Busy at the moment, go back later'
        response = 'Latest releases:\n'
        soup = BeautifulSoup(r.content)
        for episode in soup.findAll('div', class_='episode')[:5]:
            response += '* {}\n'.format(episode.contents[0].strip())
        return response
