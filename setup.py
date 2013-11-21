# #!/usr/bin/env python
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

import os
from setuptools import setup


def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('markment'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages


requirements = [
    "Jinja2==2.6",
    "PyYAML==3.10",
    "Pygments==1.6",
    "lxml==3.1.2",
    "misaka==1.0.2",
    "cssselect==0.8",
    "flask==0.9",
    "speakers==0.0.3",
    "couleur==0.5.0",
]

setup(name='markment',
      version='0.2.16',
      description=(u'Structured documentation generator for markdown'),
      author=u'Gabriel Falcao',
      author_email='gabriel@nacaolivre.org',
      url='http://github.com/gabrielfalcao/markment',
      packages=get_packages(),
      install_requires=requirements,
      entry_points={
          'console_scripts': ['markment = markment.bin:main'],
      },
      package_data={
          'markment': [
              'themes/*/*/*/*/*/*/*.*',
              'themes/*/*/*/*/*/*.*',
              'themes/*/*/*/*/*.*',
              'themes/*/*/*/*.*',
              'themes/*/*/*.*',
              'themes/*/*.*',
              'themes/*.*',
          ],
      })
