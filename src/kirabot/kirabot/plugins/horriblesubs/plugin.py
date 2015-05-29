from __future__ import unicode_literals

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from .. import CommandPlugin


class Plugin(CommandPlugin):

    def get_commands(self):
        return {
            'hs new <?int:limit>': {
                'help': 'Get new releases',
                'callback': self.new
            },
            'hs find <text:query>': {
                'help': 'Search for anime releases',
                'callback': self.search
            }
        }

    def parse_list(self, content, limit):
        response = ''
        soup = BeautifulSoup(content)
        for episode in soup.findAll('div', class_='episode')[:limit]:
            name = ' '.join(episode.contents[0].strip().split(' ')[1:])
            response += '* {}\n'.format(name)
            for res_div in episode.findAll(class_='resolution-block'):
                resolution = res_div.find('a').text.strip()
                torrent_link = res_div.find('a', text='Torrent').get('href')
                response += '  [{}] {}\n'.format(resolution, torrent_link)
        if not response:
            response = 'Can\' find what your are looking for :('
        return response

    def make_request(self, url_path, **kwargs):
        try:
            r = requests.get(
                'http://horriblesubs.info/{}'.format(url_path),
                params=kwargs)
            if not r.ok:
                raise RequestException()
        except RequestException:
            raise RequestException('Busy at the moment, go back later')
        return r.content

    def new(self, message, limit):
        if not limit:
            limit = 5
        try:
            content = self.make_request('lib/latest.php')
        except RequestException as e:
            return unicode(e)
        response = 'Latest releases:\n'
        response += self.parse_list(content, int(limit))
        return response

    def search(self, message, query, limit):
        if not limit:
            limit = 5
        try:
            content = self.make_request('lib/search.php', value=query)
        except RequestException as e:
            return unicode(e)
        response = 'Releases for {}:\n'.format(query)
        response += self.parse_list(content, int(limit))
        return response
