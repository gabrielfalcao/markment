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

import traceback
from os.path import relpath
from markment.events import after, before

W = lambda x: relpath(x)


@before.exception_handler
@after.exception_handler
def print_out(event, exception, args, kw):
    print "Exception:", traceback.format_exc(exception)


@after.file_indexed
def file_indexed(event, info, pos, total, siblings):
    print "[FILE INDEXED]:{0}".format(info['relative_path'])


@after.partially_rendering_markdown
def partialy_render_md(event, info, theme, kw, pos, total, siblings):
    print "[PRE-RENDERING MARKDOWN]:{0}".format(info['relative_path'])


@after.rendering_markdown
def render_md(event, info, theme, kw, pos, total, siblings):
    print "[RENDERING MARKDOWN]:{0}".format(info['relative_path'])


@after.html_persisted
def html_persisted(event, destination_path, raw_bytes, position, total):
    print "[HTML PERSISTED {2} of {3}]:{0}:{1}bytes".format(destination_path, len(raw_bytes), position, total)


@after.file_copied
def after_copy_file(event, source_path, destiny_path, pos, total):
    print "[FILE COPIED {2} of {3}]:{0} to {1}".format(source_path, destiny_path, pos, total)


@after.missed_file
def missed_file(event, path):
    print "[MISSED FILE]:{0}".format(path)
