#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid
import mimetypes

from flask import (
    Flask,
    Response,
    url_for,
    session,
    redirect,
)

from markment.core import Project
from markment.ui import Theme


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

project = Project.discover(os.getcwdu())


def link(path):
    return url_for('.render_path', path=path)


@app.route("/")
def index():
    session['theme_name'] = 'touch-of-pink'

    return redirect(url_for('.render_path', path='README.md'))


@app.route("/preview/<path:path>")
def render_path(path):
    theme_name = session['theme_name']

    theme = Theme.load_by_name(theme_name)
    prefix = '/assets/{0}/'.format(theme_name)

    items = list(project.generate(theme, static_prefix=prefix, link=link))

    for generated in items:
        print "." * 10
        print

        if generated['relative_path'].endswith(path):
            return Response(generated['html'])

    print len(items)

    return Response('not found', status=404)


@app.route("/assets/<theme_name>/<path:path>")
def serve_asset(theme_name, path):
    theme = Theme.load_by_name(theme_name)
    contenttype = mimetypes.guess_type(path)[0]

    with open(theme.static_file(path)) as f:
        data = f.read()

    return Response(data, mimetype=contenttype)

if __name__ == "__main__":
    app.run(debug=True)
