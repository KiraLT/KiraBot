from __future__ import unicode_literals

import requests
from requests.exceptions import RequestException
from time import sleep

from bs4 import BeautifulSoup

from .. import CommandPlugin


class Plugin(CommandPlugin):

    def init(self):
        if 'anime' not in self.storage:
            self.storage['anime'] = []
        if 'schedule' not in self.storage:
            self.storage['schedule'] = {}
        if 'new' not in self.storage:
            self.storage['new'] = {}

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
            },
            'hs subscribed': {
                'help': 'Show subscribed releases',
                'callback': self.subscribed
            },
            'hs schedule': {
                'help': 'Release schedule',
                'callback': self.schedule
            }
        }

    def background(self):
        while True:
            try:
                content = self.make_request('release-schedule/')
            except RequestException as e:
                self.app.exception(e)
            self.storage['schedule'] = self.parse_shedule(content)
            try:
                content = self.make_request('lib/latest.php')
            except RequestException as e:
                self.app.exception(e)
            self.storage['anime'] = []
            for animes in self.storage['schedule'].itervalues():
                for anime in animes.iterkeys():
                    self.storage['anime'].append(anime)
            self.storage['new'] = self.parse_list(content)
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

    def format_response(self, data):
        response = ''
        for data in data:
            response += '* {} - {}\n'.format(data['anime'], data['episode'])
            for resolution in data['resolutions']:
                response += '  [{}] {}\n'.format(
                    resolution['resolution'],
                    resolution['torrent'])
        if not response:
            response = 'Can\' find what your are looking for :('
        return response

    def parse_shedule(self, content):
        results = {}
        soup = BeautifulSoup(content)
        div = soup.find('h2', class_='weekday')
        while True:
            weekday = div.text.strip()
            if weekday not in results:
                results[weekday] = {}
            while True:
                div = div.nextSibling
                if div.name == 'h2':
                    break
                elif div.name == 'div':
                    results[weekday][div.text[:-5].strip()] = div.text[-5:]
            if div.text.strip() == 'To be scheduled':
                break
        return results

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
        if not self.storage['new']:
            return 'No new releases right now, come back later'
        response = 'Latest releases:\n'
        response += self.format_response(self.storage['new'][:5])
        return response

    def search(self, message, query):
        try:
            content = self.make_request('lib/search.php', value=query)
        except RequestException as e:
            return unicode(e)
        data = self.parse_list(content)
        response = 'Releases for {}:\n'.format(query)
        response += self.format_response(data[:5])
        return response

    def subscribe(self, message, name):
        if name not in self.storage['anime']:
            if self.name not in message.sender.storage:
                message.sender.storage[self.name] = {
                    'subscibe': []
                }
            message.sender.storage[self.name]['subscibe'].append(name)
            return 'This release is not supported, try !hs schedule to find' \
                   ' what you are looking for'
        return 'You successfully subscribed to {}'.format(name)

    def unsubscribe(self, message, name):
        releases = message.sender.storage.get(self.name, {}).get(
            'subscibe', [])
        if name in releases:
            releases.remove(name)
            return 'You successfully unsubscribed to {}'.format(name)
        else:
            return 'Release {} not found in you subscibtions, type' \
                   ' !hs subscribed to see them'.format(name)

    def schedule(self, message):
        if not self.storage['schedule']:
            return 'Schedule is empty, come back later'
        response = ''
        for weekday, animes in self.storage['schedule'].iteritems():
            response += '{}\n'.format(weekday)
            for anime_name, anime_time in animes.iteritems():
                response += '* {} - {}\n'.format(anime_name, anime_time)
        return response

    def subscribed(self, message):
        releases = message.sender.storage.get(self.name, {}).get(
            'subscibe', [])
        if releases:
            return '\n'.join(releases)
        return 'You haven\'t subscribed yet to any release'
