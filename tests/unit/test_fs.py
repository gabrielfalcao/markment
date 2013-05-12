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

from mock import Mock, patch, call
from markment.fs import Node, isfile, isdir, DotDict


def test_node_could_be_updated_by_true():
    ("Node#could_be_updated_by returns True if given "
     "node has a newer modification time")

    nd = Node(__file__)
    nd.metadata.mtime = 0
    other = Mock()
    other.metadata.mtime = 1000
    nd.could_be_updated_by(other).should.be.true


def test_node_could_be_updated_by_false():
    ("Node#could_be_updated_by returns False if given "
     "node has an older modification time")

    nd = Node(__file__)
    nd.metadata.mtime = 1000
    other = Mock()
    other.metadata.mtime = 0
    nd.could_be_updated_by(other).should.be.false


def test_node_relative():
    ("Node#relative() returns a path relative to the base")

    nd = Node("/foo/bar/")
    nd.relative('/foo/bar/yes.py').should.equal('yes.py')


@patch('markment.fs.os')
def test_trip_at_when_lazy_absolute(os):
    ("Node#trip_at(path, lazy=True) returns a generator when lazy=True "
     "(testing with absolute path)")
    os.walk.return_value = [
        ("/dummy/", [], ["file1.py", "file2.py"]),
    ]

    nd = Node("/foo/bar/")
    nd.trip_at('/dummy/', lazy=True).should.be.a('types.GeneratorType')
    list(nd.trip_at('/dummy/', lazy=True)).should.equal([
        "/dummy/file1.py",
        "/dummy/file2.py",
    ])


@patch('markment.fs.os')
def test_trip_at_when_not_lazy_absolute(os):
    ("Node#trip_at(path, lazy=False) returns a list when lazy=False "
     "(testing with absolute path)")
    os.walk.return_value = [
        ("/dummy/", [], ["file1.py", "file2.py"]),
    ]

    nd = Node("/foo/bar/")
    nd.trip_at('/dummy/', lazy=False).should.equal([
        "/dummy/file1.py",
        "/dummy/file2.py",
    ])


@patch('markment.fs.os')
def test_trip_at_when_lazy_relative(os):
    ("Node#trip_at(path, lazy=True) returns a generator when lazy=True "
     "(testing with relative path)")
    os.walk.return_value = [
        ("/dummy/", [], ["file1.py", "file2.py"]),
    ]

    nd = Node("/foo/bar/")
    nd.trip_at('/dummy/', lazy=True).should.be.a('types.GeneratorType')
    list(nd.trip_at('/dummy/', lazy=True)).should.equal([
        "/dummy/file1.py",
        "/dummy/file2.py",
    ])


@patch('markment.fs.os')
def test_trip_at_when_not_lazy_relative(os):
    ("Node#trip_at(path, lazy=False) returns a list when lazy=False "
     "(testing with relative path)")
    os.walk.return_value = [
        ("/foo/bar/somewhere", [], ["file1.py", "file2.py"]),
    ]

    nd = Node("/foo/bar/")
    nd.trip_at('somewhere', lazy=False).should.equal([
        "/foo/bar/somewhere/file1.py",
        "/foo/bar/somewhere/file2.py",
    ])


def test_walk_trips_at_node_path():
    ("Node#walk() trips at node.path")
    nd = Node("/foo/bar/")
    nd.trip_at = Mock()

    nd.walk()
    nd.walk(lazy=True)

    nd.trip_at.assert_has_calls([
        call('/foo/bar', lazy=False),
        call('/foo/bar', lazy=True),
    ])


def test_dot_dict():
    "DotDict allows accessing keys with dots"
    d = DotDict({'foo': 'bar', 'number': 42})
    d.foo.should.equal('bar')
    d.number.should.equal(42)


def test_node_basename():
    ("Node#basename should return the basename for the node.path")
    nd = Node(__file__)
    nd.basename.should.equal('test_fs.py')


@patch('markment.fs.os')
def test_node_list(os):
    ("Node#list should return a list containing one node "
     "per file found inside of the current node")
    os.listdir.return_value = ['/foo/bar/items/whatever.py']

    nd = Node('/foo/bar/items/')
    nd.list().should.have.length_of(1)

    os.listdir.assert_called_with('/foo/bar/items')


def test_node_dir_when_is_file():
    ("Node#dir should return a node pointing to the parent "
     "dir when the current node is pointing to a file")

    nd = Node('/foo/bar/items/some.py')
    nd.dir.path.should.equal('/foo/bar/items')


def test_node_dir_when_is_dir():
    ("Node#dir should return itself when the current "
     "node is pointing to a file")

    nd = Node('/foo/bar/items/')
    nd.dir.path.should.equal('/foo/bar/items')


@patch('markment.fs.exists')
@patch('markment.fs.isfile_base')
def test_isfile_if_path_exists(isfile_base, exists):
    ('fs.isfile returns result from os.path.isfile if path exists')
    exists.return_value = True

    isfile('foobar').should.equal(isfile_base.return_value)
    isfile_base.assert_called_with('foobar')


@patch('markment.fs.exists')
@patch('markment.fs.isfile_base')
def test_isfile_if_path_doesnt_exists_and_has_dot(isfile_base, exists):
    ('fs.isfile returns result from os.path.isfile if path doesnt '
     'exist and name has a dot')
    exists.return_value = False

    isfile('foobar.py').should.equal(True)


@patch('markment.fs.exists')
@patch('markment.fs.isfile_base')
def test_isfile_if_path_doesnt_exists_and_hasnt_a_dot(isfile_base, exists):
    ('fs.isfile returns result from os.path.isfile if path doesnt '
     'exist and name doesnt have not a dot')
    exists.return_value = False

    isfile('foobar').should.equal(False)


@patch('markment.fs.exists')
@patch('markment.fs.isdir_base')
def test_isdir_if_path_exists(isdir_base, exists):
    ('fs.isdir returns result from os.path.isdir if path exists')
    exists.return_value = True

    isdir('foobar').should.equal(isdir_base.return_value)
    isdir_base.assert_called_with('foobar')


@patch('markment.fs.exists')
@patch('markment.fs.isdir_base')
def test_isdir_if_path_doesnt_exists_and_has_dot(isdir_base, exists):
    ('fs.isdir returns result from os.path.isdir if path doesnt '
     'exist and have not a dot')
    exists.return_value = False

    isdir('foobar.py').should.equal(False)


@patch('markment.fs.exists')
@patch('markment.fs.isdir_base')
def test_isdir_if_path_doesnt_exists_and_hasnt_a_dot(isdir_base, exists):
    ('fs.isdir returns result from os.path.isdir if path doesnt '
     'exist and name doesnt have a dot')
    exists.return_value = False

    isdir('foobar').should.equal(True)


@patch('markment.fs.isfile')
def test_node_depth_of_with_file(isfile):
    ("Node#depth_of(path) should return the approriate number")

    isfile.return_value = True
    Node("/foo/bar/").depth_of("/foo/bar/another/dir/file.py").should.equal(2)
    Node("/foo/bar").depth_of("/foo/bar/another/dir/file.py").should.equal(2)
    Node("/foo/bar//").depth_of("/foo/bar/another/dir/file.py").should.equal(2)


@patch('markment.fs.isfile')
def test_node_depth_of_with_dir(isfile):
    ("Node#depth_of(path) should return the approriate number")

    isfile.return_value = False
    Node("/foo/bar/").depth_of("/foo/bar/another/dir/").should.equal(2)
    Node("/foo/bar").depth_of("/foo/bar/another/dir/").should.equal(2)
    Node("/foo/bar///").depth_of("/foo/bar/another/dir/").should.equal(2)

    Node("/foo/bar/").depth_of("/foo/bar/another/dir").should.equal(2)
    Node("/foo/bar").depth_of("/foo/bar/another/dir").should.equal(2)
    Node("/foo/bar///").depth_of("/foo/bar/another/dir").should.equal(2)

    Node("/foo/bar/").depth_of("/foo/bar/another/dir//").should.equal(2)
    Node("/foo/bar").depth_of("/foo/bar/another/dir//").should.equal(2)
    Node("/foo/bar///").depth_of("/foo/bar/another/dir//").should.equal(2)
