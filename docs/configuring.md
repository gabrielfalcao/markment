# Configuring your project

Markment **might** use some extra metadata to render your documentation.

It's done by reading a file called `.markment.yml` in the root folder of your documentation.

Below there is a full-featured example of a `.markment.yml` file.


```yaml
project:
  name: This title will probably be used in each <title> tag of the templates
  version: 1.2.3
  description: This is a short
  github_url: http://github.com/yourname/yourproject
  tarball_download_url: http://yoururl.com/file.tgz  # if not given defaults to "{github_url}/archive/master.tar.gz"
  zipball_download_url: http://yoururl.com/file.zip  # if not given defaults to "{github_url}/archive/master.zip

documentation:
  index: TODO.md  # the file that should be considered the main one. Defaults to README.md
```
