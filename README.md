# Markment

![logo.png](logo.png)
[![Build Status](https://secure.travis-ci.org/gabrielfalcao/markment.png?branch=master)](http://travis-ci.org/#!/gabrielfalcao/markment)

Generate beautiful documentation for your github projects


Markment reads a `README.md` or `README.markdown` finds any references
to other `.md` or `.markdown` files and generates documentation for
them.

Markment is 100% compatible with github-flavored markdown

## installation

```console
pip install markment
```

## API

Create an instance of `markment.Markment` with a markdown file and an
absolute path to fallback relative links (optional):


```python
>>> from markment import Markment
>>> mm = Markment("#Title One\n\n#Title Two")
```

### retrieving the rendered html

```python
>>> from markment import Markment
>>> mm = Markment("#Title One")
>>> mm.rendered
u'<h1 id="title-one" name="title-one"><a href="#title-one">Title One</a></h1>'
```


### retrieving indexes

```python
>>> from markment import Markment
>>> mm = Markment("#Title One\n\n##Subtitle One\n\n##Subtitle Two\n\n###And so on...")
>>> mm.index()
[{u'text': 'Title One', u'level': 1, u'anchor': u'#title-one', u'child': [{u'text': 'Subtitle One', u'anchor': u'#subtitle-one', u'level': 2}, {u'text': 'Subtitle Two', u'level': 2, u'anchor': u'#subtitle-two', u'child': [{u'text': 'And so on...', u'anchor': u'#and-so-on---', u'level': 3}]}]}]
```

## purpose

Markment was created to empower the documentation pages at
[octomarks.io](http://octomarks.io).

You can see it live [here](http://octomarks.io/gabrielfalcao/markment)
