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
from speakers import Speaker

EVENTS = [
    'all',
    'folder_indexed',
    'file_indexed',
    'file_copied',
    'missed_file',
    'folder_created',
    'theme_file_found',
    'project_file_found',
    'markdown_table',
    'markdown_link',
    'markdown_image',
    'markdown_header',
    'markdown_code',
    'document_found',
    'html_persisted',
    'partially_rendering_markdown',
    'rendering_markdown',
    'rendering_html',
]

before = Speaker('before', EVENTS)
after = Speaker('after', EVENTS)
