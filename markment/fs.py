# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import shutil

from fnmatch import fnmatch
from functools import partial
from os.path import abspath, join, dirname, exists, split, basename

LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)


class Node(object):
    def __init__(self, base_path):
        self.base_path = abspath(base_path)
        self.base_path_regex = '^{0}'.format(re.escape(self.base_path))

    def relative(self, path):
        return re.sub(self.base_path_regex, '', path).lstrip(os.sep)

    def walk(self, path=None):
        for root, folders, filenames in os.walk(path or self.base_path):
            for filename in filenames:
                yield join(root, filename)

    def contains(self, path):
        return exists(self.join(path))

    def join(self, path):
        return join(self.base_path, path)

    def open(self, path, *args, **kw):
        return open(self.join(path), *args, **kw)


class TreeMaker(object):
    def __init__(self, base_path):
        self.base_path = abspath(base_path)
        self.base_path_regex = '^{0}'.format(re.escape(self.base_path))
        self.node = Node(base_path)

    def relative(self, path):
        return re.sub(self.base_path_regex, '', path).lstrip(os.sep)

    def find_all_markdown_files(self):
        dirs = []
        for fullpath in self.node.walk(self.base_path):
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


class Generator(object):
    regex = re.compile(r'[.](md|markdown)$', re.I)

    def __init__(self, destination_path):
        self.destination_path = destination_path
        self.files_to_copy = []
        self.destination = Node(destination_path)

    def rename_markdown_filename(self, path):
        return self.regex.sub('.html', path)

    def calculate_prefix(self, link, assets_folder):
        is_markdown = self.regex.search(link)

        if is_markdown:
            path = './{0}'.format(self.rename_markdown_filename(link.lstrip('/')))
        else:
            path = './{0}/{1}'.format(assets_folder, link.lstrip('/'))
            self.files_to_copy.append(path)

        return path

    def persist(self, project, theme):
        assets_folder = theme.index['static_path']
        assets_folder_root = dirname(assets_folder)
        assets_folder_name = Node(assets_folder_root).relative(assets_folder)

        master_index = project.generate(theme,
                                        static_prefix=assets_folder_name,
                                        url_prefix=partial(self.calculate_prefix,
                                                           assets_folder=assets_folder_name))

        os.makedirs(self.destination_path)

        ret = []

        for item in master_index:
            if item['type'] != 'blob':
                continue

            dest_filename = self.rename_markdown_filename(item['relative_path'])
            destiny = self.destination.join(dest_filename)
            relative_destiny = split(destiny)[0]

            if relative_destiny and not exists(relative_destiny):
                os.makedirs(relative_destiny)

            with self.destination.open(destiny, 'w') as f:
                f.write(item['html'])

            ret.append(destiny)

        for dest in self.files_to_copy:
            destiny = self.destination.join(dest)
            ret.append(destiny)
            shutil.copy2(dest, destiny)

        cloner = AssetsCloner(assets_folder)
        ret.extend(cloner.clone_to(self.destination_path))

        return ret


class AssetsCloner(object):
    def __init__(self, path):
        self.assets_path = path
        self.root = dirname(path)
        self.node = Node(self.root)
        self.basename = split(path)[-1]

    def clone_to(self, root):
        ret = []

        dest_node = Node(root)

        for source_path in self.node.walk(self.assets_path):
            relative_path = self.node.relative(source_path)
            destination_path = dest_node.join(relative_path)
            destination_dir = dirname(destination_path)

            if not dest_node.contains(destination_dir):
                os.makedirs(destination_dir)

            shutil.copy2(source_path, destination_path)
            ret.append(destination_path)

        return ret
