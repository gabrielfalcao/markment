# Supercharge your project's documentation

[![Build Status](https://secure.travis-ci.org/gabrielfalcao/markment.png?branch=master)](http://travis-ci.org/#!/gabrielfalcao/markment)
[github page](https://github.com/gabrielfalcao/markment)

Markment reads a `README.md` or `README.markdown` finds any references
to other `.md` or `.markdown` files and generates documentation for
them.

Markment is mostly compatible with github-flavored markdown


## Crash course in 3 simple steps


#### 1. Install markment

```console
pip install markment
```

#### 2. Go to a project that has one or more markdown files

```console
cd myproject
```


#### 3. Run markment!

```console
markment --output=./_generated-docs/
```

#### Done!


## Features

* Finds markdown files recursively in the given directory tree and generates documentation for them.

* Support to [metadata](docs/configuring.md) related to your
  project. (You can set project title, description, github url,
  download url and the themes might make use of it)

* Currently has 1 builtin theme [slate](https://github.com/jsncostello/slate) from github, but [I had forked](https://github.com/markment) and
  am already working on migrating some github-pages themes to Goals.

* You can write your own theme and use it right away through the simple [theme development api](docs/themes.md).

* Seriously, creating new themes is a breeze.

* Builtin [flask](http://flask.pocoo.org/) server so you can develop
  your themes preview the documentation before generating all of it.


## Future

These are some goals I want to achieve with markment for the next releases.

* Full-text search API + template.

* API documentation generation for python files (Similar to
  doxygen). I personally love markdown so much that I actually like to
  use as my documentation language inside of python docstrings.

## Purpose

Markment was initially created to empower the documentation pages at
[octomarks.io](http://octomarks.io), but only the programatic [api](docs/api.md) was being used.

Until one day at [Yipit](http://yipit.com/about/team) I had to do a [retrospective item](http://www.mountaingoatsoftware.com/scrum/sprint-retrospective/) to
improve our documentation. So I went ahead and turned markment into a full documentation generator.

We have internally a lot of documentation, but it just wasn't exposed
appropriately. Markment can now

You can see it live[here](http://octomarks.io/gabrielfalcao/markment)
