#!/usr/bin/env python
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

import os
import uuid
import mimetypes

from flask import (
    Flask,
    Response,
    url_for,
    redirect,
    g,
)

from markment.core import Project
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

    def link(path, current_document_info):
        if path.endswith('.md') or path.endswith('.markdown'):
            return url_for('.render_path', path=path)
        else:
            found = current_node.cd(path)
            relative_path = current_node.relative(found.path)
            return '/raw/{0}'.format(relative_path)

    def static_url_callback(path, current_document_info):
        if theme.node.find(path):
            return '/assets/{0}'.format(path)

        return '/raw/{0}'.format(path)

    @app.before_request
    def get_project():
        g.project = Project.discover(current_dir)

    @app.context_processor
    def inject_basics():
        return {
            'server_mode': True
        }

    @app.route("/")
    def index():
        return redirect(url_for('.render_path', path=g.project.meta['documentation']['index']))

    @app.route("/preview/<path:path>")
    def render_path(path):
        items = list(g.project.generate(theme, static_url_cb=static_url_callback, link_cb=link))

        for generated in items:
            if generated['relative_path'].endswith(path):
                return Response(generated['html'])

        return Response('not found', status=404)

    @app.route("/assets/<path:path>")
    def serve_asset(path):
        contenttype = mimetypes.guess_type(path)[0]

        with open(theme.static_file(path)) as f:
            data = f.read()

        return Response(data, mimetype=contenttype)

    return app
