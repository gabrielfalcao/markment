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
from markment.fs import Generator

from tests.unit.base import FakeNode


def test_rename_markdown_file():
    ("Generator#rename_markdown_filename(path)")

    project = Mock()
    theme = Mock()

    gen = Generator(project, theme)
    gen.rename_markdown_filename("/bb/foo.md").should.equal('/bb/foo.html')


def test_get_levels():
    ("Generator#get_levels(link)")

    project = Mock()
    theme = Mock()

    gen = Generator(project, theme)
    fixed, levels = gen.get_levels('../../buz.py')

    fixed.should.equal('buz.py')
    levels.should.equal(['..', '..'])


@patch('markment.fs.exists')
def test_relative_link_callback_with_markdown(exists):
    ("Generator#relative_link_callback(original_link, current_document_info,"
     " destination_root) with a markdown file")

    theme = Mock()

    project = Mock()
    project.node = FakeNode("/coolproject/")

    engine = Generator(project, theme)
    destination_root = FakeNode("/output")

    value = engine.relative_link_callback(
        "../docs/index.md",
        {"relative_path": "docs/faq.md"},
        destination_root,
    )
    value.should.equal('./index.html')


@patch('markment.fs.exists')
def test_relative_link_callback_with_markdown_not_found(exists):
    ("Generator#relative_link_callback(original_link, current_document_info,"
     " destination_root) with a markdown not found [\033[2;31mthere is a TODO here\033[0m]")

    # TODO: this test should raise an exception

    theme = Mock()

    project = Mock()
    project.node = FakeNode("/coolproject/")
    project.node.find = Mock(return_value=None)

    engine = Generator(project, theme)
    destination_root = FakeNode("/output")

    value = engine.relative_link_callback(
        "../docs/index.md",
        {"relative_path": "docs/faq.md"},
        destination_root,
    )
    value.should.equal('../docs/index.md')


@patch('markment.fs.exists')
def test_relative_link_callback_with_asset_already_to_copy(exists):
    ("Generator#relative_link_callback(original_link, current_document_info,"
     " destination_root) with an asset")

    theme = Mock()

    project = Mock()
    project.node = FakeNode("/coolproject")

    engine = Generator(project, theme)
    engine.files_to_copy = [
        "/coolproject/css/style.css",
        "/css/style.css",
        "css/style.css",
        "style.css",
    ]

    destination_root = FakeNode("/output")

    value = engine.relative_link_callback(
        "css/style.css",
        {"relative_path": "docs/index.md"},
        destination_root,
    )
    value.should.equal(u'../css/style.css')


@patch('markment.fs.exists')
def test_relative_link_callback_with_asset(exists):
    ("Generator#relative_link_callback(original_link, current_document_info,"
     " destination_root) with an asset")

    theme = Mock()

    project = Mock()
    project.node = FakeNode("/coolproject")

    engine = Generator(project, theme)
    destination_root = FakeNode("/output")

    value = engine.relative_link_callback(
        "css/style.css",
        {"relative_path": "docs/index.md"},
        destination_root,
    )
    value.should.equal(u'../css/style.css')


@patch('markment.fs.exists')
def test_relative_link_callback_with_asset_not_found(exists):
    ("Generator#relative_link_callback(original_link, current_document_info,"
     " destination_root) with asset not found")

    # TODO: this test should raise an exception

    theme = Mock()

    project = Mock()
    project.node = FakeNode("/coolproject/")
    project.node.find = Mock(return_value=None)

    engine = Generator(project, theme)
    destination_root = FakeNode("/output")

    value = engine.relative_link_callback(
        "../css/style.css",
        {"relative_path": "css/faq.md"},
        destination_root,
    )
    value.should.equal('../css/style.css')


@patch('markment.fs.exists')
def test_static_url_callback_with_asset_not_found(exists):
    ("Generator#static_url_callback(original_link, current_document_info,"
     " destination_root) with asset not found")

    # TODO: this test should raise an exception
    project = Mock()

    theme = Mock()
    theme.node = FakeNode("/coolproject/")
    theme.node.find = Mock(return_value=None)

    engine = Generator(project, theme)
    destination_root = FakeNode("/output")

    engine.static_url_callback.when.called_with(
        "style.css",
        {"relative_path": "css/faq.md"},
        destination_root,
    ).should.throw(IOError, "BOOM, could not find style.css anywhere")


@patch('markment.fs.exists')
def test_static_url_callback_with_asset(exists):
    ("Generator#static_url_callback(original_link, current_document_info,"
     " destination_root) finding an asset")

    # TODO: this test should raise an exception
    project = Mock()

    theme = Mock()
    theme.node = FakeNode("/coolproject/")

    engine = Generator(project, theme)
    destination_root = FakeNode("/output")

    value = engine.static_url_callback(
        "css/style.css",
        {"relative_path": "faq.md"},
        destination_root,
    )

    value.should.equal("./css/style.css")


@patch('markment.fs.exists')
def test_static_url_callback_with_asset_with_levels(exists):
    ("Generator#static_url_callback(original_link, current_document_info,"
     " destination_root) with asset not found [\033[31mthere is a TODO here\033[0m]")

    # TODO: this test should raise an exception
    project = Mock()

    theme = Mock()
    theme.node = FakeNode("/coolproject/")

    engine = Generator(project, theme)
    destination_root = FakeNode("/output")

    value = engine.static_url_callback(
        "help.md",
        {"relative_path": "docs/index.md"},
        destination_root,
    )

    value.should.equal("../help.html")


@patch('markment.fs.io')
@patch('markment.fs.exists')
def test_persist_when_exists(io, exists):
    ("Generator#persist(destination_path)"
     " when path already exists")

    theme = Mock()
    theme.index = {'static_path': '/themes/cool'}
    project = Mock()
    project.generate.return_value = [
        {
            "type": "blob",
            "html": "<h1>Foobar</h1>",
            "markdown": "# Foobar\n",
            "path": "/simple/index.md",
            "relative_path": "./index.md",
        }
    ]

    engine = Generator(project, theme)

    generated = engine.persist("/output")

    generated.should.equal([
        "/output/index.html"
    ])


@patch('markment.fs.os')
@patch('markment.fs.io')
@patch('markment.fs.exists')
def test_persist_when_does_not_exist(exists, io, os):
    ("Generator#persist(destination_path)"
     " when path already does not exist")
    exists.return_value = False
    theme = Mock()
    theme.index = {'static_path': '/themes/cool'}
    project = Mock()
    project.generate.return_value = [
        {
            "type": "tree",
            "path": "/simple/",
            "relative_path": "./",
        },
        {
            "type": "blob",
            "html": "<h1>Foobar</h1>",
            "markdown": "# Foobar\n",
            "path": "/simple/index.md",
            "relative_path": "./index.md",
        }
    ]

    engine = Generator(project, theme)

    generated = engine.persist("/output")

    generated.should.equal([
        "/output/index.html"
    ])

    os.makedirs.assert_called_once_with("/output")


@patch('markment.fs.AssetsCloner')
@patch('markment.fs.shutil')
@patch('markment.fs.os')
@patch('markment.fs.io')
@patch('markment.fs.exists')
@patch('markment.fs.Node')
def test_persist_with_files_to_copy(Node, exists, io, os, shutil, Cloner):
    ("Generator#persist(destination_path)"
     " with files to copy")
    os.sep = '/'
    Node.side_effect = FakeNode

    exists.return_value = True
    theme = Mock()
    theme.index = {'static_path': '/themes/cool'}
    project = Mock()

    project.node = FakeNode("/simple/")

    theme.node = FakeNode("/themes/cool")

    project.generate.return_value = [
        {
            "type": "tree",
            "path": "/simple/",
            "relative_path": "./",
        },
        {
            "type": "blob",
            "html": "<h1>Foobar</h1>",
            "markdown": "# Foobar\n",
            "path": "/simple/index.md",
            "relative_path": "./index.md",
        }
    ]

    engine = Generator(project, theme)
    engine.files_to_copy = [
        "style.css",
        "logo.png",
    ]

    generated = engine.persist("/output")

    generated.should.equal([
        '/output/./index.html',
        '/output/style.css',
        '/output/logo.png',
    ])


@patch('markment.fs.AssetsCloner')
@patch('markment.fs.shutil')
@patch('markment.fs.os')
@patch('markment.fs.io')
@patch('markment.fs.exists')
@patch('markment.fs.Node')
def test_persist_with_files_to_copy_from_theme(
        Node, exists, io, os, shutil, Cloner):
    ("Generator#persist(destination_path)"
     " with files to copy from the theme")
    os.sep = '/'
    Node.side_effect = FakeNode

    exists.return_value = False
    theme = Mock()
    theme.index = {'static_path': '/themes/cool'}
    project = Mock()

    project.node = FakeNode("/simple/")
    project.node.find = Mock(return_value=None)
    theme.node = FakeNode("/themes/cool")

    project.generate.return_value = [
        {
            "type": "tree",
            "path": "/simple/",
            "relative_path": "./",
        },
        {
            "type": "blob",
            "html": "<h1>Foobar</h1>",
            "markdown": "# Foobar\n",
            "path": "/simple/index.md",
            "relative_path": "./index.md",
        }
    ]

    engine = Generator(project, theme)
    engine.files_to_copy = [
        "style.css",
        "logo.png",
    ]

    generated = engine.persist("/output")

    generated.should.equal([
        '/output/./index.html',
        '/output/style.css',
        '/output/logo.png',
    ])


@patch('markment.fs.AssetsCloner')
@patch('markment.fs.shutil')
@patch('markment.fs.os')
@patch('markment.fs.io')
@patch('markment.fs.exists')
@patch('markment.fs.Node')
def test_persist_with_files_to_copy_missing(
        Node, exists, io, os, shutil, Cloner):
    ("Generator#persist(destination_path,gently=False)"
     " with files to copy from the theme")
    os.sep = '/'
    Node.side_effect = FakeNode

    exists.return_value = True
    theme = Mock()
    theme.index = {'static_path': '/themes/cool'}
    project = Mock()

    project.node = FakeNode("/simple/")
    project.node.find = Mock(return_value=None)
    theme.node = FakeNode("/themes/cool")
    theme.node.find = Mock(return_value=None)

    project.generate.return_value = [
        {
            "type": "tree",
            "path": "/simple/",
            "relative_path": "./",
        },
        {
            "type": "blob",
            "html": "<h1>Foobar</h1>",
            "markdown": "# Foobar\n",
            "path": "/simple/index.md",
            "relative_path": "./index.md",
        }
    ]

    engine = Generator(project, theme)
    engine.files_to_copy = [
        "style.css",
        "logo.png",
    ]

    engine.persist.when.called_with("/output").should.throw(
        IOError, "The documentation refers to style.css, logo.png but they doesn't exist anythere")


@patch('markment.fs.AssetsCloner')
@patch('markment.fs.shutil')
@patch('markment.fs.os')
@patch('markment.fs.io')
@patch('markment.fs.exists')
@patch('markment.fs.Node')
def test_persist_with_files_to_copy_missing_gently(
        Node, exists, io, os, shutil, Cloner):
    ("Generator#persist(destination_path, gently=True)"
     " with files to copy from the theme missing")
    os.sep = '/'
    Node.side_effect = FakeNode

    exists.return_value = True
    theme = Mock()
    theme.index = {'static_path': '/themes/cool'}
    project = Mock()

    project.node = FakeNode("/simple/")
    project.node.find = Mock(return_value=None)
    theme.node = FakeNode("/themes/cool")
    theme.node.find = Mock(return_value=None)

    project.generate.return_value = [
        {
            "type": "tree",
            "path": "/simple/",
            "relative_path": "./",
        },
        {
            "type": "blob",
            "html": "<h1>Foobar</h1>",
            "markdown": "# Foobar\n",
            "path": "/simple/index.md",
            "relative_path": "./index.md",
        }
    ]

    engine = Generator(project, theme)
    engine.files_to_copy = [
        "style.css",
        "logo.png",
    ]

    generated = engine.persist("/output", gently=True)
    generated.should.equal(['/output/./index.html'])
