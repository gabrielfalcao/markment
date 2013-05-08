# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
import re
import time
import shutil

from fnmatch import fnmatch
from functools import partial
from os.path import (
    abspath,
    join,
    dirname,
    exists,
    split,
    relpath,
    expanduser,
    isfile,
    isdir
)

LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)


class DotDict(dict):
    def __getattr__(self, attr):
        try:
            return super(DotDict, self).__getattribute(attr)
        except AttributeError:
            return self[attr]

STAT_LABELS = ["mode", "ino", "dev", "nlink", "uid", "gid", "size", "atime", "mtime", "ctime"]


class Node(object):
    def __init__(self, path):
        self.path = abspath(expanduser(path))
        {
        # TODO : rename all path to path
        }
        self.path_regex = '^{0}'.format(re.escape(self.path))
        self.exists = exists(self.path)
        try:
            stats = os.stat(self.path)
        except OSError:
            stats = [0] * len(STAT_LABELS)

        self.metadata = DotDict(zip(STAT_LABELS, stats))
        self.is_file = isfile(self.path)
        self.is_dir = isdir(self.path)

    @property
    def dir(self):
        if not self.is_dir:
            return self.parent
        else:
            return self

    @property
    def parent(self):
        return self.__class__(dirname(self.path))

    def could_be_updated_by(self, other):
        return self.metadata.mtime < other.metadata.mtime

    def relative(self, path):
        """##### `Node#relative(path)`

        returns a given path subtracted by the node.path [python`unicode`]

        ```python
        rel = Node('/Users/gabrielfalcao/').relative('/Users/gabrielfalcao/profile-picture.png')
        assert rel == 'profile-picture.png'
        ```
        """
        return re.sub(self.path_regex, '', path).lstrip(os.sep)

    def trip_at(self, path):
        """ ##### `Node#trip_at(path)`

        does a os.walk at the given path and yields the absolute path
        to each file

        ```python
        for filename in node.trip_at('/etc/smb'):
            print filename
        ```
        """
        for root, folders, filenames in os.walk(path):
            for filename in filenames:
                yield join(root, filename)

    def walk(self):
        return self.trip_at(self.path)

    def glob(self, pattern):
        """ ##### `Node#glob(pattern)`

        searches for globs recursively in all the children node of the
        current node returning a respective [python`Node`] instance
        for that given.

        ```python
        for node in Node('/Users/gabrifalcao').glob('*.png'):
            print node.path  # will print the absolute
                             # path of the found file
        ```
        """
        for filename in self.walk():
            if fnmatch(filename, pattern):
                yield self.__class__(filename)

    def grep(self, pattern, flags=0):
        """ ##### `Node#grep(pattern)`

        searches recursively for children that match the given regex
        returning a respective [python`Node`] instance for that given.

        ```python
        for node in Node('/Users/gabrifalcao').glob('*.png'):
            print node.path  # will print the absolute
                             # path of the found file
        ```
        """
        for filename in self.walk():
            if re.search(pattern, filename, flags):
                yield self.__class__(filename)

    def find(self, relative_path):
        """ ##### `Node#find(relative_path)`

        finds a file given the relative_path, it glob and grep using
        the given relative_path to match as a glob and then tries
        to return the first found node.

        If nothing is found, returns None

        ```python

        logo = Node('~/projects/personal/markment').find('logo.png')
        assert logo.path == os.path.expanduser('~/projects/personal/markment')
        ```
        """
        found = list(self.glob(relative_path)) + list(self.grep(relative_path))
        if found:
            return found[0]

        return None

    def contains(self, path):
        return exists(self.join(path))

    def join(self, path):
        return abspath(join(self.path, path))

    def open(self, path, *args, **kw):
        return open(self.join(path), *args, **kw)

    def __repr__(self):
        return '<markment.fs.Node (path={0})>'.format(self.path)


class TreeMaker(object):
    def __init__(self, path):
        self.path = abspath(path)
        self.path_regex = '^{0}'.format(re.escape(self.path))
        self.node = Node(path)

    def __repr__(self):
        return '<markment.fs.TreeMaker(path={0})>'.format(self.path)

    def relative(self, path):
        return re.sub(self.path_regex, '', path).lstrip(os.sep)

    def find_all_markdown_files(self):
        dirs = []
        for fullpath in self.node.walk():
            folder = dirname(fullpath)
            if fnmatch(fullpath, '*.md'):
                if folder != self.path and folder not in dirs:
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

    def __init__(self, project, theme):
        self.files_to_copy = []
        self.project = project
        self.theme = theme

    def rename_markdown_filename(self, path):
        return self.regex.sub('.html', path)

    def calculate_prefix(self, link, info, assets_folder, project, theme):
        is_markdown = self.regex.search(link)

        in_theme = theme.node.find(link)
        in_local = project.node.find(link)
        found = in_local or in_theme

        if is_markdown:
            prefix = './{0}'.format(self.rename_markdown_filename(link.lstrip('/')))
        else:
            level = 1
            current_document = Node(info['relative_path'])

            print "*" * 10, info['relative_path'], "*" * 10

            while current_document.parent and not current_document.dir.find(link):
                level += 1
                current_document = current_document.parent

            relative = current_document.relative(link)

            prefix = '{0}/{1}'.format('.' * level, link.lstrip('/'))
            if found:
                self.files_to_copy.append(relative)

        return prefix

    def persist(self, destination_path, gently=False):
        destination = Node(destination_path)

        assets_folder = self.theme.index['static_path']
        assets_folder_root = dirname(assets_folder)
        assets_folder_name = Node(assets_folder_root).relative(assets_folder)

        url_prefix_callback = partial(
            self.calculate_prefix,
            assets_folder=assets_folder_name,
            project=self.project,
            theme=self.theme,
        )
        master_index = self.project.generate(self.theme,
                                             static_prefix=assets_folder_name,
                                             url_prefix=url_prefix_callback)

        if not exists(destination_path):
            os.makedirs(destination_path)

        ret = []

        for item in master_index:
            if item['type'] != 'blob':
                continue

            dest_filename = self.rename_markdown_filename(item['relative_path'])
            destiny = destination.join(dest_filename)
            relative_destiny = split(destiny)[0]

            if relative_destiny and not exists(relative_destiny):
                os.makedirs(relative_destiny)

            with destination.open(destiny, 'w') as f:
                f.write(item['html'])

            ret.append(destiny)

            references = item.get('url_references', [])

            self.files_to_copy.extend(references)
            ret.extend(references)

        missed_files = []
        for src in self.files_to_copy:

            src = relpath(src)
            in_theme = self.theme.node.find(src)
            in_local = self.project.node.find(src)

            if in_theme:
                source = in_theme.path
            elif in_local:
                source = in_local.path
            else:  # not really there
                missed_files.append(src)
                continue

            destiny = destination.join(src)
            ret.append(destiny)
            destiny_folder = dirname(destiny)
            if not exists(destiny_folder):
                os.makedirs(destiny_folder)

            already_exists = exists(destiny)
            should_update = already_exists and Node(destiny).could_be_updated_by(Node(source))

            if not already_exists or should_update:
                shutil.copy2(source, destiny)

        cloner = AssetsCloner(assets_folder)

        ret.extend(cloner.clone_to(destination_path))

        if missed_files and not gently:
            raise IOError("The documentation refers to {0} "
                          "but they doesn't exist anythere".format(
                              ", ".join(missed_files)))

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

        for source_path in self.node.trip_at(self.assets_path):
            relative_path = self.node.relative(source_path)
            destination_path = dest_node.join(relative_path)
            destination_dir = dirname(destination_path)

            if not dest_node.contains(destination_dir):
                os.makedirs(destination_dir)

            shutil.copy2(source_path, destination_path)
            ret.append(destination_path)

        return ret
