#!/usr/bin/env python
# -*- coding: utf-8 -*-


def MARKDOWN(m):
    """The tests below have 4 spaces of indentation in the beginning,
    so this function dedents it and strips the final result"""

    return "\n".join(s[4:] for s in m.splitlines()).strip()
