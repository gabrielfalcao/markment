#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import time

import requests
from markment.fs import Node
from markment.ui import Theme
from markment.server import server


local_node = Node(__file__).dir

themes = [x.dir for x in reversed(local_node.parent.cd('markment/themes').grep('markment.yml'))]
output_path = local_node.join('_output')


for t in themes:
    print t.basename
