#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <markment - markdown-based documentation generator for python>
# Copyright (C) <2013>  Gabriel Falc達o <gabriel@nacaolivre.org>
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
from markment.events import after
from markment.fs import Node
from lxml import etree


@after.all
def save_sitemap(event, args, project, theme, generated):
    if not args.SITEMAP_PREFIX:
        return

    urlset = etree.Element("urlset")
    destination = Node(args.OUTPUT)

    NAME = 'sitemap.xml'

    for item in filter(lambda x: x.endswith('html'), generated):
        relative = destination.relative(item)
        url = etree.SubElement(urlset, "url")
        loc = etree.SubElement(url, "loc")
        loc.text = "{0}/{1}".format(
            args.SITEMAP_PREFIX.rstrip('/'),
            relative,
        )

    with destination.open(NAME, 'w') as f:
        f.write(etree.tostring(urlset, pretty_print=True).decode('utf-8'))
