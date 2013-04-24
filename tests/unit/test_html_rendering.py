# -*- coding: utf-8 -*-
from markment import Markment
from lxml import html as lhtml
from .base import MARKDOWN


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
