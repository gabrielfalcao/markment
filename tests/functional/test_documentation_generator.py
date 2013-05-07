# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil

from markment.core import Project
from markment.fs import Generator
from markment.ui import Theme
from lxml import html as lhtml
from sure import scenario

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

    pj = Project.discover(context.project_path)

    destination = Generator(context.output_path)
    theme = Theme.load_by_name('touch-of-pink')

    generated = destination.persist(pj, theme)

    generated.should.be.a(list)
    generated.should.equal([
        LOCAL_FILE('output/index.html'),
        LOCAL_FILE('output/docs/output.html'),
        LOCAL_FILE('output/docs/strings.html'),
        LOCAL_FILE('output/assets/style.css'),
        LOCAL_FILE('output/assets/img/favicon.png'),
    ])


@fs_test
def test_index_file(context):
    "The index file should have the assets pointing to the right path"

    pj = Project.discover(context.project_path)

    destination = Generator(context.output_path)
    theme = Theme.load_by_name('touch-of-pink')

    generated = destination.persist(pj, theme)

    index = generated[0]

    html = open(index).read()
    dom = lhtml.fromstring(html)

    links = dom.cssselect('link[rel="stylesheet"]')

    links.should.have.length_of(2)

    tango, style = links

    style.attrib.should.have.key("href").being.equal("./assets/style.css")
