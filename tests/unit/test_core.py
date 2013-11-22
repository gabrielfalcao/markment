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
from markment.core import Project


def test_get_master_index():
    ("Project#get_master_index should return an index that respects the "
     "table of contents declared in the markment.yml file")

    # Given a project class that has a hardcoded toc declaration
    class MyProject(Project):
        def __init__(self):
            self.meta = {
                'toc': [
                    'some/dir/2/file.md',
                    'second.md',
                    'third/thing.md',
                ],
            }

        def find_markdown_files(self):
            return [
                {
                    'relative_path': 'one-of-the/last-ones.md',
                    'type': 'blob',
                },
                {
                    'relative_path': 'another.md',
                    'type': 'blob',
                },
                {
                    'relative_path': 'second.md',
                    'type': 'blob',
                },
                {
                    'relative_path': 'some/dir/2/file.md',
                    'type': 'blob',
                },
                {
                    'relative_path': 'third/thing.md',
                    'type': 'blob',
                },
            ]

    # When I get the master index
    result = MyProject().get_master_index()

    # Then it should return them ordered by toc
    result.should.equal([
        {
            'relative_path': 'some/dir/2/file.md',
            'type': 'blob',
        },
        {
            'relative_path': 'second.md',
            'type': 'blob',
        },
        {
            'relative_path': 'third/thing.md',
            'type': 'blob',
        },
        {
            'relative_path': 'one-of-the/last-ones.md',
            'type': 'blob',
        },
        {
            'relative_path': 'another.md',
            'type': 'blob',
        },
    ])
