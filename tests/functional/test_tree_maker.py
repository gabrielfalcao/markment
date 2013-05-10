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
from os.path import dirname, abspath, join
from markment.fs import TreeMaker


LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)


def test_treemaker_finds_all_files():
    ("TreeMaker should find all the markdown files in a given directory")

    tm = TreeMaker(LOCAL_FILE('fixtures'))

    files = list(tm.find_all_markdown_files())
    files.should.have.length_of(6)

    files.should.equal([
        {
            'path': LOCAL_FILE('fixtures', 'index.md'),
            'relative_path': 'index.md',
            'type': 'blob',
        },
        {
            'path': LOCAL_FILE('fixtures', 'docs'),
            'relative_path': 'docs',
            'type': 'tree',
        },
        {
            'path': LOCAL_FILE('fixtures', 'docs', 'output.md'),
            'relative_path': 'docs/output.md',
            'type': 'blob',
        },
        {
            'path': LOCAL_FILE('fixtures', 'docs', 'strings.md'),
            'relative_path': 'docs/strings.md',
            'type': 'blob',
        },
        {
            'path': LOCAL_FILE('fixtures', 'docs', 'even', 'deeper'),
            'relative_path': 'docs/even/deeper',
            'type': 'tree',
        },
        {
            'path': LOCAL_FILE('fixtures', 'docs', 'even', 'deeper', 'item.md'),
            'relative_path': 'docs/even/deeper/item.md',
            'type': 'blob',
        },
    ])
