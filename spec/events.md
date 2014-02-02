# Events

Markment uses [speakers](http://falcao.it/speakers/) for a simple, steady and synchonous [event system](http://en.wikipedia.org/wiki/Software_bus).

Under `markment.events` [you can find](https://github.com/gabrielfalcao/markment/blob/master/markment/events.py) its code in github, to see a full and up-to-date list of events.

Here is a list of the basic events you can listen in your own code when [extending](extending.md) markment.


## before.all

`before.all.shout(args)`

Called right after markment parses the command line arguments.

#### arguments

###### `args`

An instance of [`ArgumentParser`](http://docs.python.org/2/library/argparse.html#argparse.ArgumentParser) with
the command line arguments passed to the markment executable.

Check the examples section below to see how to use it.


## after.all

`after.all.shout(args, project, theme, generated)`

Called after markment is done with everything.

#### arguments

###### `args`

An instance of [`ArgumentParser`](http://docs.python.org/2/library/argparse.html#argparse.ArgumentParser) with
the command line arguments passed to the markment executable.

###### `project`

An instance of [`markment.core.Project`](../markment/core.py@Project) referencing the current documentation folder.

###### `theme`

An instance of [`markment.ui.Theme`](../markment/ui.py@Theme) referencing the current chosen theme.

###### `generated`

A list of strings containing the relative paths of the generated documentation files.


## after.folder_indexed

`after.folder_indexed.shout(folder_info, position, total_results, grep_result)`

Happens after markment finds a folder that contains one or more markdown files.

#### arguments

###### `folder_info`

A dictionary with metadata about the folder

###### `position`

An `int`. The current position in the operation of indexing folders and files. Always off by 1 (starts from 1)

###### `total_results`

Also an `int`. The total number of items that will be indexed.

###### `grep_result`

A list of [`markment.fs.Node`](../markment/fs.py@Node) with each markdown file that was found.


## after.file_indexed

`after.file_indexed.shout(file_info, position, total_results, grep_result)`

Happens after markment finds a file that contains one or more markdown files.

#### arguments

###### `file_info`

A dictionary with metadata about the file

###### `position`

An `int`. The current position in the operation of indexing files and files. Always off by 1 (starts from 1)

###### `total_results`

Also an `int`. The total number of items that will be indexed.

###### `grep_result`

A list of [`markment.fs.Node`](../markment/fs.py@Node) with each markdown file that was found.


## before.file_copied

`before.file_copied.shout(source, destiny, position, total_files_to_copy)`

Happens right before markment makes a call to [`shutil.copy2`](http://docs.python.org/2/library/shutil.html#shutil.copy2)

#### arguments

###### `source`

A string with the source path.

###### `destiny`

A string with the destination path.

###### `position`

An `int`. The current position in the list of files to be copied

###### `total_files_to_copy`

Also an `int`. The total number of items that have to be copied.


## after.file_copied

`after.file_copied.shout(source, destiny, position, total_files_to_copy)`

Happens right after markment calls [`shutil.copy2`](http://docs.python.org/2/library/shutil.html#shutil.copy2)

#### arguments

###### `source`

A string with the source path.

###### `destiny`

A string with the destination path.

###### `position`

An `int`. The current position in the list of files to be copied

###### `total_files_to_copy`

Also an `int`. The total number of items that have to be copied.

## after.missed_file

`after.missed_file.shout(path)`

Happens right after markment tried to look for a file that was referenced in a markdown link or image,
but the file could not be found within the current project.

#### arguments

###### `path`

## before.folder_created
## theme_file_found
## project_file_found
## html_persisted
## markdown_table
## markdown_link
## markdown_image
## markdown_header
## markdown_code
## document_found
## partially_rendering_markdown
## rendering_markdown
## rendering_html

## More examples

Markment uses the event system for printing messages in the console, generating sitemaps and a few other cool things.

You can check out those examples in the [plugins directory](https://github.com/gabrielfalcao/markment/tree/master/markment/plugins).
