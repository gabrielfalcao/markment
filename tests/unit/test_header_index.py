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

from sure import expect
from markment import Markment
from .base import MARKDOWN


def test_markment_contains_the_raw_markdown():
    "Markment should contain the original markment"

    MD = MARKDOWN("""
    # Installation
    Such a cool lib

    # API Reference
    """)

    mm = Markment(MD)

    mm.raw.should.equal(MD)


def test_markment_finds_1st_level_headers():
    "Markment should find and index 1st level headers"

    MD = MARKDOWN("""
    # Installation

    # Tutorial

    # API Reference

    """)

    mm = Markment(MD)

    mm.index().should.equal([
        {"text": "Installation", "level": 1, "anchor": "#installation"},
        {"text": "Tutorial", "level": 1, "anchor": "#tutorial"},
        {"text": "API Reference", "level": 1, "anchor": "#api-reference"},
    ])


def test_markment_finds_2nd_level_headers():
    "Markment should find and index 2nd level headers"

    MD = MARKDOWN("""
    # Installation

    chuck norris

    ## Through PIP


    ## Compiling manually


    """)

    mm = Markment(MD)

    expect(mm.index()).to.equal([
        {"text": "Installation",
         "anchor": "#installation",
         "level": 1, "child": [
             {"text": "Through PIP", "level": 2, "anchor": "#through-pip"},
             {"text": "Compiling manually", "level": 2, "anchor": "#compiling-manually"},
         ]},
    ])


def test_markment_finds_3rd_level_headers():
    "Markment should find and index 3rd level headers"

    MD = MARKDOWN("""
    # Installation

    chuck norris

    ## Through PIP

    ## Compiling manually

    ### Caveats

    """)

    mm = Markment(MD)

    mm.index().should.equal([
        {"text": "Installation", "level": 1,
         "anchor": "#installation",
         "child": [
             {"text": "Through PIP", "level": 2, "anchor": "#through-pip"},
             {"text": "Compiling manually", "level": 2,
              "anchor": "#compiling-manually",
              "child": [
                  {"text": "Caveats", "level": 3, "anchor": "#caveats"},
              ]},
         ]},
    ])


def test_markment_doesnt_fail_if_has_no_headers():
    "Markment should find and index 3rd level headers"

    MD = MARKDOWN("""
    ## Installation
    """)

    mm = Markment(MD)

    mm.index().should.equal([
        {
            "text": "Installation",
            "level": 2,
            "anchor": "#installation"
        },
    ])
