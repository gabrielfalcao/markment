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
import re


class TemplateContext(object):
    link_regex = re.compile(r'[.](md|markdown)$', re.I)

    def __init__(self, static_url_cb=None, link_cb=None, **data):
        self.data = data
        if callable(static_url_cb):
            self.static_file = static_url_cb
        if callable(link_cb):
            self.link = link_cb

    def static_file(self, name):
        return "./{0}".format(name.lstrip('/'))

    def link(self, path):
        if self.link_regex.search(path):
            return './{0}'.format(self.link_regex.sub('.html', path))

        return path

    def ready_to_render(self):
        ctx = {}
        ctx['link'] = self.link
        ctx['static_file'] = self.static_file

        ctx.update(self.data)

        return ctx
