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
from markment.fs import AssetsCloner

from tests.unit.base import FakeNode


@patch('markment.fs.shutil')
@patch('markment.fs.os')
@patch('markment.fs.exists')
@patch('markment.fs.Node')
def test_persist_with_files_to_copy_missing(
        Node, exists, os, shutil):
    ("AssetsCloner#clone_to(destination_path)"
     " when destination does not exist should create dirs")

    os.sep = '/'
    Node.side_effect = FakeNode
    exists.return_value = False

    source = AssetsCloner('/source/')
    source.node.trip_at = Mock(return_value=[
        '/source/file1.txt',
        '/source/subdir/file2.txt',
    ])
    result = source.clone_to('/destination')

    result.should.equal([
        "/destination/file1.txt",
        "/destination/subdir/file2.txt",
    ])


@patch('markment.fs.shutil')
@patch('markment.fs.os')
@patch('markment.fs.exists')
@patch('markment.fs.Node')
def test_persist_with_files_to_copy_existing(
        Node, exists, os, shutil):
    ("AssetsCloner#clone_to(destination_path)"
     " when destination already exists should not create dirs")

    os.sep = '/'
    Node.side_effect = FakeNode
    exists.return_value = True

    source = AssetsCloner('/source/')
    source.node.trip_at = Mock(return_value=[
        '/source/file1.txt',
        '/source/subdir/file2.txt',
    ])
    result = source.clone_to('/destination')

    result.should.equal([
        "/destination/file1.txt",
        "/destination/subdir/file2.txt",
    ])
