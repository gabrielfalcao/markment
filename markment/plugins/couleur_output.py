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

import sys
from os.path import basename, dirname, relpath
from markment.events import after, before
from markment.version import version
from couleur import Shell


sh = Shell(sys.stdout)
has_persisted_html = False

W = lambda x: relpath(x)


@after.file_indexed
def file_indexed(event, info, pos, total, siblings):
    sh.bold_blue("\rIndexing file ")
    sh.bold_white(str(pos))
    sh.bold_blue(" of ")
    sh.bold_white(str(total))
    if pos == total:
        sh.bold_blue(" done.")
        sh.normal("\n")
    sh.bold_blue("\n", replace=True)


@after.html_persisted
def html_persisted(event, destination_path, bites):
    sh.bold_white('\rCreated ')
    sh.white(W(destination_path))
    sh.bold_white(" . {0}kb ".format(len(bites) / 1000.0))
    sh.white("written\n")


@after.file_copied
def after_copy_file(event, source_path, destiny_path, pos, total):
    sh.bold_green("\rCopying file ")
    sh.bold_white(str(pos))
    sh.bold_green(" of ")
    sh.bold_white(str(total))
    if pos == total:
        sh.bold_green(" done.")
        sh.normal("\n")
    sh.bold_green("\n", replace=True)


@after.missed_file
def missed_file(event, path):
    # sh.bold_red('Missing file {0}\n'.format(path))
    pass


@before.all
def before_all(self, args):
    sh.white("Markment ")
    sh.bold_green(version)
    sh.normal("\n\n")
    sh.yellow("Scanning {0}...\n".format(args.OUTPUT))


@after.all
def after_all(self, generated):
    sh.normal("\nMarkment has generated ")
    sh.bold_green(str(len(generated)))
    sh.bold_white(" new files\n")
