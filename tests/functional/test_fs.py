# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from markment.fs import Node

from .base import LOCAL_FILE as L


def test_reduce_to_base_path():
    ("Node#reduce_to_base_path(path) should return the approriate path")

    result = Node(L('fixtures/img/logo.png')).reduce_to_base_path("../../img/logo.png")
    result.should.equal((L('fixtures'), 'img/logo.png', '../..'))


def test_node_depth_of():
    ("Node#depth_of(path) should return the approriate number")

    path = L()
    (Node(path).depth_of(L('fixtures/img/logo.png')).should.equal(2))
    (Node(path).depth_of(L('fixtures/img/')).should.equal(2))
    (Node(path).depth_of(L('fixtures/img')).should.equal(2))

    path = L().rstrip('/')
    (Node(path).depth_of(L('fixtures/img/logo.png')).should.equal(2))
    (Node(path).depth_of(L('fixtures/img/')).should.equal(2))
    (Node(path).depth_of(L('fixtures/img')).should.equal(2))

    path = L() + "///"
    (Node(path).depth_of(L('fixtures/img/logo.png')).should.equal(2))
    (Node(path).depth_of(L('fixtures/img/')).should.equal(2))
    (Node(path).depth_of(L('fixtures/img')).should.equal(2))


def test_node_path_to_related_in_subtree_deep_in_it():
    ("Node#path_to_related(path) should return the "
     "approriate number when really deep in a subtree")

    source_path = L('fixtures/img/logo.png')
    requesting_path = L('fixtures/docs/even/deeper/item.md')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../../../img/logo.png")


def test_node_path_to_related_in_subtree():
    ("Node#path_to_related(path) should return the "
     "approriate number when in a subtree")

    source_path = L('fixtures/img/logo.png')
    requesting_path = L('fixtures/docs/strings.md')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../img/logo.png")


def test_node_path_to_related():
    ("Node#path_to_related(path) should return the approriate path")

    source_path = L('fixtures/img/logo.png')
    requesting_path = L('fixtures/index.md')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("./img/logo.png")


def test_node_non_existing_path_to_related_in_subtree_deep_in_it():
    ("Node#path_to_related(path) should return the "
     "approriate number when really deep in a subtree "
     "even when it does not exist")

    source_path = L('fixtures/img/404.png')
    requesting_path = L('fixtures/docs/even/deeper/item.markdown')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../../../img/404.png")


def test_node_non_existing_path_to_related_in_subtree():
    ("Node#path_to_related(path) should return the "
     "approriate number when in a subtree"
     "even when it does not exist")

    source_path = L('fixtures/img/404.png')
    requesting_path = L('fixtures/docs/strings.markdown')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("../img/404.png")


def test_node_non_existing_path_to_related():
    ("Node#path_to_related(path) should return the approriate path"
     "even when it does not exist")

    source_path = L('fixtures/img/404.png')
    requesting_path = L('fixtures/index.markdown')

    result = Node(source_path).path_to_related(requesting_path)
    result.should.equal("./img/404.png")
