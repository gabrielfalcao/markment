# -*- coding: utf-8 -*-
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
    context.project_path = LOCAL_FILE('fixtures')
    context.output_path = LOCAL_FILE('output')


def cleanup(context):
    if os.path.exists(context.output_path):
        shutil.rmtree(context.output_path)


fs_test = scenario([prepare], [cleanup])


@fs_test
def test_generate_files(context):
    "Markment should find files and generate them"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = destination.persist(context.output_path)

    generated.should.be.a(list)
    map(relpath, generated).should.equal(map(relpath, [
        LOCAL_FILE('output/index.html'),
        LOCAL_FILE('output/docs/output.html'),
        LOCAL_FILE('output/docs/strings.html'),
        LOCAL_FILE('output/img/logo.png'),
        LOCAL_FILE('output/assets/style.css'),
        LOCAL_FILE('output/assets/img/favicon.png'),
    ]))


@fs_test
def test_index_file(context):
    "The index file should have the assets pointing to the right path"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = destination.persist(context.output_path)

    index = generated[0]

    html = open(index).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('link[rel="stylesheet"]')

    links.should.have.length_of(2)

    tango, style = links

    style.attrib.should.have.key("href").being.equal("./assets/style.css")


@fs_test
def test_index_has_correct_links_for_md_files(context):
    "The index file should have correct html links for markdown files"

    project = Project.discover(context.project_path)
    theme = Theme.load_from_path(LOCAL_FILE('fixtures', 'themes', 'turbo'))
    destination = Generator(project, theme)
    generated = destination.persist(context.output_path)

    index = generated[0]

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
    generated = destination.persist(context.output_path)

    index = generated[0]

    html = open(index).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('a.toc')

    links.should.have.length_of(3)

    l1, l2, l3 = links

    l1.attrib.should.have.key('href').being.equal('./index.html')
    l2.attrib.should.have.key('href').being.equal('./docs/output.html')
    l3.attrib.should.have.key('href').being.equal('./docs/strings.html')


@fs_test
def test_index_images_point_to_right_place(context):
    "The index file should have correct html paths to images"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = destination.persist(context.output_path)

    index = generated[0]

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
    generated = destination.persist(context.output_path)

    second_level = generated[1]

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('link[rel="stylesheet"]')

    links.should.have.length_of(2)

    tango, style = links

    style.attrib.should.have.key("href").being.equal("../assets/style.css")


@fs_test
def test_second_level_has_correct_links_for_md_files(context):
    "The second_level file should have correct html links for markdown files"

    project = Project.discover(context.project_path)
    theme = Theme.load_from_path(LOCAL_FILE('fixtures', 'themes', 'turbo'))
    destination = Generator(project, theme)
    generated = destination.persist(context.output_path)

    second_level = generated[1]

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('a')

    links.should.have.length_of(3)

    l1, l2, l3 = links

    l1.attrib.should.have.key('href').being.equal('#python-tutorial')
    l2.attrib.should.have.key('href').being.equal('../docs/output.html')
    l3.attrib.should.have.key('href').being.equal('../docs/strings.html')


@fs_test
def test_second_level_toc_links_point_to_html_files(context):
    "The second_level file should have correct html links for markdown files"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = destination.persist(context.output_path)

    second_level = generated[1]

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('a.toc')

    links.should.have.length_of(3)

    l1, l2, l3 = links

    l1.attrib.should.have.key('href').being.equal('../second_level.html')
    l2.attrib.should.have.key('href').being.equal('../docs/output.html')
    l3.attrib.should.have.key('href').being.equal('../docs/strings.html')


@fs_test
def test_second_level_images_point_to_right_place(context):
    "The second_level file should have correct html paths to images"

    project = Project.discover(context.project_path)
    theme = Theme.load_by_name('touch-of-pink')
    destination = Generator(project, theme)
    generated = destination.persist(context.output_path)

    second_level = generated[1]

    html = open(second_level).read()
    dom = lhtml.fromstring(html)

    images = dom.cssselect('img')

    images.should.have.length_of(1)

    img = images[0]

    img.attrib.should.have.key('src').being.equal("../img/logo.png")
