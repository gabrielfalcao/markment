#!/usr/bin/env python
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
from markment.registry import CALLBACK_REGISTRY


class Main(object):
    def __init__(self, callback):
        self.name = callback

    @classmethod
    def _add_method(cls, name, where, when):
        def method(self, fn):
            CALLBACK_REGISTRY.append_to(where, when % {'0': self.name}, fn)
            return fn

        method.__name__ = method.fn_name = name
        setattr(cls, name, method)

for name, where, when in [
        (b'all', 'all', '%(0)s'),
        (b'project_file_found', 'project_file_found', '%(0)s_each'),
        (b'folder_indexed', 'folder_indexed', '%(0)s_each'),
        (b'file_indexed', 'file_indexed', '%(0)s_each'),
        (b'folder_created', 'folder_created', '%(0)s_each'),
        (b'asset_folder_created', 'folder_created', '%(0)s_each'),
        (b'asset_file_copied', 'asset_file_copied', '%(0)s_each'),
        (b'markdown_table', 'markdown_table', '%(0)s_each'),
        (b'markdown_link', 'markdown_link', '%(0)s_each'),
        (b'markdown_image', 'markdown_image', '%(0)s_each'),
        (b'markdown_header', 'markdown_header', '%(0)s_each'),
        (b'markdown_code', 'markdown_code', '%(0)s_each'),
        (b'document_found', 'document_found', '%(0)s_each'),
        (b'html_persisted', 'html_persisted', '%(0)s_each')]:
    Main._add_method(name, where, when)

before = Main(b'before')
after = Main(b'after')
