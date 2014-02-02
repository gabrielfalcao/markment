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
    context.project_path = LOCAL_FILE('sandbox_mixed')
    context.theme_path = LOCAL_FILE('sandbox_mixed/simpletheme')
    context.output_path = LOCAL_FILE('sandbox_mixed/output')


def cleanup(context):
    if os.path.exists(context.output_path):
        shutil.rmtree(context.output_path)


fs_test = scenario([prepare], [cleanup])
sort_files = lambda x: "{0}{1}".format(len(relpath(x).split(os.sep)), x)
filter_html = lambda files: [i for i in files if i.endswith('.html')]


@fs_test
def test_first_level_file(context):
    "The first level file should have the assets pointing to the right path"

    project = Project.discover(context.project_path)
    theme = Theme.load_from_path(context.theme_path)
    destination = Generator(project, theme)
    generated = sorted(filter_html(destination.persist(context.output_path)), key=lambda x: len(x.split(os.sep)))
    generated.should.have.length_of(2)

    first_level = generated[0]
    first_level.should.contain('index.html')

    html = open(first_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('link.theme-asset')

    links.should.have.length_of(1)

    style = links[0]

    style.attrib.should.have.key("href").being.equal("./assets/stylesheets/stylesheet.css")


@fs_test
def test_second_level_file(context):
    "The second_level file should have the assets pointing to the right path"

    project = Project.discover(context.project_path)
    theme = Theme.load_from_path(context.theme_path)
    destination = Generator(project, theme)
    generated = sorted(filter_html(destination.persist(context.output_path)), key=sort_files)
    generated.should.have.length_of(2)

    second_level = generated[1]
    second_level.should.contain('docs/index.html')

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('link.theme-asset')

    links.should.have.length_of(1)

    style = links[0]

    style.attrib.should.have.key("href").being.equal("../assets/stylesheets/stylesheet.css")
