#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from markment.core import Project
from markment.fs import Generator
from markment.ui import Theme

project = Project.discover(os.getcwdu())
theme = Theme.load_by_name('touch-of-pink')

destination = Generator(project, theme)

generated = destination.persist(os.path.join(project.path, '_public'), gently=True)

for f in generated:
    print "\033[1;32mGenerated:\033[0m  ", os.path.relpath(f)
