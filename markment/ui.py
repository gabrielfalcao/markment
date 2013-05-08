# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import yaml
from jinja2 import Template
from .fs import Node, LOCAL_FILE, join

THEME_ROOT = LOCAL_FILE('themes')


class Theme(object):
    index_filename = 'markment.yml'

    def __init__(self, path):
        self.node = Node(path)
        self._index = {}

    @property
    def path(self):
        return self.node.path

    def static_file(self, *path):
        return join(self.index['static_path'], *path)

    def get_template_content(self):
        return self._load_file_contents(self.index['index_template'])

    def get_template(self):
        return Template(self.get_template_content())

    def render(self, **kw):
        template = self.get_template()
        return template.render(**kw)

    def _load_file_contents(self, path):
        "Loads the bytes of a file and decode as utf-8"
        with self.node.open(path) as template:
            content = template.read()

        return content.decode('utf-8')

    @property
    def index(self):
        if not self._index:
            self._index = self.calculate_index()

        return self._index

    def calculate_index(self):
        index = self._load_file_contents(self.index_filename)
        parsed = yaml.load(index)
        parsed['static_path'] = self.node.join(parsed.get('static_path', 'assets'))
        return parsed

    @classmethod
    def load_from_path(cls, path):
        if not Node(path).contains(cls.index_filename):
            m = ('The folder "{0}" should contain a {1} file but '
                 'doesn\'t'.format(path, cls.index_filename))

            raise InvalidThemePackage(m)

        return cls(path)

    @classmethod
    def load_by_name(cls, name):
        path = join(THEME_ROOT, name)
        if not Node(THEME_ROOT).contains(name):
            m = 'Markment does not have a builtin theme called "{0}"'
            raise InvalidThemePackage(m.format(name))

        return cls.load_from_path(path)


class InvalidThemePackage(Exception):
    pass
