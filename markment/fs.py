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

import io
import os
import re
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
    basename,
)
from os.path import isfile as isfile_base
from os.path import isdir as isdir_base

from .events import before, after

LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)


def isfile(path, exists):
    if exists:
        return isfile_base(path)

    return '.' in split(path)[-1]


def isdir(path, exists):
    if exists:
        return isdir_base(path)

    return '.' not in split(path)[-1]


class DotDict(dict):
    def __getattr__(self, attr):
        try:
            return super(DotDict, self).__getattribute(attr)
        except AttributeError:
            return self[attr]

STAT_LABELS = ["mode", "ino", "dev", "nlink", "uid", "gid", "size", "atime", "mtime", "ctime"]


DOTDOTSLASH = '..{0}'.format(os.sep)


class Node(object):
    """Node is a file abstraction.

    The constructor takes a path as a parameter and grabs filesystem
    information about it.

    Its attributes `is_file` and `isdir` are booleans and are useful
    for quickly identifying its 'type', which among Markment's engine
    codebase is either 'blob', for a file and 'dir' for a directory.

    It also has `self.metadata`, which is just a handy `DotDict`
    containing the results of calling `os.stat` (mode, ino, dev,
    nlink, uid, giu, size, atime, mtime, ctime)
    """
    def __init__(self, path):
        self.path = abspath(expanduser(path)).rstrip('/')
        self.path_regex = '^{0}'.format(re.escape(self.path))
        try:
            stats = os.stat(self.path)
            self.exists = True
        except OSError:
            stats = [0] * len(STAT_LABELS)
            self.exists = False

        self.metadata = DotDict(zip(STAT_LABELS, stats))
        self.is_file = isfile(self.path, exists=self.exists)
        self.is_dir = isdir(self.path, exists=self.exists)

    @property
    def basename(self):
        return basename(self.path)

    def list(self):
        return map(self.__class__, os.listdir(self.dir.path))

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

    def trip_at(self, path, lazy=False):
        """ ##### `Node#trip_at(path)`

        does a os.walk at the given path and yields the absolute path
        to each file

        ```python
        for filename in node.trip_at('/etc/smb'):
            print filename
        ```
        """
        def iterator():
            for root, folders, filenames in os.walk(self.join(path)):
                for filename in filenames:
                    yield join(root, filename)

        return lazy and iterator() or list(iterator())

    def walk(self, lazy=False):
        return self.trip_at(self.path, lazy=lazy)

    def glob(self, pattern, lazy=False):
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
        def iterator():
            for filename in self.walk(lazy=lazy):
                if fnmatch(filename, pattern):
                    yield self.__class__(filename)

        return lazy and iterator() or list(iterator())

    def grep(self, pattern, flags=0, lazy=False):
        """ ##### `Node#grep(pattern)`

        searches recursively for children that match the given regex
        returning a respective [python`Node`] instance for that given.

        ```python
        for node in Node('/Users/gabrifalcao').glob('*.png'):
            print node.path  # will print the absolute
                             # path of the found file
        ```
        """

        def iterator():
            for filename in self.walk(lazy=lazy):
                if re.search(pattern, filename, flags):
                    yield self.__class__(filename)

        return lazy and iterator() or list(iterator())

    def __eq__(self, other):
        return self.path == other.path and self.metadata == other.metadata

    def find(self, relative_path):
        """ ##### `Node#find(relative_path)`

        Returns the first file that matches the given relative path.
        Returns None if nothing is returned.

        If nothing is found, returns None
        ```python

        logo = Node('~/projects/personal/markment').find('logo.png')
        assert logo.path == os.path.expanduser('~/projects/personal/markment/logo.png')
        ```
        """
        found = list(self.grep(relative_path, lazy=True))
        if found:
            return found[0]

        return None

    def depth_of(self, path):
        """Returns the level of depth of the given path inside of the
        instance's path.

        Only really works with paths that are relative to the class.

        ```python
        level = Node('/foo/bar').depth_of('/foo/bar/another/dir/file.py')
        assert level == 2
        ```
        """
        new_path = self.relative(path)
        final_path = self.join(new_path)
        if isfile(final_path, exists(final_path)):
            new_path = dirname(new_path)

        new_path = new_path.rstrip('/')
        new_path = "{0}/".format(new_path)
        return new_path.count(os.sep)

    def path_to_related(self, path):
        """Returns the path to a related file. (is under a subtree the
        same tree as the node).

        It's useful to know how to go back to the root of this node
        instance.

        ```python
        way_back = Node('/foo/bar').path_to_related('/foo/bar/another/dir/file.py')
        assert way_back == '../../'

        way_back = Node('/foo/bar/docs/static/file.css').path_to_related('/foo/bar/docs/intro/index.md')
        assert way_back == '../static/file.css'
        ```
        """
        # self.path = "...functional/fixtures/img/logo.png"
        # path = "...functional/fixtures/docs/index.md"
        current = self.dir

        while not path.startswith(current.dir.path):
            current = current.dir.parent.dir

        remaining = current.relative(self.path)

        level = current.relative(path).count(os.sep)

        way_back = os.sep.join(['..'] * level) or '.'
        result = "{0}/{1}".format(way_back, remaining)

        return result

    def cd(self, path):
        return self.__class__(self.join(path))

    def contains(self, path):
        return exists(self.join(path))

    def join(self, path):
        return abspath(join(self.path, path))

    def open(self, path, *args, **kw):
        return io.open(self.join(path), *args, **kw)

    def __repr__(self):
        return '<markment.fs.Node (path={0})>'.format(self.path)


class DocumentIndexer(object):
    def __init__(self, path):
        self.node = Node(path)

    def __repr__(self):
        return '<markment.fs.DocumentIndexer(path={0})>'.format(self.node.path)

    def find_all_markdown_files(self):
        dirs = []

        grep_result = self.node.grep(r'[.](md|markdown)$', re.I)
        total_results = len(grep_result)
        for position, md_node in enumerate(grep_result, start=1):
            folder = md_node.dir.path
            if md_node.dir != self.node.dir and folder not in dirs:
                dirs.append(folder)
                folder_info = {
                    'path': folder,
                    'relative_path': self.node.relative(folder) or './',
                    'type': 'tree',
                }
                after.folder_indexed.shout(
                    folder_info, position, total_results, grep_result)
                yield folder_info

            file_info = {
                'path': md_node.path,
                'relative_path': self.node.relative(md_node.path),
                'type': 'blob',
            }
            after.file_indexed.shout(
                file_info, position, total_results, grep_result)

            yield file_info


class Generator(object):
    regex = re.compile(r'[.](md|markdown)$', re.I)

    def __init__(self, project, theme):
        self.files_to_copy = []
        self.project = project
        self.theme = theme

    def rename_markdown_filename(self, path):
        return self.regex.sub('.html', path)

    def relative_link_callback(self, original_link, current_document_info, destination_root):

        fixed_link, levels = self.get_levels(original_link)

        is_markdown = self.regex.search(original_link)

        found = self.project.node.find(fixed_link)
        if not found:
            return original_link

        found_base = self.project.node.dir

        relative_path = found_base.relative(found.path)

        current_document_path = self.rename_markdown_filename(current_document_info['relative_path'])

        if is_markdown:
            relative_path = self.rename_markdown_filename(relative_path)

        item_destination = destination_root.cd(relative_path)
        destination_document = destination_root.cd(current_document_path)

        prefix = item_destination.path_to_related(destination_document.path)

        if found.path not in self.files_to_copy and not is_markdown:
            self.files_to_copy.append(found.path)

        return prefix

    def get_levels(self, link):
        levels = []
        while link.startswith(DOTDOTSLASH):
            levels.append('..')
            link = link.replace(DOTDOTSLASH, '', 1)

        return link, levels

    def static_url_callback(self, link, current_document_info, destination_root):
        is_markdown = self.regex.search(link)
        prefix = link

        link, levels = self.get_levels(link)
        in_theme = self.theme.node.find(link)

        if in_theme:
            found = in_theme
            found_base = self.theme.node.dir
            found_relative = found_base.relative(found.path)
            asset_destination = destination_root.cd(found_relative)
            current_document_destination = destination_root.cd(current_document_info['relative_path'])
            if not levels:
                prefix = asset_destination.path_to_related(current_document_destination.path)

        else:
            raise IOError("BOOM, could not find {0} anywhere".format(link))

        if is_markdown:
            prefix = self.rename_markdown_filename(prefix)

        elif found and found.path not in self.files_to_copy:
            self.files_to_copy.append(found.path)

        return prefix

    def persist(self, destination_path, gently=False):
        destination = Node(destination_path)

        master_index = self.project.generate(
            self.theme,
            static_url_cb=partial(self.static_url_callback, destination_root=destination),
            link_cb=partial(self.relative_link_callback, destination_root=destination),
        )

        ret = []

        total_indexes = len(master_index)
        for position, item in enumerate(master_index, start=1):
            if item['type'] != 'blob':
                continue

            dest_filename = self.rename_markdown_filename(item['relative_path'])
            destiny = destination.join(dest_filename)
            relative_destiny = split(destiny)[0]

            if relative_destiny and not exists(relative_destiny):
                before.folder_created.shout(relative_destiny)
                os.makedirs(relative_destiny)
                after.folder_created.shout(relative_destiny)

            with destination.open(destiny, 'w') as f:
                value = item['html'].decode('utf-8')
                value = before.html_persisted.shout(destiny, value) or value
                f.write(value)
                after.html_persisted.shout(destiny, value, position, total_indexes)

            ret.append(destiny)

        missed_files = []
        total_files_to_copy = len(self.files_to_copy)
        for position, src in enumerate(self.files_to_copy, start=1):
            in_theme = self.theme.node.find(src)
            in_local = self.project.node.find(src)

            if in_local:
                found = in_local
                found_base = self.project.node.dir
                after.project_file_found.shout(found, found_base)

            elif in_theme:
                found = in_theme
                found_base = self.theme.node.dir
                after.theme_file_found.shout(found, found_base)

            else:
                missed_files.append(src)
                after.missed_file.shout(src)
                continue

            source = found.path
            relative_source = found_base.relative(found.path)
            destiny = destination.join(relative_source)
            ret.append(destiny)

            destiny_folder = dirname(destiny)

            if not exists(destiny_folder):
                before.folder_created.shout(relative_destiny)
                os.makedirs(destiny_folder)
                after.folder_created.shout(relative_destiny)

            already_exists = exists(destiny)
            should_update = already_exists and Node(destiny).could_be_updated_by(Node(source))

            if not already_exists or should_update:
                before.file_copied.shout(
                    source, destiny, position, total_files_to_copy)
                shutil.copy2(source, destiny)
                after.file_copied.shout(
                    source, destiny, position, total_files_to_copy)

        cloner = AssetsCloner(self.theme.index['static_path'])

        cloner.clone_to(destination_path)

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
        source_paths = self.node.trip_at(self.assets_path)
        total_files_to_copy = len(source_paths)

        for position, source_path in enumerate(source_paths, start=1):
            relative_path = self.node.relative(source_path)

            destination_path = dest_node.join(relative_path)
            destination_dir = dirname(destination_path)

            if not dest_node.contains(destination_dir):
                before.folder_created.shout(destination_dir)
                os.makedirs(destination_dir)
                after.folder_created.shout(destination_dir)

            before.file_copied.shout(
                source_path, destination_path, position, total_files_to_copy)
            shutil.copy2(source_path, destination_path)
            after.file_copied.shout(
                source_path, destination_path, position, total_files_to_copy)
            ret.append(destination_path)

        return ret
