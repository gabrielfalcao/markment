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

    def header(self, text, level):
        item = {
            'text': str(text),
            'level': int(level),
        }
        indexes = self.markment_indexes
        if level > 1:
            indexes = self.last_index_plus_child(level - 1)

        indexes.append(item)
        return '<h{level} name="{slug}"><a href="#{slug}">{text}</a></h{level}>'.format(
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

    def __init__(self, markdown, renderer=None):
        self.raw = markdown
        self.renderer = renderer or MarkmentRenderer()
        self.markdown = Markdown(
            self.renderer,
            extensions=self.extensions,
        )
        self.rendered = self.compile()

    def compile(self):
        return self.markdown.render(self.raw)

    def index(self):
        return deepcopy(self.renderer.markment_indexes)
