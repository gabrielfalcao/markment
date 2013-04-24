#!/usr/bin/env python
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
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter


class MarkmentRenderer(HtmlRenderer, SmartyPants):
    def setup(self):
        super(MarkmentRenderer, self).setup()
        self.markment_indexes = []

    def last_index_plus_child(self):
        last_index = self.markment_indexes[-1]
        if 'child' not in last_index:
            last_index['child'] = []

        return last_index['child']

    def header(self, text, level):
        t = str(text)
        t = re.sub(r'^[# ]*(.*)', '\g<1>', t)
        t = re.sub(r'`([^`]*)`', '\033[1;33m\g<1>\033[0m', t)
        item = {
            'text': t,
            'level': int(level),
        }
        indexes = self.markment_indexes
        if level > 1:
            indexes = self.last_index_plus_child()

        indexes.append(item)

    def block_code(self, text, lang):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
        else:
            lexer = guess_lexer(text, stripall=True)

        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


class Markment(object):
    compiled = None

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
        self.compile()

    def compile(self):
        if self.compiled:
            return

        self.compiled = self.markdown.render(self.raw)

    def index(self):
        return deepcopy(self.renderer.markment_indexes)
