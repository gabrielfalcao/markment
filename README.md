# Markment
> version 0.0.1
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

## usage

Generate the documentation and output the files under `html` directory

```console
markment html
```

## theming

It currently has 1 theme: octomarks

```console
markment -t octomarks html
```

But you can develop themes very easily by writing jinja2 templates
