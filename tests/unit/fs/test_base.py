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

from mock import patch
from markment.fs import isfile, isdir


@patch('markment.fs.isdir_base')
def test_isdir_when_exists(isdir_base):
    ("markment.fs.isdir should return os.path.isdir when given path exists")

    isdir_base.return_value = "yeah!"
    isdir("/foo", True).should.equal("yeah!")

    isdir_base.assert_called_once_with("/foo")


@patch('markment.fs.isfile_base')
def test_isfile_when_exists(isfile_base):
    ("markment.fs.isfile should return os.path.isfile when given path exists")

    isfile_base.return_value = "yeah!"
    isfile("/foo", True).should.equal("yeah!")

    isfile_base.assert_called_once_with("/foo")
