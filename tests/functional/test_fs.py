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

from markment.fs import Node

from .base import LOCAL_FILE as L


def test_node_depth_of():
    ("Node#depth_of(path) should return the approriate number")

    path = L()
    (Node(path).depth_of(L('sandbox_simple/img/logo.png')).should.equal(2))
    (Node(path).depth_of(L('sandbox_simple/img/')).should.equal(2))
    (Node(path).depth_of(L('sandbox_simple/img')).should.equal(2))

    path = L().rstrip('/')
    (Node(path).depth_of(L('sandbox_simple/img/logo.png')).should.equal(2))
    (Node(path).depth_of(L('sandbox_simple/img/')).should.equal(2))
    (Node(path).depth_of(L('sandbox_simple/img')).should.equal(2))

    path = L() + "///"
    (Node(path).depth_of(L('sandbox_simple/img/logo.png')).should.equal(2))
    (Node(path).depth_of(L('sandbox_simple/img/')).should.equal(2))
    (Node(path).depth_of(L('sandbox_simple/img')).should.equal(2))


def test_node_path_to_related_in_subtree_deep_in_it():
    ("Node#path_to_related(path) should return the "
     "approriate number when really deep in a subtree")

    source_path = L('sandbox_simple/img/logo.png')
    requesting_path = L('sandbox_simple/docs/even/deeper/item.md')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../../../img/logo.png")


def test_node_path_to_related_in_subtree():
    ("Node#path_to_related(path) should return the "
     "approriate number when in a subtree")

    source_path = L('sandbox_simple/img/logo.png')
    requesting_path = L('sandbox_simple/docs/strings.md')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../img/logo.png")


def test_node_path_to_related():
    ("Node#path_to_related(path) should return the approriate path")

    source_path = L('sandbox_simple/img/logo.png')
    requesting_path = L('sandbox_simple/index.md')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("./img/logo.png")


def test_node_non_existing_path_to_related_in_subtree_deep_in_it():
    ("Node#path_to_related(path) should return the "
     "approriate number when really deep in a subtree "
     "even when it does not exist")

    source_path = L('sandbox_simple/img/404.png')
    requesting_path = L('sandbox_simple/docs/even/deeper/item.markdown')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../../../img/404.png")


def test_node_non_existing_path_to_related_in_subtree():
    ("Node#path_to_related(path) should return the "
     "approriate number when in a subtree"
     "even when it does not exist")

    source_path = L('sandbox_simple/img/404.png')
    requesting_path = L('sandbox_simple/docs/strings.markdown')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../img/404.png")


def test_node_non_existing_path_to_related():
    ("Node#path_to_related(path) should return the approriate path"
     "even when it does not exist")

    source_path = L('sandbox_simple/img/404.png')
    requesting_path = L('sandbox_simple/index.markdown')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("./img/404.png")
