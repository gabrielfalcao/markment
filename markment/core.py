# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import yaml

from collections import OrderedDict

from .fs import PathWalker, TreeMaker
from .engine import Markment
from .views import TemplateContext


class Project(object):
    metadata_filename = '.markment.yml'

    def __init__(self, path):
        self.path = path
        self.walker = PathWalker(path)
        self.tree = TreeMaker(path)
        self.meta = {}
        self._found_files = OrderedDict()
        self.load(path)

    def load(self, path):
        metadata = self.parse_metadata(path)

        self.meta.update(metadata)

        p = metadata['project']
        self.name = p['name']
        self.version = p['version']
        self.description = p['description']

    def parse_metadata(self, path):
        with self.walker.open(self.metadata_filename) as f:
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
        with self.walker.open(info['path']) as f:
            data = f.read()

        decoded = data.decode('utf-8')
        md = Markment(decoded)

        info['markdown'] = md.raw
        info['indexes'] = md.index()
        info['documentation'] = md.rendered

        Context = TemplateContext(
            project=self,
            documentation=md.rendered,
            index=md.index(),
            master_index=list(master_index),
            json=json,
            **kw)

        ctx = Context.ready_to_render(static_prefix=static_prefix)
        info['html'] = theme.render(**ctx)
        return info

    @classmethod
    def discover(cls, path):
        return cls(path)

    def __repr__(self):
        return '<Project({0})>'.format(repr(self.path))
