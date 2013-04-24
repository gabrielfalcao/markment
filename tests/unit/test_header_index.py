#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sure import expect
from markment import Markment


def MARKDOWN(m):
    """The tests below have 4 spaces of indentation in the beginning,
    so this function dedents it and strips the final result"""

    return "\n".join(s[4:] for s in m.splitlines()).strip()


def test_markment_contains_the_raw_markdown():
    "Markment should contain the original markment"

    MD = MARKDOWN("""
    # Installation
    Such a cool lib

    # API Reference
    """)

    mm = Markment(MD)

    expect(mm.raw).to.equal(MD)


def test_markment_finds_1st_level_headers():
    "Markment should find and index 1st level headers"

    MD = MARKDOWN("""
    # Installation

    # Tutorial

    # API Reference

    """)

    mm = Markment(MD)

    expect(mm.index()).to.equal([
        {"text": "Installation", "level": 1},
        {"text": "Tutorial", "level": 1},
        {"text": "API Reference", "level": 1},
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
        {"text": "Installation", "level": 1, "child": [
            {"text": "Through PIP", "level": 2},
            {"text": "Compiling manually", "level": 2},
        ]},
    ])
