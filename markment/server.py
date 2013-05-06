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


current_dir = os.path.abspath(os.getcwdu())
static_url_path = '/raw'

app = Flask(__name__, static_folder=current_dir, static_url_path=static_url_path)
app.secret_key = uuid.uuid4().hex

project = Project.discover(current_dir, url_prefix=static_url_path)


def link(path):
    return url_for('.render_path', path=path)


@app.route("/")
def index():
    session['theme_name'] = 'touch-of-pink'

    return redirect(url_for('.render_path', path='README.md'))


def get_theme():
    if 'theme_name' not in session:
        session['theme_name'] = 'touch-of-pink'

    return session['theme_name']


@app.route("/preview/<path:path>")
def render_path(path):
    theme_name = get_theme()

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
