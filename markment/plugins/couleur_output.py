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
from datetime import datetime
from os.path import relpath
from markment.events import after, before
from markment.version import version
from couleur import Shell


sh = Shell(sys.stdout)

W = lambda x: relpath(x)


@before.exception_handler
@after.exception_handler
def print_out(event, exception, args, kw):
    sh.bold_red("\n#ERROR ({0})#\n".format(exception))


@after.file_indexed
def file_indexed(event, info, pos, total, siblings):
    sh.blue("\rIndexing file ")
    sh.bold_white(str(pos))
    sh.blue(" of ")
    sh.bold_white(str(total))
    if pos == total:
        sh.bold_white(" done.")
        sh.normal("\n")
    sh.normal("\n", replace=True)


@after.partially_rendering_markdown
def partialy_render_md(event, info, theme, kw, pos, total, siblings):
    sh.blue("\rPre-rendering markdown ")
    sh.bold_white(str(pos))
    sh.white(" of ")
    sh.bold_white(str(total))
    if pos == total:
        sh.normal(" done.")
        sh.normal("\n")
    sh.normal("\n", replace=True)


@after.rendering_markdown
def render_md(event, info, theme, kw, pos, total, siblings):
    sh.blue("\rPost-processing markdown ")
    sh.bold_white(str(pos))
    sh.white(" of ")
    sh.bold_white(str(total))
    if pos == total:
        sh.normal(" done.")
        sh.normal("\n")
    sh.normal("\n", replace=True)

total_bytes = 0


@after.html_persisted
def html_persisted(event, destination_path, raw_bytes, position, total):
    global total_bytes
    if total_bytes is 0:
        sh.normal("\n")

    total_bytes += len(raw_bytes)
    if position < total:
        sh.red('\rWriting ')
        sh.bold_white("{0}kb".format(total_bytes / 1000.0))
    else:
        sh.blue('\rWrote ')
        sh.bold_yellow("{0}kb".format(total_bytes / 1000.0))

    if position == total:
        sh.blue(' of html')
        sh.bold_red(b' \xe2\x9d\xa4')
        sh.normal("\n")

    sh.normal("\n", replace=True)


@after.file_copied
def after_copy_file(event, source_path, destiny_path, pos, total):
    sh.blue("\rCopying file ")
    sh.bold_white(str(pos))
    sh.blue(" of ")
    sh.bold_white(str(total))
    if pos == total:
        sh.blue(" done.")
        sh.normal("\n")
    sh.blue("\n", replace=True)


@after.missed_file
def missed_file(event, path):
    # sh.bold_red('Missing file {0}\n'.format(path))
    pass


@before.all
def before_all(self, args):
    sh.white("Markment ")
    sh.green(version)
    sh.normal("\n\n")
    sh.bold_white("The documentation will be built with the theme ")
    sh.green(args.THEME)
    sh.bold_white("...\n")
    sh.bold_white("Scanning ")
    sh.yellow(args.SOURCE)
    sh.bold_white("...\n")
    before.started = datetime.now()


@after.all
def after_all(event, args, project, theme, generated):
    sh.white("\nMarkment took ")
    now = datetime.now()
    took = (now - before.started)
    seconds = took.seconds
    if not seconds:
        seconds = took.microseconds / 1000.0 / 1000.0

    sh.green("{0:.2f}".format(seconds))
    sh.white(" seconds to run\n")
