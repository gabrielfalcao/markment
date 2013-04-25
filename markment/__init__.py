# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from copy import deepcopy
from misaka import HtmlRenderer, SmartyPants, Markdown
from misaka import (
    EXT_FENCED_CODE,
    EXT_NO_INTRA_EMPHASIS,
    EXT_SUPERSCRIPT,
    EXT_AUTOLINK,
    HTML_USE_XHTML,
    HTML_SMARTYPANTS,
)
from lxml import html as lhtml
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter


def slugify(text):
    return re.sub(r'\W', '-', text.strip().lower())


class MarkmentRenderer(HtmlRenderer, SmartyPants):
    def setup(self):
        super(MarkmentRenderer, self).setup()
        self.markment_indexes = []
        self.relative_url_prefix = None
        self.code_count = {'text': ''}

    def last_index_plus_child(self, level):
        indexes = self.markment_indexes

        for _ in range(level):
            last_index = indexes[-1]
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
        needs_prefix = not link.startswith('http')

        if not needs_prefix or not self.relative_url_prefix:
            return ''

        if needs_prefix:
            prefix = self.relative_url_prefix.rstrip('/') + '/'

        return prefix + link.lstrip('/')

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
        return element

    def link(self, link, title, content):
        url = link
        prefixed = self.prefix_link_if_needed(link)
        if prefixed:
            url = prefixed

        element = '<a href="{0}" title="{1}">{2}</a>'.format(
            url,
            title,
            content,
        )
        return element

    def header(self, text, level):
        item = {
            'text': str(text),
            'anchor': '#{0}'.format(slugify(text)),
            'level': int(level),
        }
        indexes = self.markment_indexes
        if level > 1:
            indexes = self.last_index_plus_child(level - 1)

        indexes.append(item)
        return '<h{level} id="{slug}" name="{slug}"><a href="#{slug}">{text}</a></h{level}>'.format(
            level=level,
            text=text,
            slug=slugify(text)
        )

    def add_attributes_to_code(self, code):
        dom = lhtml.fromstring(code)
        pre = dom.cssselect("div.highlight pre")[0]
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
        return self.add_attributes_to_code(highlight(text, lexer, formatter))


class Markment(object):
    extensions = (EXT_FENCED_CODE |
                  EXT_NO_INTRA_EMPHASIS |
                  HTML_SMARTYPANTS |
                  EXT_AUTOLINK |
                  EXT_SUPERSCRIPT |
                  HTML_USE_XHTML)

    def __init__(self, markdown, renderer=None, relative_url_prefix=None):
        self.raw = markdown
        self.renderer = renderer or MarkmentRenderer()
        self.renderer.relative_url_prefix = relative_url_prefix
        self.markdown = Markdown(
            self.renderer,
            extensions=self.extensions,
        )
        self.rendered = self.compile()

    def compile(self):
        return self.markdown.render(self.raw)

    def index(self):
        return deepcopy(self.renderer.markment_indexes)
