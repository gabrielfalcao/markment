#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <markment - markdown-based documentation generator for python>
# Copyright (C) <2013>  Gabriel Falc達o <gabriel@nacaolivre.org>
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
import re
from markment.events import after
from markment.fs import Node
from shutil import copy2


@after.all
def generate_index(event, args, project, theme, generated):
    destination = Node(args.OUTPUT)
    index = project.meta['documentation']['index']
    if index.lower().strip() == 'index.md':
        return

    renamed = re.sub(r'[.](md|markdown)$', '.html', index, re.I)
    src = destination.join(renamed)
    dst = destination.join('index.html')
    copy2(src, dst)
