# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from PIL import Image
from markment.fs import Node

screenshots = Node('spec/screenshots').grep('[.]png$')
for image in screenshots:
    sys.stdout.write("cropping {0}...".format(image.basename))
    im = Image.open(image.path)
    try:
        im = im.crop((0, 0, 1200, 500))
    except Exception as e:
        print "FAILED:", e
        continue

    im.save(image.path)
    print "OK"
