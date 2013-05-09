#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
from os.path import abspath, join

from markment.core import Project
from markment.fs import Generator
from markment.ui import Theme


CWD_FILE = lambda *path: join(abspath(os.getcwdu()), *path)

project_path = CWD_FILE('example')
output_path = CWD_FILE('_public')

print "Generating documentation from", project_path
print "  Destination:", output_path

project = Project.discover(project_path)
theme = Theme.load_by_name('touch-of-pink')
destination = Generator(project, theme)
generated = destination.persist(output_path, gently=True)

for f in generated:
    print "\033[1;32mGenerated:\033[0m  ", os.path.relpath(f)
