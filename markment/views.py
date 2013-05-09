# -*- coding: utf-8 -*-
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
