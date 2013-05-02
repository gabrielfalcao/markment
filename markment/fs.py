# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
from fnmatch import fnmatch
from os.path import abspath, join, dirname


class TreeMaker(object):
    def __init__(self, base_path):
        self.base_path = abspath(base_path)
        self.base_path_regex = '^{0}'.format(re.escape(self.base_path))

    def relative(self, path):
        return re.sub(self.base_path_regex, '', path).lstrip(os.sep)

    def walk(self, path):
        for root, folders, filenames in os.walk(self.base_path):
            for filename in filenames:
                yield join(root, filename)

    def find_all_markdown_files(self):
        dirs = []
        for fullpath in self.walk(self.base_path):
            folder = dirname(fullpath)
            if fnmatch(fullpath, '*.md'):
                if folder != self.base_path and folder not in dirs:
                    dirs.append(folder)
                    yield {
                        'path': folder,
                        'relative_path': self.relative(folder),
                        'type': 'tree',
                    }

                yield {
                    'path': fullpath,
                    'relative_path': self.relative(fullpath),
                    'type': 'blob',
                }
