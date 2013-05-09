# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch
from markment.fs import Node


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
