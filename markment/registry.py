#!/usr/bin/env python
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

import os


def _function_matches(one, other):
    return (os.path.abspath(one.func_code.co_filename) == os.path.abspath(other.func_code.co_filename) and
            one.func_code.co_firstlineno == other.func_code.co_firstlineno)


class CallbackDict(dict):
    def append_to(self, where, when, function):
        if not any(_function_matches(o, function) for o in self[where][when]):
            self[where][when].append(function)

    def clear(self):
        for name, action_dict in self.items():
            for callback_list in action_dict.values():
                callback_list[:] = []


STEP_REGISTRY = {}
CALLBACK_REGISTRY = CallbackDict(
    {
        'all': {
            'before': [],
            'after': [],
        },
        'project_file_found': {
            'before_each': [],
            'after_each': [],
        },
        'file_copied': {
            'before_each': [],
            'after_each': [],
        },
        'missed_file': {
            'before_each': [],
            'after_each': [],
        },
        'markdown_table': {
            'before_each': [],
            'after_each': [],
        },
        'markdown_link': {
            'before_each': [],
            'after_each': [],
        },
        'markdown_header': {
            'before_each': [],
            'after_each': [],
        },
        'markdown_code': {
            'before_each': [],
            'after_each': [],
        },
        'markdown_image': {
            'before_each': [],
            'after_each': [],
        },
        'document_found': {
            'before_each': [],
            'after_each': [],
        },
        'html_persisted': {
            'before_each': [],
            'after_each': [],
        },
        'file_indexed': {
            'before_each': [],
            'after_each': [],
        },
        'folder_indexed': {
            'before_each': [],
            'after_each': [],
        },
        'folder_created': {
            'before_each': [],
            'after_each': [],
        },
        'asset_folder_created': {
            'before_each': [],
            'after_each': [],
        },
        'asset_file_copied': {
            'before_each': [],
            'after_each': [],
        },
    },
)


def call_hook(situation, kind, *args, **kw):
    for callback in CALLBACK_REGISTRY[kind][situation]:
        callback(*args, **kw)


def clear():
    CALLBACK_REGISTRY.clear()
