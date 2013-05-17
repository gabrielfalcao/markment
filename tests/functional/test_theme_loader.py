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

from jinja2 import Template


from markment.ui import Theme, InvalidThemePackage

from .base import LOCAL_FILE, BUILTIN_FILE


def test_theme_from_folder_succeeds():
    ("Markment should provide a way to load templates from a folder")

    theme = Theme.load_from_path(LOCAL_FILE('sandbox_simple', 'themes', 'turbo'))

    theme.should_not.be.none
    theme.should.be.a(Theme)
    theme.path.should.equal(LOCAL_FILE('sandbox_simple', 'themes', 'turbo'))


def test_theme_from_folder_missing_yml_file():
    ("Markment should complain when a folder is not a valid theme")

    destination = LOCAL_FILE('sandbox_simple', 'docs')
    message = ('The folder "{0}" should contain a markment.yml '
               'file but doesn\'t'.format(destination))

    (Theme.load_from_path
     .when
     .called_with(destination)
     .should.throw(
         InvalidThemePackage,
         message))


def test_theme_get_index():
    ("markment.ui.Theme should return the template content")

    theme = Theme.load_from_path(LOCAL_FILE('sandbox_simple', 'themes', 'turbo'))

    theme.should.be.a(Theme)

    index = theme.index

    index.should.be.a(dict)
    index.should.have.key('index_template').being.equal('base.html')
    index.should.have.key('static_path').being.equal(LOCAL_FILE('sandbox_simple', 'themes', 'turbo', 'media'))


def test_theme_get_template():
    ("markment.ui.Theme should return the template")

    theme = Theme.load_from_path(LOCAL_FILE('sandbox_simple', 'themes', 'turbo'))

    theme.should.be.a(Theme)

    template = theme.get_template()

    template.should.be.a(Template)
    template.render.should.be.callable


def test_theme_render():
    ("markment.ui.Theme should be able to render the template")

    theme = Theme.load_from_path(LOCAL_FILE('sandbox_simple', 'themes', 'turbo'))

    theme.should.be.a(Theme)

    rendered = theme.render(documentation='VERY WELL')
    rendered.should.be.an(unicode)
    rendered.should.look_like('<test>This works VERY WELL</test>')


def test_theme_load_by_name():
    ("markment.ui.Theme should be able to load builtin themes")

    theme = Theme.load_by_name('touch-of-pink')
    theme.should.be.a(Theme)
    theme.path.should.equal(BUILTIN_FILE('themes', 'touch-of-pink'))


def test_theme_load_by_name_when_doesnt_exist():
    ("markment.ui.Theme should be able to load builtin themes")
    message = ('Markment does not have a builtin theme called "blablablabla"')

    (Theme.load_by_name
     .when
     .called_with('blablablabla')
     .should.throw(
         InvalidThemePackage,
         message))
