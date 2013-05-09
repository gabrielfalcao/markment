#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import argparse
from os.path import abspath, join, exists

from markment.core import Project
from markment.fs import Generator
from markment.ui import Theme


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
    '-o', '--output-path', dest='OUTPUT', default='./_public/',
    help='Where markment should output the new documentation')


def main():
    args = parser.parse_args()

    project_path = args.SOURCE
    output_path = args.OUTPUT

    print "Generating documentation from", project_path
    print "  Destination:", output_path

    project = Project.discover(project_path)
    if exists(join(args.THEME, 'markment.yml')):
        theme = Theme.load_from_path(args.SOURCE)
    elif os.sep not in args.THEME:
        theme = Theme.load_by_name(args.THEME)
    else:
        print "Invalid theme name:", args.THEME

    destination = Generator(project, theme)
    generated = destination.persist(output_path, gently=True)

    for f in generated:
        print "\033[1;32mGenerated:\033[0m  ", os.path.relpath(f)


if __name__ == '__main__':
    main()
