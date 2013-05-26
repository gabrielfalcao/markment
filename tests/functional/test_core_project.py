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
from os.path import relpath, join
from markment.core import Project
from markment.ui import Theme
from .base import CWD_FILE


def test_project_should_find_metadata():
    "core.Project.discover() should find metadata in a .markment.yml file"

    project = Project.discover(join(os.getcwdu(), "spec"))

    project.should.be.a(Project)
    project.should.have.property('name').being.equal('Markment')
    project.should.have.property('version').being.equal('0.2.12')
    project.should.have.property('description').being.equal(
        'A markdown-based automatic documentation generator')


def test_project_should_render_all_markdown_files_with_certain_theme():
    ("core.Project#generate(theme) should return each one "
     "of the markdown files under the given template")

    theme = Theme.load_by_name('touch-of-pink')

    project = Project.discover(join(os.getcwdu(), 'spec'))

    generated = list(sorted(project.generate(theme), key=lambda x: len(x['relative_path'])))

    generated.should_not.be.empty

    readme = generated[0]

    readme.should.be.a(dict)
    readme.should.have.key('markdown')
    readme.should.have.key('indexes')
    readme.should.have.key('documentation')
    readme.should.have.key('html')
    readme.should.have.key('path')
    readme.should.have.key('relative_path')

    len(readme['html']).should.be.above(len(readme['documentation']))
    readme['path'].should.equal(CWD_FILE('spec/API.md'))
    readme['relative_path'].should.equal(relpath(CWD_FILE('API.md')))
