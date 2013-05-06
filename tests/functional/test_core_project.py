# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from os.path import relpath
from markment.core import Project
from markment.ui import Theme
from .base import LOCAL_FILE, CWD_FILE


def test_project_should_find_metadata():
    "core.Project.discover() should find metadata in a .markment.yml file"

    project = Project.discover(os.getcwdu())

    project.should.be.a(Project)
    project.should.have.property('name').being.equal('Markment')
    project.should.have.property('version').being.equal('0.0.2')
    project.should.have.property('description').being.equal(
        'A markdown-based automatic documentation generator')


def test_project_should_render_all_markdown_files_with_certain_theme():
    ("core.Project#generate(theme) should return each one "
     "of the markdown files under the given template")

    theme = Theme.load_by_name('touch-of-pink')

    project = Project.discover(os.getcwdu())

    generated = list(project.generate(theme))

    generated.should_not.be.empty

    readme = generated[0]

    readme.should.be.a(dict)
    readme.should.have.key('markdown')
    readme.should.have.key('indexes')
    readme.should.have.key('documentation')
    readme.should.have.key('html')
    readme.should.have.key('path')
    readme.should.have.key('relative_path')

    readme['html'].should.contain(readme['documentation'])
    readme['path'].should.equal(CWD_FILE('index.md'))
    readme['relative_path'].should.equal(relpath(CWD_FILE('index.md')))
