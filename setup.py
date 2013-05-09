# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <markment - markdown-based test runner for python>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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
    "Pygments==1.5",
    "misaka==1.0.2",
    "cssselect==0.8",
    "lxml==3.1.2",
    "PyYAML==3.10",
    "Flask==0.9",
    "Jinja2==2.6",
]

setup(name='markment',
      version='0.1.0',
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
