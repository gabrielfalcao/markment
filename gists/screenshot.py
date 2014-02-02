# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from sleepyhollow import SleepyHollow
browser = SleepyHollow()

response = browser.get("http://localhost:5000", config={
    'screenshot': True,
    'width': 1300,
    'height': 600,
})

response.save_screenshot("../spec/screenshots/{0}.png".format(sys.argv[1]))
