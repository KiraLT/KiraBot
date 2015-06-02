from __future__ import unicode_literals

import requests
from requests.exceptions import RequestException
from time import sleep

from bs4 import BeautifulSoup

from .. import CommandPlugin


class Plugin(CommandPlugin):

    def get_commands(self):
        return {
            'hs new': {
                'help': 'Get new releases',
                'callback': self.new
            },
            'hs find <text:query>': {
                'help': 'Search for anime releases',
                'callback': self.search
            },
            'hs subscribe <text:name>': {
                'help': 'Subscibe for notifications of new releases',
                'callback': self.subscribe
            },
            'hs unsubscribe <text:name>': {
                'help': 'Unsubscibe for notifications of new releases',
                'callback': self.unsubscribe
            }
        }

    def background(self):
        while True:
            if 'anime' not in self.storage:
                self.storage['anime'] = []
            try:
                content = self.make_request('lib/latest.php')
            except RequestException as e:
                self.app.exceptions(e)
            for data in self.parse_list(content):
                if data['anime'] not in self.storage['anime']:
                    self.storage['anime'].append(data['anime'])
            sleep(60)

    def parse_list(self, content):
        results = []
        soup = BeautifulSoup(content)
        for episode in soup.findAll('div', class_='episode'):
            name = ' '.join(episode.contents[0].strip().split(' ')[1:])
            resolutions = []
            for res_div in episode.findAll(class_='resolution-block'):
                if not res_div.find('a'):
                    continue
                resolution = res_div.find('a').text.strip()
                torrent_link = res_div.find('a', text='Torrent').get('href')
                resolutions.append({
                    'resolution': resolution,
                    'torrent': torrent_link
                })
            results.append({
                'anime': '-'.join(name.split('-')[:-1]).strip(),
                'episode': name.split('-')[-1].strip(),
                'resolutions': resolutions
            })
        return results

    def parse_list_response(self, content, limit):
        response = ''
        for data in self.parse_list(content)[:limit]:
            response += '* {} - {}\n'.format(data['anime'], data['episode'])
            for resolution in data['resolutions']:
                response += '  [{}] {}\n'.format(
                    resolution['resolution'],
                    resolution['torrent'])
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

    def new(self, message):
        try:
            content = self.make_request('lib/latest.php')
        except RequestException as e:
            return unicode(e)
        response = 'Latest releases:\n'
        response += self.parse_list_response(content, 5)
        return response

    def search(self, message, query):
        try:
            content = self.make_request('lib/search.php', value=query)
        except RequestException as e:
            return unicode(e)
        response = 'Releases for {}:\n'.format(query)
        response += self.parse_list_response(content, 5)
        return response

    def subscribe(self, message, name):
        if name not in self.storage['anime']:
            if self.name not in message.sender.storage:
                message.sender.storage[self.name] = {
                    'subscibe': []
                }
            message.sender.storage[self.name]['subscibe'].append(name)
            return 'This anime is not supported'
        return 'You successfully subscribed to {}'.format(name)

    def unsubscribe(self, message, name):
        return 'You unsuccessfully subscribed to {}'.format(name)
