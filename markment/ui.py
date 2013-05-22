# -*- coding: utf-8 -*-
# <markment - markdown-based documentation generator for python>
# Copyright (C) <2013>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
from .fs import Node, LOCAL_FILE, join

THEME_ROOT = LOCAL_FILE('themes')


class Theme(object):
    index_filename = 'markment.yml'

    def __init__(self, path):
        self.node = Node(path)
        self.loader = FileSystemLoader(self.node.dir.path)
        self.environment = Environment(loader=self.loader)
        self._index = {}

    @property
    def path(self):
        return self.node.path

    def static_file(self, *path):
        return join(self.index['static_path'], *path)

    def get_template(self):
        return self.environment.get_template(self.index['index_template'])

    def render(self, **kw):
        template = self.get_template()
        return template.render(**kw)

    def _load_file_contents(self, path):
        "Loads the bytes of a file and decode as utf-8"
        with self.node.open(path) as template:
            content = template.read()

        try:
            return content.decode('utf-8')
        except UnicodeEncodeError:
            return content

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
        node = Node(path)
        if not node.contains(cls.index_filename):
            m = ('The folder "{0}" should contain a {1} file but '
                 'doesn\'t'.format(node.path, cls.index_filename))

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
