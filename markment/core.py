# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import yaml

from collections import OrderedDict

from .fs import Node, TreeMaker, dirname
from .engine import Markment
from .views import TemplateContext


class Project(object):
    metadata_filename = '.markment.yml'

    def __init__(self, path, url_prefix=None):
        self.path = path
        self.url_prefix = url_prefix or './'

        self.node = Node(path)
        self.tree = TreeMaker(path)
        self.meta = {
            'project': {
                'name': dirname(path),
            }
        }
        self._found_files = OrderedDict()
        self.load(path)

    def load(self, path):
        metadata = self.parse_metadata(path)

        self.meta.update(metadata)

        p = self.meta['project']
        self.name = p.get('name', '')
        self.version = p.get('version', '')
        self.description = p.get('description', '')

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
            self._found_files[name] = info

        return self._found_files

    def generate(self, theme, static_prefix=None, **kw):
        master_index = self.find_markdown_files().values()

        for info in master_index:
            yield self.render_html_from_markdown_info(
                info, theme, static_prefix, master_index, **kw)

    def render_html_from_markdown_info(self, info, theme, static_prefix,
                                       master_index, **kw):
        with self.node.open(info['path']) as f:
            data = f.read()

        decoded = data.decode('utf-8')
        md = Markment(decoded, url_prefix=kw.get("url_prefix", self.url_prefix))

        info['markdown'] = md.raw
        info['indexes'] = md.index()
        info['documentation'] = md.rendered

        Context = TemplateContext(
            project=self,
            documentation=md.rendered,
            index=md.index(),
            master_index=list(master_index),
            json=json,
            static_prefix=static_prefix,
            **kw)

        ctx = Context.ready_to_render()
        info['html'] = theme.render(**ctx)
        info['references'] = md.url_references
        return info

    @classmethod
    def discover(cls, path, *args, **kw):
        return cls(path, *args, **kw)

    def __repr__(self):
        return '<Project({0})>'.format(repr(self.path))
