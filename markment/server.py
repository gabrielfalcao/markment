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
from functools import partial

from markment.core import Project
from markment.ui import Theme
from markment.fs import Node


def server(source_path, theme):
    current_dir = os.path.abspath(source_path)
    current_node = Node(current_dir)
    static_url_path = '/raw'

    app = Flask(__name__, static_folder=current_dir, static_url_path=static_url_path)
    app.secret_key = uuid.uuid4().hex

    def url_prefix_callback(link, current_document_info):
        target = link.lower()

        if target.endswith(".md") or target.endswith(".markdown"):
            return link
        else:
            return "{0}/{1}".format(static_url_path, link.lstrip('/'))

    project = Project.discover(current_dir)

    def link(path, current_document_info):
        if path.endswith('.md') or path.endswith('.markdown'):
            return url_for('.render_path', path=path)
        else:
            found = current_node.cd(path)
            relative_path = current_node.relative(found.path)
            return '/raw/{0}'.format(relative_path)

    def static_url_callback(path, current_document_info, theme):
        if theme.node.find(path):
            return '/assets/{0}/{1}'.format(session['theme_name'], path)

        return '/raw/{0}'.format(path)

    @app.route("/")
    def index():
        session['theme_name'] = 'slate'
        return redirect(url_for('.render_path', path=project.meta['documentation']['index']))

    def get_theme():
        if 'theme_name' not in session:
            session['theme_name'] = 'slate'

        return session['theme_name']

    @app.route("/preview/<path:path>")
    def render_path(path):
        theme_name = get_theme()

        theme = Theme.load_by_name(theme_name)

        items = list(project.generate(theme, static_url_cb=partial(static_url_callback, theme=theme), link_cb=link))

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

    return app
