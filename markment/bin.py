#!/usr/bin/env python
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
import yaml
import argparse

from os.path import abspath, join, exists, relpath

from markment.core import Project
from markment.fs import Generator, Node
from markment.ui import Theme, InvalidThemePackage
from markment.server import server
from markment.events import before, after
from markment.version import version

LOGO = """
                      _                         _
 _ __ ___   __ _ _ __| | ___ __ ___   ___ _ __ | |_
| '_ ` _ \ / _` | '__| |/ / '_ ` _ \ / _ \ '_ \| __|
| | | | | | (_| | |  |   <| | | | | |  __/ | | | |_
|_| |_| |_|\__,_|_|  |_|\_\_| |_| |_|\___|_| |_|\__|

version {0}
... Generate beautiful documentation for your project
""".format(version)

local_node = Node(__file__).dir


parser = argparse.ArgumentParser(
    add_help=True,
    formatter_class=argparse.RawTextHelpFormatter,
    description=LOGO,
    epilog='''Markment finds all the markdown files recursively in the given source
directory and generated static html for all of them.

It comes with a few builtin themes so you have absolutely no
more work other than just having your documentation well written.

A builtin HTTP server is also available so you can preview your
documentation before generating it.

Example usage:

  Server:

    markment --serve -t modernist

  Generate static files:

    markment -o ~/Desktop/myproject-docs/ -t modernist

''')

parser.add_argument(
    'SOURCE',
    default=os.getcwdu(), nargs='?',
    help='The source path in which markdown should recursively find documentation.')

parser.add_argument(
    '-t', '--theme', dest='THEME', default='bootstrap-full',
    help='Markment theme name or path')

parser.add_argument(
    '-s', '--server', dest='RUNSERVER', action="store_true",
    default=False,
    help='Enables the builtin HTTP server')

parser.add_argument(
    '--autoindex', dest='AUTOINDEX', action="store_true",
    default=True,
    help='Generates an index.html file if it does not exist in the destination folder.')

parser.add_argument(
    '-o', '--output-path', dest='OUTPUT', default='./_public/',
    help='Where markment should output the new documentation')

parser.add_argument(
    '--themes', dest='JUST_LIST_THEMES', action="store_true", default=False,
    help="Just list the names of the available themes. Skips documentation generation")

parser.add_argument(
    '--sitemap-for', dest='SITEMAP_PREFIX', default="",
    help="Generates a sitemap pointing to the given url prefix.")

parser.add_argument(
    '--porcelain', dest='PORCELAIN', action="store_true", default=False,
    help="Tells markment to use a format that is less visually rich and more machine-friendly")


def get_themes():
    for theme in local_node.cd('themes').grep('markment.yml'):
        yield theme


def list_themes(porcelain=False):
    if not porcelain:
        print "Available themes:"
    for theme in get_themes():
        with open(theme.path) as f:
            raw = f.read()

        meta = yaml.load(raw)
        if 'author' not in meta:
            continue

        if porcelain:
            print theme.dir.basename
        else:
            print "  \033[1;32m", theme.dir.basename, "\033[0mby", meta['author']['name'], ' \033[1;33m({0})\033[0m'.format(
                meta['author']['website']
            )


def main():
    args = parser.parse_args()

    if not args.PORCELAIN:
        from markment.plugins import couleur_output
    else:
        from markment.plugins import porcelain_output
    if args.SITEMAP_PREFIX:
        from markment.plugins import sitemap

    if args.AUTOINDEX:
        from markment.plugins import autoindex

    if args.JUST_LIST_THEMES:
        if not args.PORCELAIN:
            print LOGO
        return list_themes(args.PORCELAIN)

    project_path = abspath(args.SOURCE)
    output_path = abspath(args.OUTPUT)
    before.all.shout(args)
    project = Project.discover(project_path)
    if exists(join(args.THEME, 'markment.yml')):
        theme = Theme.load_from_path(args.THEME)
    elif os.sep not in args.THEME:
        try:
            theme = Theme.load_by_name(args.THEME)
        except InvalidThemePackage:
            print "." * 20
            print "\033[1;32m Invalid theme name\033[0m"
            print "." * 20
            print
            print "\033[1;31mMarkment doesn't have a builtin theme called \033[0m'{0}'".format(args.THEME)
            print
            return list_themes()
    else:
        print "Invalid theme name:", args.THEME
        print
        return list_themes()

    if args.RUNSERVER:
        print "\033[1;32mMarkment is serving the documentation "
        print "under \033[1;31m'./{0}' \033[1;32mdynamically\033[0m".format(
            relpath(project_path))
        print
        print "\033[1;33mNow you can just change whatever files you want"
        print "and refresh your browser\033[0m"
        print
        return server(project_path, theme).run(debug=True, use_reloader=False)

    destination = Generator(project, theme)
    generated = destination.persist(output_path, gently=True)
    after.all.shout(args, project, theme, generated)


if __name__ == '__main__':
    main()
