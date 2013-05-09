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
    basename,
)
from os.path import isfile as isfile_base
from os.path import isdir as isdir_base


LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)


def isfile(path):
    if exists(path):
        return isfile_base(path)

    return '.' in split(path)[-1]


def isdir(path):
    if exists(path):
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
    def __init__(self, path):
        self.path = abspath(expanduser(path)).rstrip('/')
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
    def basename(self):
        return basename(self.path)

    @property
    def dir(self):
        if not self.is_dir:
            return self.parent
        else:
            return self

    @property
    def parent(self):
        return self.__class__(dirname(self.path))

    def reduce_to_base_path(self, path):
        levels = []
        while path.startswith(DOTDOTSLASH):
            levels.append('..')
            path = path.replace(DOTDOTSLASH, '', 1)

        way_back = os.sep.join(levels)
        return self.cd(way_back).dir.path, path, way_back

    def could_be_updated_by(self, other):
        return self.metadata.mtime < other.metadata.mtime

    def create_tree_if_not_exists(self):
        if not self.dir.exists:
            os.makedirs(self.dir.path)

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
            for root, folders, filenames in os.walk(path):
                for filename in filenames:
                    yield join(root, filename)

        return lazy and iterator() or list(iterator())

    def walk(self):
        return self.trip_at(self.path)

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
            for filename in self.walk():
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
            for filename in self.walk():
                if re.search(pattern, filename, flags):
                    yield self.__class__(filename)

        return lazy and iterator() or list(iterator())

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
        if isfile(self.join(new_path)):
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
        way_back = Node('/foo/bar').depth_of('/foo/bar/another/dir/file.py')
        assert way_back == '../../'

        way_back = Node('/foo/bar/docs/static/file.css').depth_of('/foo/bar/docs/intro/index.md')
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
        return open(self.join(path), *args, **kw)

    def __repr__(self):
        return '<markment.fs.Node (path={0})>'.format(self.path)


class TreeMaker(object):
    def __init__(self, path):
        self.path = abspath(path.rstrip('/'))
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

    def relative_link_callback(self, original_link, current_document_info, destination_root):
        fixed_link, levels = self.get_levels(original_link)

        is_markdown = self.regex.search(original_link)

        found = self.project.node.find(fixed_link)
        if not found:
            return original_link

        found_base = self.project.node.dir

        relative_path = found_base.relative(found.path)

        current_document_path = self.rename_markdown_filename(current_document_info['relative_path'])

        item_destination = destination_root.cd(relative_path)
        destination_document = destination_root.cd(current_document_path)

        prefix = item_destination.path_to_related(destination_document.path)

        if found.path not in self.files_to_copy and not is_markdown:
            self.files_to_copy.append(found.path)

        if prefix == './':
            prefix = prefix + fixed_link

        if is_markdown:
            prefix = self.rename_markdown_filename(prefix)

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
        in_local = self.project.node.find(link)

        if levels:
            prefix = link

        if in_local:
            found = in_local
            found_base = self.project.node.dir
            link = found_base.relative(found.path)

        elif in_theme:
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

        missed_files = []
        for src in self.files_to_copy:

            src = relpath(src)
            in_theme = self.theme.node.find(src)
            in_local = self.project.node.find(src)

            if in_local:
                found = in_local
                found_base = self.project.node.dir

            elif in_theme:
                found = in_theme
                found_base = self.theme.node.dir

            else:
                missed_files.append(src)
                continue

            source = found.path
            relative_source = found_base.relative(found.path)
            destiny = destination.join(relative_source)
            ret.append(destiny)
            destiny_folder = dirname(destiny)
            if not exists(destiny_folder):
                os.makedirs(destiny_folder)

            already_exists = exists(destiny)
            should_update = already_exists and Node(destiny).could_be_updated_by(Node(source))

            if not already_exists or should_update:
                shutil.copy2(source, destiny)

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

        for source_path in self.node.trip_at(self.assets_path):
            relative_path = self.node.relative(source_path)
            destination_path = dest_node.join(relative_path)
            destination_dir = dirname(destination_path)

            if not dest_node.contains(destination_dir):
                os.makedirs(destination_dir)

            shutil.copy2(source_path, destination_path)
            ret.append(destination_path)

        return ret
