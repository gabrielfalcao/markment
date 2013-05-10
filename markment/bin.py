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
import argparse
from os.path import abspath, join, exists, relpath

from markment.core import Project
from markment.fs import Generator
from markment.ui import Theme
from markment.server import server


LOGO = """
                      _                         _
 _ __ ___   __ _ _ __| | ___ __ ___   ___ _ __ | |_
| '_ ` _ \ / _` | '__| |/ / '_ ` _ \ / _ \ '_ \| __|
| | | | | | (_| | |  |   <| | | | | |  __/ | | | |_
|_| |_| |_|\__,_|_|  |_|\_\_| |_| |_|\___|_| |_|\__|

... Generate beautiful documentation for your project
"""

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

    markment --serve -t slate

  Generate static files:

    markment -o ~/Desktop/myproject-docs/ -t slate

''')

parser.add_argument(
    'SOURCE',
    default=os.getcwdu(), nargs='?',
    help='The source path in which markdown should recursively find documentation.')

parser.add_argument(
    '-t', '--theme', dest='THEME', default='slate',
    help='Markment theme name or path')

parser.add_argument(
    '-s', '--server', dest='RUNSERVER', action="store_true",
    default=False,
    help='Enables the builtin HTTP server')

parser.add_argument(
    '-o', '--output-path', dest='OUTPUT', default='./_public/',
    help='Where markment should output the new documentation')


def main():
    args = parser.parse_args()

    project_path = abspath(args.SOURCE)
    output_path = abspath(args.OUTPUT)

    project = Project.discover(project_path)
    if exists(join(args.THEME, 'markment.yml')):
        theme = Theme.load_from_path(args.THEME)
    elif os.sep not in args.THEME:
        theme = Theme.load_by_name(args.THEME)
    else:
        print "Invalid theme name:", args.THEME

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
    print "Generating documentation from", project_path
    print "  Destination:", output_path

    generated = destination.persist(output_path, gently=True)

    for f in generated:
        print "\033[1;32mGenerated:\033[0m  ", os.path.relpath(f)


if __name__ == '__main__':
    main()
