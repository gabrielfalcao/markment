# Testing a complex sandbox

In the first implementation of static documentation generation in markment I ended up with a silly `static_url_callback` that looks for theme files in the project directory too.

I already tried to strip out the extra code that looks into the project directory for static files, and all the tests continue passing.

It doesn't make sense and before just stripping out that code without assuring that this misconception will never happen again in markment's source code.
