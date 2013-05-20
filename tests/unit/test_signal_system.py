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

from mock import Mock
from markment.bus import Function, Speaker


def test_function_as_string():
    "Function#as_string"

    def testing():
        pass

    s = Function(testing)

    str(s).should.equal('Function(name="testing", lineno="27", filename="tests/unit/test_signal_system.py")')


def test_function_repr():
    "repr(#Function)"

    def testing():
        pass

    s = Function(testing)

    repr(s).should.equal(b'Function(name="testing", lineno="38", filename="tests/unit/test_signal_system.py")')


def test_speaker_with_wrong_parameter():
    "Speaker takes list of strings"

    Speaker.when.called_with("Testing", "foo").should.throw(
        TypeError, "actions must be a list of strings. Got u'foo'")


def test_speaker_as_string():
    "Speaker as string"

    sp = Speaker("AwesomeSauce", ['do this', 'do that'])
    str(sp).should.eql("Speaker(name=awesomesauce, actions=OrderedDict([(u'do_this', partial:for_decorator), (u'do_that', partial:for_decorator)]), total_hooks=0)")


def test_listeners_hear_to_speakers():
    "Listeners should hear to speaker"
    before = Speaker('before', ['file_created'])

    @before.file_created
    def obeyer(event, node):
        node.received_successfully(True)

    node = Mock()
    node.path = 'foo/bar'
    before.shout('file_created', node)
    node.received_successfully.assert_called_once_with(True)


def test_speaker_keys():
    "Speakers should have keys"

    def obeyer(speaker, node):
        node.path.should.equal('foo/bar')

    sp = Speaker('before', ['file_created'])
    sp.file_created(obeyer).key.should.equal(
        'before:file_created[tests.unit.test_signal_system:obeyer:77]')


def test_listeners_with_exceptions():
    "Listeners by default raise exceptions"
    before = Speaker('on', ['file_created'])

    @before.file_created
    def obeyer(event):
        raise IOError("You got served")

    before.shout.when.called_with('file_created').should.throw(
        IOError, "You got served")


def test_listeners_returning_values():
    "Listeners by default raise exceptions"
    before = Speaker('on', ['file_created'])

    calls = []

    @before.file_created
    def obeyer1(event):
        calls.append(event)

    @before.file_created
    def obeyer2(event):
        calls.append(event)
        return len(calls)

    before.file_created.shout().should.equal(2)


def test_listeners_with_exception_handler():
    "Speakers can have custom exception handlers"
    before = Speaker('on', ['file_created'])

    ensure = Mock()

    @before.exception_handler
    def handler(speaker, exception, args, kwargs):
        speaker.should.equal(before)
        exception.should.be.an(IOError)
        args.should.be.a(tuple)
        args.should.equal(("YAY",))
        kwargs.should.be.a(dict)
        kwargs.should.equal({'awesome': True})
        ensure.was_called()

    @before.file_created
    def obeyer(event, *args, **kwargs):
        args.should.be.a(tuple)
        args.should.equal(("YAY",))
        kwargs.should.be.a(dict)
        kwargs.should.equal({'awesome': True})
        raise IOError("You got served")

    before.shout('file_created', "YAY", awesome=True)
    ensure.was_called.assert_called_once_with()


def test_2_listeners_with_exception_handler():
    "It's forbidden to have 2 exception handlers"
    before = Speaker('on', ['file_created'])

    @before.exception_handler
    def handler(speaker, exception, args, kwargs):
        pass

    before.exception_handler.when.called_with(lambda: None).should.throw(
        RuntimeError, 'Attempt to register Function(name="<lambda>", lineno="151", filename="tests/unit/test_signal_system.py") as an exception_handler for Speaker(name=on, actions=OrderedDict([(u\'file_created\', partial:for_decorator)]), total_hooks=0), but it already has <bound method Speaker.exception_handler of Speaker(name=on, actions=OrderedDict([(u\'file_created\', partial:for_decorator)]), total_hooks=0)> assigned')
