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

import json
import yaml
from os.path import basename
from functools import partial
from collections import OrderedDict

from .fs import Node, DocumentIndexer
from .engine import Markment
from .views import TemplateContext
from .events import before, after


class Project(object):
    metadata_filename = '.markment.yml'

    def __init__(self, path):
        self.path = path

        self.node = Node(path)
        self.tree = DocumentIndexer(path)
        self.name = basename(path)
        self.version = ''
        self.description = ''

        documentation_index_fallback = 'README.md'

        found = self.node.grep(r'\.(md|markdown)')

        if found:
            documentation_index_fallback = found[0].basename

        self.meta = {
            'project': {
                'name': self.name,
            },
            'documentation': {
                'index': documentation_index_fallback
            }
        }
        self._found_files = []
        self.load(path)

    def load(self, path):
        metadata = self.parse_metadata(path)

        self.meta.update(metadata)

        p = self.meta['project']
        self.name = p.get('name', self.name)
        self.version = p.get('version', self.version)
        self.description = p.get('description', self.description)
        self.github_url = p.get('github_url', '')

        tarball_fallback = zipball_fallback = ''

        if self.github_url:
            tarball_fallback = '{0}/archive/master.tar.gz'.format(self.github_url)
            zipball_fallback = '{0}/archive/master.zip'.format(self.github_url)

        self.zipball_download_url = p.get('zipball_download_url', zipball_fallback)
        self.tarball_download_url = p.get('tarball_download_url', tarball_fallback)

    def parse_metadata(self, path):
        if not self.node.contains(self.metadata_filename):
            return {}

        with self.node.open(self.metadata_filename) as f:
            data = f.read()

        return yaml.load(data.decode('utf-8'))

    def find_markdown_files(self):
        if self._found_files:
            return self._found_files

        for_blobs = lambda info: info['type'] == 'blob'
        blobs = filter(for_blobs, self.tree.find_all_markdown_files())

        for info in blobs:
            name = info['relative_path']
            self._found_files.append(info)

        return self._found_files


    def get_master_index(self):
        """returns the master index, respecting any existing toc"""
        original_master_index = self.find_markdown_files()
        master_index = []
        table_of_contents = self.meta.get('toc', [])
        for toc_item in table_of_contents:
            for item in original_master_index:
                if toc_item == item['relative_path']:
                    master_index.append(item)

        for item in original_master_index:
            if item not in master_index:
                master_index.append(item)

        return master_index

    def pre_render(self, theme, static_url_cb, link_cb, **kw):
        master_index = self.get_master_index()
        total_indexes = len(master_index)
        for position, info in enumerate(master_index, start=1):
            partial_link_cb = partial(link_cb, current_document_info=info)
            before.rendering_markdown.shout(
                info, theme, kw, position, total_indexes)

            info['extra'] = kw
            info['markment'] = md = self.load_markment(
                info, partial_link_cb, **kw)
            info['markdown'] = md.raw
            info['indexes'] = md.index()
            info['documentation'] = md.rendered

            info.update(self.render_html_from_markdown_info(
                        md, info, theme,
                partial(static_url_cb, current_document_info=info),
                partial_link_cb, [], **kw))

            after.partially_rendering_markdown.shout(
                info, theme, kw, position, total_indexes, master_index)

    def post_render(self, theme, static_url_cb, link_cb, **kw):
        master_index = self.get_master_index()
        total_indexes = len(master_index)
        for position, info in enumerate(master_index, start=1):
            info.update(self.render_html_from_markdown_info(
                        info['markment'], info, theme,
                partial(static_url_cb, current_document_info=info),
                partial(link_cb, current_document_info=info), master_index, **kw))
            after.rendering_markdown.shout(
                info, theme, kw, position, total_indexes, master_index)

        return master_index
    def generate(self, theme, static_url_cb=None, link_cb=None, **kw):
        if not static_url_cb:
            static_url_cb = lambda link, *a, **kw: link

        if not link_cb:
            link_cb = lambda link, *a, **kw: link

        self.pre_render(theme, static_url_cb, link_cb, **kw)

        # rendering again, now with the full master_index
        return self.post_render(theme, static_url_cb, link_cb, **kw)

    def load_markment(self, info, link_cb, **kw):
        with self.node.open(info['path']) as f:
            data = f.read()

        try:
            decoded = data.decode('utf-8')
        except UnicodeEncodeError:
            decoded = data

        return Markment(decoded, url_prefix=link_cb)

    def render_html_from_markdown_info(
            self, md, info, theme, static_url_cb, link_cb, master_index, **kw):

        Context = TemplateContext(
            project=self.meta['project'],
            meta=self.meta,
            documentation=md.rendered,
            index=md.index(),
            master_index=list(master_index),
            json=json,
            static_url_cb=static_url_cb,
            link_cb=link_cb,
            info=info,
            current=info,
            **kw)

        ctx = Context.ready_to_render()
        before.rendering_html.shout(info, ctx)
        info['html'] = theme.render(**ctx).encode('utf-8')
        after.rendering_html.shout(info, ctx)
        return info

    @classmethod
    def discover(cls, path, *args, **kw):
        return cls(path, *args, **kw)

    def __repr__(self):
        return '<Project({0})>'.format(repr(self.path))
