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
import sys
from collections import OrderedDict, defaultdict
from functools import wraps

from .handy import underlinefy, nicepartial
ENCODE = 'utf-8'

class Function(object):
    def __init__(self, func):
        self.call = func

        self.name = func.__name__
        self.filename = os.path.relpath(func.func_code.co_filename)
        self.lineno = func.func_code.co_firstlineno + 1

    @property
    def module_name(self):
        return self.filename_without_extension.replace(os.sep, '.')

    @property
    def filename_without_extension(self):
        return os.path.splitext(self.filename)[0]

    def as_string(self, **kwargs):
        kw = OrderedDict()
        kw['name'] = self.name
        kw['lineno'] = self.lineno
        kw['filename'] = self.filename

        kw.update(kwargs)
        itemize = lambda d: ", ".join(['{0}="{1}"'.format(k, d[k]) for k in d])
        return 'Function({0})'.format(itemize(kw))

    def __str__(self):
        return self.as_string()

    def __repr__(self):
        return self.as_string().encode(ENCODE)

    def __call__(self, *args, **kw):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return self.call(*args, **kw)


class Speaker(object):
    def __init__(self, name, actions, output=None):
        self.name = underlinefy(name)
        self.actions = OrderedDict()
        self.hooks = defaultdict(list)
        self.default_exception_handler = Function(self.__base_exc_handler)
        self._exception_handler = self.default_exception_handler
        if not isinstance(actions, list):
            raise TypeError('actions must be a list of strings. Got %r' % actions)

        for action in map(underlinefy, actions):
            self.actions[action] = nicepartial(self.for_decorator, action)
            self.actions[action].shout = nicepartial(self.shout, action)
            setattr(self, action, self.actions[action])

    def __str__(self):
        return 'Speaker(name={0}, actions={1}, total_hooks={2})'.format(
            self.name, self.actions, len(self.hooks))

    def __repr__(self):
        return str(self).encode(ENCODE)

    def __base_exc_handler(self, speaker, exception, args, kwargs):
        raise

    def exception_handler(self, callback):
        if self._exception_handler is not self.default_exception_handler:
            raise RuntimeError('Attempt to register {0} as an exception_handler for {1}, but it already has {2} assigned'.format(
                Function(callback),
                self,
                self.exception_handler,
            ))

        self._exception_handler = Function(callback)
        return callback

    def for_decorator(self, action, callback):
        safe_action = underlinefy(action)

        responder = Function(callback)

        @wraps(responder.call)
        def wrapper(*args, **kw):
            try:
                res = callback(self, *args, **kw)
            except Exception as exc:
                if self.exception_handler:
                    return self._exception_handler(self, exc, args, kw)

            return res

        responder.key = b'{speaker}:{action}[{module}:{hook}:{lineno}]'.format(
            speaker=self.name,
            action=safe_action,
            module=responder.module_name,
            hook=wrapper.__name__,
            lineno=responder.lineno,
        )
        self.hooks[action].append(wrapper)
        return responder

    def shout(self, action, *args, **kw):
        for hook in self.hooks[action]:
            result = hook(*args, **kw)
            if result:
                return result
