# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
from fnmatch import fnmatch
from os.path import abspath, join, dirname, exists

LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)


class PathWalker(object):
    def __init__(self, base_path):
        self.base_path = abspath(base_path)
        self.base_path_regex = '^{0}'.format(re.escape(self.base_path))

    def relative(self, path):
        return re.sub(self.base_path_regex, '', path).lstrip(os.sep)

    def walk(self, path):
        for root, folders, filenames in os.walk(self.base_path):
            for filename in filenames:
                yield join(root, filename)

    def contains(self, path):
        return exists(self.join(path))

    def join(self, path):
        return join(self.base_path, path)

    def open(self, path):
        return open(self.join(path))

    def __iter__(self):
        return self

    def next(self):
        for path in self.walk(self.base_path):
            yield path


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
