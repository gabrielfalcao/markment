# The `Markment` class

```python
from markment import Markment
```

This class takes a markdown string and compiles into an html string
with all the markment filters, which also includes pygments-based
syntax highlighting.

#### optional arguments

###### `renderer`

An instance of `MarkmentRenderer` or `None`, you can pass your own
[misaka custom renderer](http://misaka.61924.nl/manual/#toc_14) or
even just inherit markment's [default renderer](https://github.com/gabrielfalcao/markment/blob/master/markment/engine.py#L39).

Although, if you want to customize the output that markment does you can just use use the [markment events api](events.md).

###### `url_prefix`

A callback that takes a path and returns the absolute path to that link.
This is used by markment to customize every markdown link and image's final output.


#### Example

```python
>>> from markment import Markment
>>> from markment.fs import Node
>>> root = Node("~/project/docs/")
>>>
>>> def calculate_path(path):
...     found = root.find(path)
...     if found:
...         return found.path
...     return path
...
>>> mm = Markment("# Title one\n[some reference to docs](some-docs.md)\n", url_prefix=calculate_path)
>>>
>>> mm.compile()
u'<h1 id="title-one" name="title-one"><a href="#title-one">Title one</a></h1>\n<p><a href="some-docs.md">some reference to docs</a></p>\n'
```

## retrieving the rendered html

```python
>>> from markment import Markment
>>> mm = Markment("#Title One")
>>> mm.rendered
u'<h1 id="title-one" name="title-one"><a href="#title-one">Title One</a></h1>'
```

## retrieving indexes

```python
>>> from markment import Markment
>>> mm = Markment("#Title One\n\n##Subtitle One\n\n##Subtitle Two\n\n###And so on...")
>>> mm.index()
[{u'text': 'Title One', u'level': 1, u'anchor': u'#title-one', u'child': [{u'text': 'Subtitle One', u'anchor': u'#subtitle-one', u'level': 2}, {u'text': 'Subtitle Two', u'level': 2, u'anchor': u'#subtitle-two', u'child': [{u'text': 'And so on...', u'anchor': u'#and-so-on---', u'level': 3}]}]}]
```
