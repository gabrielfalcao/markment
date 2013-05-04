# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from os.path import dirname, abspath, join

import markment

LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)
CWD_FILE = lambda *path: join(abspath(os.getcwdu()), *path)
BUILTIN_FILE = lambda *path: join(abspath(dirname(markment.__file__)), *path)
