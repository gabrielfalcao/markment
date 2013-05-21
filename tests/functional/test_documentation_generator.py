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

import os
import shutil

from markment.core import Project
from markment.fs import Generator
from markment.ui import Theme
from lxml import html as lhtml
from sure import scenario
from os.path import relpath
from .base import LOCAL_FILE


def prepare(context):
    context.project_path = LOCAL_FILE('sandbox_simple')
    context.output_path = LOCAL_FILE('output')


def cleanup(context):
    if os.path.exists(context.output_path):
        shutil.rmtree(context.output_path)


fs_test = scenario([prepare], [cleanup])
sort_files = lambda x: (len(relpath(x).split(os.sep)), x)


@fs_test
def test_generate_files(context):
    "Markment should find files and generate them"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.be.a(list)
    map(relpath, generated).should.equal(map(relpath, [
        LOCAL_FILE('output/index.html'),
        LOCAL_FILE('output/assets/style.css'),
        LOCAL_FILE('output/docs/output.html'),
        LOCAL_FILE('output/docs/strings.html'),
        LOCAL_FILE('output/img/logo.png'),
        LOCAL_FILE('output/assets/img/favicon.png'),
        LOCAL_FILE('output/docs/even/deeper/item.html'),
    ]))


@fs_test
def test_index_file(context):
    "The index file should have the assets pointing to the right path"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=lambda x: len(x.split(os.sep)))
    generated.should.have.length_of(7)

    index = generated[0]

    html = open(index).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('link.theme-asset')

    links.should.have.length_of(1)

    style = links[0]

    style.attrib.should.have.key("href").being.equal("./assets/style.css")


@fs_test
def test_index_has_correct_links_for_md_files(context):
    "The index file should have correct html links for markdown files"

    project = Project.discover(context.project_path)
    theme = Theme.load_from_path(LOCAL_FILE('sandbox_simple', 'themes', 'turbo'))
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.have.length_of(5)
    index = generated[0]
    index.should.contain('index')

    html = open(index).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('a')

    links.should.have.length_of(3)

    l1, l2, l3 = links

    l1.attrib.should.have.key('href').being.equal('#python-tutorial')
    l2.attrib.should.have.key('href').being.equal('./docs/output.html')
    l3.attrib.should.have.key('href').being.equal('./docs/strings.html')


@fs_test
def test_index_toc_links_point_to_html_files(context):
    "The index file should have correct html links for markdown files"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.have.length_of(7)

    index = generated[0]
    index.should.contain('index')

    html = open(index).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('a.toc')

    links.should.have.length_of(4)

    l1, l2, l3, l4 = links

    l1.attrib.should.have.key('href').being.equal('./index.html')
    l2.attrib.should.have.key('href').being.to.match('./docs/\w+.html')
    l3.attrib.should.have.key('href').being.to.match('./docs/\w+.html')
    l4.attrib.should.have.key('href').being.equal('./docs/even/deeper/item.html')


@fs_test
def test_index_images_point_to_right_place(context):
    "The index file should have correct html paths to images"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.have.length_of(7)

    index = generated[0]
    index.should.contain('index')

    html = open(index).read()
    dom = lhtml.fromstring(html)

    images = dom.cssselect('img')

    images.should.have.length_of(1)

    img = images[0]

    img.attrib.should.have.key('src').being.equal("./img/logo.png")


@fs_test
def test_second_level_file(context):
    "The second_level file should have the assets pointing to the right path"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.have.length_of(7)

    second_level = generated[2]
    second_level.should.contain('docs/output.html')

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('link.theme-asset')

    links.should.have.length_of(1)

    style = links[0]

    style.attrib.should.have.key("href").being.equal("../assets/style.css")


@fs_test
def test_second_level_has_correct_links_for_md_files(context):
    "The second_level file should have correct html links for markdown files"

    project = Project.discover(context.project_path)
    theme = Theme.load_from_path(LOCAL_FILE('sandbox_simple', 'themes', 'simple-index'))
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.have.length_of(5)

    second_level = generated[1]
    second_level.should.contain('docs/output.html')

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('a.index')

    links.should.have.length_of(4)

    l1, l2, l3, l4 = links

    l1.attrib.should.have.key('href').being.equal('../index.html')
    l2.attrib.should.have.key('href').being.to.match('./\w+.html')
    l3.attrib.should.have.key('href').being.to.match('./\w+.html')
    l4.attrib.should.have.key('href').being.equal('./even/deeper/item.html')


@fs_test
def test_second_level_toc_links_point_to_html_files(context):
    "The second_level file should have correct html links for markdown files"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.have.length_of(7)

    second_level = generated[2]
    second_level.should.contain('docs/output.html')

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('a.toc')

    links.should.have.length_of(4)

    l1, l2, l3, l4 = links

    l1.attrib.should.have.key('href').being.equal('../index.html')
    l2.attrib.should.have.key('href').being.to.match('./\w+.html')
    l3.attrib.should.have.key('href').being.to.match('./\w+.html')
    l4.attrib.should.have.key('href').being.equal('./even/deeper/item.html')


@fs_test
def test_second_level_stylesheets_point_to_right_place(context):
    "The second_level file should have correct html paths to stylesheets"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = sorted(destination.persist(context.output_path), key=sort_files)
    generated.should.have.length_of(7)

    second_level = generated[2]
    second_level.should.contain('docs/output.html')

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    stylesheets = dom.cssselect('link.theme-asset')

    stylesheets.should.have.length_of(1)

    img = stylesheets[0]

    img.attrib.should.have.key('href').being.equal("../assets/style.css")
