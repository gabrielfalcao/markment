# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re


class TemplateContext(object):
    link_regex = re.compile(r'[.](md|markdown)$', re.I)

    def __init__(self, static_prefix=None, **data):
        self.data = data
        self.static_prefix = static_prefix or './'

    def static_file(self, name):
        return "./{0}/{1}".format(self.static_prefix.strip('/'), name.lstrip('/'))

    def link(self, path):
        if self.link_regex.search(path):
            return './{0}'.format(self.link_regex.sub('.html', path))

        return path

    def ready_to_render(self, static_prefix=None):
        if static_prefix:
            self.static_prefix = static_prefix

        ctx = {}
        ctx['link'] = self.link
        ctx['static_file'] = self.static_file

        ctx.update(self.data)

        return ctx
