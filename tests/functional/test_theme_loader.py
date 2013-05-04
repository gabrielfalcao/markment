# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jinja2 import Template


from markment.ui import Theme, InvalidThemePackage

from .base import LOCAL_FILE, BUILTIN_FILE


def test_theme_from_folder_succeeds():
    ("Markment should provide a way to load templates from a folder")

    theme = Theme.load_from_path(LOCAL_FILE('fixtures', 'themes', 'turbo'))

    theme.should_not.be.none
    theme.should.be.a(Theme)
    theme.path.should.equal(LOCAL_FILE('fixtures', 'themes', 'turbo'))


def test_theme_from_folder_missing_yml_file():
    ("Markment should complain when a folder is not a valid theme")

    destination = LOCAL_FILE('fixtures', 'docs')
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

    theme = Theme.load_from_path(LOCAL_FILE('fixtures', 'themes', 'turbo'))

    theme.should.be.a(Theme)

    index = theme.index

    index.should.be.a(dict)
    index.should.have.key('index_template').being.equal('base.html')
    index.should.have.key('static_path').being.equal(LOCAL_FILE('fixtures', 'themes', 'turbo', 'media'))


def test_theme_get_template_content():
    ("markment.ui.Theme should return the template content")

    theme = Theme.load_from_path(LOCAL_FILE('fixtures', 'themes', 'turbo'))

    theme.should.be.a(Theme)

    content = theme.get_template_content()

    content.should.be.an(unicode)
    content.should.look_like('<test>This works {{ documentation }}</test>')


def test_theme_get_template():
    ("markment.ui.Theme should return the template")

    theme = Theme.load_from_path(LOCAL_FILE('fixtures', 'themes', 'turbo'))

    theme.should.be.a(Theme)

    template = theme.get_template()

    template.should.be.a(Template)
    template.render.should.be.callable


def test_theme_render():
    ("markment.ui.Theme should be able to render the template")

    theme = Theme.load_from_path(LOCAL_FILE('fixtures', 'themes', 'turbo'))

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
