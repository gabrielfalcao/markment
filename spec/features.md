# Features

Markment has some cool features like **lots of builtin themes**,
**sitemap generation** and some more.

The section below wil guide you through its options and how they work together.


## Themes

You can check out all the available themes by running:

```sh
markment --themes
```

![themes.png](themes.png)

## Generating a sitemap

You might want to host your project's documentation. In such case, you
might want search engines to find your documentation more easily.

Markment can generate a sitemap for you, all you need is to tell it
what is your url prefix.

For example, if you want to host your project's documentation using
[github pages](http://pages.github.com/) you will need to use the url form `http://{your-github-username}.github.io/{your-project-name}`.

```sh
markment --sitemap-for="http://gabrielfalcao.github.io/lettuce"
```
