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

from copy import deepcopy
from misaka import HtmlRenderer, SmartyPants, Markdown
from misaka import (
    EXT_FENCED_CODE,
    EXT_NO_INTRA_EMPHASIS,
    EXT_SUPERSCRIPT,
    EXT_AUTOLINK,
    EXT_TABLES,
    HTML_USE_XHTML,
    HTML_SMARTYPANTS,
)
from lxml import html as lhtml
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

from .events import after
from .handy import slugify


class MarkmentRenderer(HtmlRenderer, SmartyPants):
    def setup(self):
        super(MarkmentRenderer, self).setup()
        self.markment_indexes = []
        self.url_prefix = None
        self.code_count = {'text': '', 'count': 0}
        self.url_references = []

    def last_index_plus_child(self, level):
        indexes = self.markment_indexes

        for _ in range(level):
            try:
                last_index = indexes[-1]
            except IndexError:
                break

            if 'child' not in last_index:
                last_index['child'] = []

            indexes = last_index['child']

        return indexes

    def count_index_for_header(self, text):
        if self.code_count['text'] == text:
            self.code_count['count'] += 1
        else:
            self.code_count['text'] = text
            self.code_count['count'] = 1

        return self.code_count['count']

    def prefix_link_if_needed(self, link):
        needs_prefix = '://' not in link and not link.startswith('//')
        if not self.url_prefix:
            return ''

        if needs_prefix:
            if callable(self.url_prefix):
                prefixed = self.url_prefix(link)
            else:
                prefix = self.url_prefix.rstrip('/') + '/'
                prefixed = prefix + link.lstrip('/')

            self.url_references.append(prefixed)
        else:
            prefixed = ''

        return prefixed

    def table(self, header, body):
        table = "".join([
            '<table class="table">',
            '<thead>', header.strip(), '</thead>',
            '<tbody>', body.strip(), '</tbody>',
            '</table>',
        ])
        memory = {'element': table}
        after.shout('markdown_table', memory)
        return memory['element']

    def image(self, link, title, alt):
        url = link
        prefixed = self.prefix_link_if_needed(link)
        if prefixed:
            url = prefixed

        element = '<img src="{0}" title="{1}" alt="{2}" />'.format(
            url,
            title,
            alt
        )
        memory = {'element': element}
        after.markdown_image.shout(memory)
        return memory['element']

    def link(self, link, title, content):
        url = link
        prefixed = self.prefix_link_if_needed(link)
        if prefixed:
            url = prefixed

        element = '<a href="{0}"{1}>{2}</a>'.format(
            url,
            title and 'title="{1}"'.format(title) or '',
            content,
        )
        memory = {'element': element}
        after.markdown_link.shout(memory)
        return memory['element']

    def header(self, text, level):
        item = {
            'text': text,
            'anchor': '#{0}'.format(slugify(text)),
            'level': int(level),
        }

        indexes = self.markment_indexes
        if level > 1:
            indexes = self.last_index_plus_child(level - 1)

        indexes.append(item)
        element = '<h{level} id="{slug}" name="{slug}"><a href="#{slug}">{text}</a></h{level}>'.format(
            level=level,
            text=text,
            slug=slugify(text)
        )
        memory = {'element': element}
        after.markdown_header.shout(memory)
        return memory['element']

    def add_attributes_to_code(self, code):
        dom = lhtml.fromstring(code)
        pre = dom.cssselect("div.highlight pre")[0]
        if self.markment_indexes:
            last_header = self.markment_indexes[-1]

            slug_prefix = slugify(last_header['text'])
            pre.attrib['name'] = "{0}-example-{1}".format(
                slug_prefix,
                self.count_index_for_header(last_header['text'])
            )

        return lhtml.tostring(dom)

    def block_code(self, text, lang):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
        else:
            lexer = guess_lexer(text, stripall=True)

        formatter = HtmlFormatter()
        code = self.add_attributes_to_code(highlight(text, lexer, formatter))
        memory = {'element': code}
        after.markdown_code.shout(memory)
        return memory['element']


class Markment(object):
    extensions = (EXT_FENCED_CODE |
                  EXT_NO_INTRA_EMPHASIS |
                  HTML_SMARTYPANTS |
                  EXT_TABLES |
                  EXT_AUTOLINK |
                  EXT_SUPERSCRIPT |
                  HTML_USE_XHTML)

    def __init__(self, markdown, renderer=None, url_prefix=None):
        self.raw = markdown
        self.renderer = renderer or MarkmentRenderer()
        self.renderer.url_prefix = url_prefix
        self.markdown = Markdown(
            self.renderer,
            extensions=self.extensions,
        )
        self.rendered = self.compile()
        self.url_references = self.renderer.url_references

    def compile(self):
        return self.markdown.render(self.raw)

    def index(self):
        return deepcopy(self.renderer.markment_indexes)
