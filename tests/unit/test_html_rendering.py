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

from markment import Markment
from markment.engine import MarkmentRenderer

from lxml import html as lhtml
from .base import MARKDOWN


def test_prefix_link_when_needed():
    "MarkmentRenderer#prefix_link_if_needed should prefix if link is relative"
    renderer = MarkmentRenderer()
    renderer.url_prefix = 'http://awesome.com'

    result = renderer.prefix_link_if_needed('bar.png')
    result.should.equal('http://awesome.com/bar.png')


def test_prefix_link_when_not_needed():
    "MarkmentRenderer#prefix_link_if_needed should NOT prefix if link is absolute"
    renderer = MarkmentRenderer()
    renderer.url_prefix = 'http://awesome.com'

    result = renderer.prefix_link_if_needed('http://ok.com/bar.png')
    result.should.equal('')


def test_prefix_link_when_not_needed_provided():
    "MarkmentRenderer#prefix_link_if_needed should NOT prefix if link is absolute"
    renderer = MarkmentRenderer()
    result = renderer.prefix_link_if_needed('bar.png')
    result.should.equal('')


def test_anchors_in_1st_level_headers():
    "Markment should put anchors in 1st level headers"

    MD = MARKDOWN("""
    # API Reference

    some content
    """)

    mm = Markment(MD)

    dom = lhtml.fromstring(mm.rendered)

    headers = dom.cssselect("h1")

    headers.should.have.length_of(1)

    h1 = headers[0]
    h1.attrib.should.have.key("name").being.equal("api-reference")
    h1.attrib.should.have.key("id").being.equal("api-reference")

    links = h1.getchildren()
    links.should.have.length_of(1)

    a = links[0]
    a.text.should.equal("API Reference")
    a.attrib.should.have.key("href").equal("#api-reference")


def test_anchors_in_2nd_level_headers():
    "Markment should put anchors in 2nd level headers"

    MD = MARKDOWN("""
    # API Reference

    ## Rendering content
    """)

    mm = Markment(MD)

    dom = lhtml.fromstring(mm.rendered)

    headers = dom.cssselect("h2")

    headers.should.have.length_of(1)

    h2 = headers[0]
    h2.attrib.should.have.key("name").being.equal("rendering-content")
    h2.attrib.should.have.key("id").being.equal("rendering-content")

    links = h2.getchildren()
    links.should.have.length_of(1)

    a = links[0]
    a.text.should.equal("Rendering content")
    a.attrib.should.have.key("href").equal("#rendering-content")


def test_code_block():
    "Markment should render code blocks"

    MD = MARKDOWN("""
    # API Reference

    This is good

    ```python
    import os
    os.system('ls /')
    ```

    This is not good

    ```python
    import os
    os.system('sudo rm -rf /')
    ```
    """)

    mm = Markment(MD)

    dom = lhtml.fromstring(mm.rendered)

    code_blocks = dom.cssselect("div.highlight pre")

    code_blocks.should.have.length_of(2)

    code1, code2 = code_blocks

    code1.attrib.should.have.key("name").equal("api-reference-example-1")
    code2.attrib.should.have.key("name").equal("api-reference-example-2")


def test_code_block_guesses_lexer():
    "Markment should render code blocks even without a language specified"

    MD = MARKDOWN("""
    # API Reference

    This is good

    ```
    import os
    os.system('ls /')
    ```

    This is not good

    ```python
    import os
    os.system('sudo rm -rf /')
    ```
    """)

    mm = Markment(MD)

    dom = lhtml.fromstring(mm.rendered)

    code_blocks = dom.cssselect("div.highlight pre")

    code_blocks.should.have.length_of(2)

    code1, code2 = code_blocks

    code1.attrib.should.have.key("name").equal("api-reference-example-1")
    code2.attrib.should.have.key("name").equal("api-reference-example-2")


def test_image_relative():
    "Markment should render images with relative path"

    MD = MARKDOWN("""
    # Awesome project

    ![LOGO](logo.png)
    """)

    mm = Markment(MD, url_prefix='http://falcao.it')

    dom = lhtml.fromstring(mm.rendered)

    images = dom.cssselect("img")

    images.should.have.length_of(1)

    img = images[0]

    img.attrib.should.have.key("src").equal("http://falcao.it/logo.png")
    img.attrib.should.have.key("alt").equal("LOGO")


def test_image_relative_with_callback():
    "Markment should render images with relative path"

    MD = MARKDOWN("""
    # Awesome project

    ![LOGO](logo.png)

    [Documentation](docs.md)
    """)

    def process_url(path):
        if path.lower().endswith("md"):
            return "http://markdown.com/{0}".format(path)
        else:
            return "http://images.com/{0}".format(path)

    mm = Markment(MD, url_prefix=process_url)

    dom = lhtml.fromstring(mm.rendered)

    images = dom.cssselect("img")

    images.should.have.length_of(1)

    img = images[0]

    img.attrib.should.have.key("src").equal("http://images.com/logo.png")
    img.attrib.should.have.key("alt").equal("LOGO")

    links = dom.cssselect("a")

    links.should.have.length_of(2)

    a = links[-1]

    a.attrib.should.have.key("href").equal("http://markdown.com/docs.md")


def test_image_absolute():
    "Markment should render images with absolute path"

    MD = MARKDOWN("""
    # Awesome project

    ![LOGO](http://octomarks.io/logo.png)
    """)

    mm = Markment(MD, url_prefix='http://falcao.it')

    dom = lhtml.fromstring(mm.rendered)

    images = dom.cssselect("img")

    images.should.have.length_of(1)

    img = images[0]

    img.attrib.should.have.key("src").equal("http://octomarks.io/logo.png")
    img.attrib.should.have.key("alt").equal("LOGO")


def test_link_relative():
    "Markment should render links with relative path"

    MD = MARKDOWN("""
    [LOGO](file.md)
    """)

    mm = Markment(MD, url_prefix='http://falcao.it')

    dom = lhtml.fromstring(mm.rendered)

    links = dom.cssselect("a")

    links.should.have.length_of(1)

    a = links[0]

    a.attrib.should.have.key("href").equal("http://falcao.it/file.md")
    a.text.should.equal('LOGO')


def test_link_absolute():
    "Markment should render links with absolute path"

    MD = MARKDOWN("""
    [LOGO](http://octomarks.io/file.md)
    """)

    mm = Markment(MD, url_prefix='http://falcao.it')

    dom = lhtml.fromstring(mm.rendered)

    links = dom.cssselect("a")

    links.should.have.length_of(1)

    a = links[0]

    a.attrib.should.have.key("href").equal("http://octomarks.io/file.md")
    a.text.should.equal('LOGO')


def test_markment_doesnt_fail_if_has_no_headers():
    "Markment should find and index 3rd level headers"

    MD = MARKDOWN("""
    ```python
    poor code, doesn't have a title
    ```

    """)

    mm = Markment(MD)

    mm.index().should.equal([])


def test_markment_renders_tables():
    "Markment should be able to render tables"

    MD = MARKDOWN('''
    | button                                     | code                                         |
    | ---------------------------                | :-------------------------------:            |
    | <a class="btn btn-success">Success</a>     | `<a class="btn btn-success">Success</a>`     |
    ''')

    mm = Markment(MD)

    dom = lhtml.fromstring(mm.rendered)

    table = dom.cssselect("table.table")

    table.should_not.be.empty

    table_data = dom.cssselect('tr > td')
    table_data.should.have.length_of(2)

    column1, column2 = table_data

    button = column1.getchildren()
    button.should_not.be.empty
    button[0].text.should.equal('Success')

    code = column2.getchildren()
    code.should_not.be.empty
    code[0].text.should.equal('<a class="btn btn-success">Success</a>')
