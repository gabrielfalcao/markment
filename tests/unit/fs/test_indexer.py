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

from mock import Mock, patch
from markment.fs import DocumentIndexer


@patch('markment.fs.exists')
def test_find_all_markdown_in_shallow_repo(exists):
    "DocumentIndexer#find_all_markdown_files() in a folder with no child nodes"

    origin = '/foo/bar'
    maker = DocumentIndexer(origin)
    maker.node = Mock(path='/weeee')
    maker.node.relative.side_effect = lambda x: "relative[{0}]".format(x)

    markdown_node = Mock()
    markdown_node.dir.path = '/ccc/aaa'
    markdown_node.path = '/FFF/000'
    maker.node.grep.return_value = [markdown_node]
    files = list(maker.find_all_markdown_files())
    files.should.equal([{
        u'path': u'/ccc/aaa',
        u'type': u'tree',
        u'relative_path': u'relative[/ccc/aaa]'
    },
    {
        u'path': u'/FFF/000',
        u'type': u'blob',
        u'relative_path': u'relative[/FFF/000]'
    }
    ])

    repr(maker).should.equal('<markment.fs.DocumentIndexer(path=/weeee)>')
