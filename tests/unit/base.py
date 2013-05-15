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
import os as _os
from markment.fs import Node as BaseNode
from markment.fs import isfile, isdir

from mock import MagicMock, Mock


def MARKDOWN(m):
    """The tests below have 4 spaces of indentation in the beginning,
    so this function dedents it and strips the final result"""

    return "\n".join(s[4:] for s in m.splitlines()).strip()


class FakeFile(MagicMock):
    def __init__(self, path=None, mode=None, *args, **kw):
        super(FakeFile, self).__init__(path, mode, *args, **kw)
        self.path = path
        self.mode = mode
        self.write = Mock()

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        if value:
            raise value


class FakeNode(BaseNode):
    refcount = 0

    def __init__(self, path):
        FakeNode.refcount += 1
        self.path = "/{0}".format(path.strip('/'))
        self.path_regex = '^{0}'.format(self.path)
        self.is_file = isfile(path, False)
        self.is_dir = isdir(path, False)
        self.exists = False
        self.metadata = Mock()
        self.metadata.atime = FakeNode.refcount
        self.metadata.ctime = FakeNode.refcount
        self.metadata.mtime = FakeNode.refcount

    @property
    def parent(self):
        path = _os.path.dirname(_os.path.join(self.path))
        return FakeNode(path)

    def could_be_updated_by(self, other):
        return other.metadata.mtime > self.metadata.mtime

    def join(self, other):
        return _os.path.join(self.path, other)

    def open(self, *args, **kw):
        return FakeFile(*args, **kw)

    def find(self, path):
        return FakeNode(self.join(path))
