from __future__ import unicode_literals

import os.path

import ujson


class StorageObject(object):

    def serialize(self):
        raise NotImplementedError()

    def unserialize(self):
        raise NotImplementedError()


class Storage(object):

    def __init__(self, app):
        self.app = app
        self.data = None
        self.open()

    def open(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def serialize(self, data):
        return data


class FileStorage(Storage):

    def open(self):
        if not os.path.isdir(os.path.dirname(self.app.config['STORAGE_FILE'])):
            os.makedirs(os.path.dirname(self.app.config['STORAGE_FILE']))
        if os.path.isfile(self.app.config['STORAGE_FILE']):
            with open(self.app.config['STORAGE_FILE']) as storage_file:
                self.data = ujson.load(storage_file)
        else:
            self.data = {}

    def save(self):
        with open(self.app.config['STORAGE_FILE'], 'w') as storage_file:
            ujson.dump(self.data, storage_file)
