---
title: "Automated linting with flake8 and pre-commit hooks"
permalink: /flake8-pre-commit-hooks/
layout: post
category: programming
published: true
date: 2015-03-27 15:40:15
teaser: >
    Clean code does not make good code, but it certainly makes good code
    easier. Using a pre-commit Git hook is an excellent way of
    maintaining team-wide standards, and this example shows how to do
    this in a way that everyone can use, regardless of their Git client.
---

Clean code does not make code good, but it certainly makes writing good
code a lot easier. And it's far easier to read clean code, easier to
debug, to reason about, and easier to maintain. Which all of course
means happier developers and faster development cycles - at least in the
long run.

One of the prime tools for maintaining clean code is a linter, a tool
that checks code for basic style problems. I've found the Python tool
[flake8](flake8.readthedocs.org) incredibly helpful, especially its
combination of linting (too many lines!), static analysis (unused
imports!), and complexity analysis (too many code branches in a
function!). It doesn't guarantee good code, but it makes the basics much
easier and in the end contributes to better code.

It's easy enough to run the program, but it gives better feedback when
used directly in an editor, e.g. through a vim plugin, or a Git
pre-commit hook, checking for issues before committing them. On team
projects it's easier to focus first on the pre-commit hook, leaving the
choice of editor configuratio to each developer.

The flake8 tool actually has a feature to support this, however in this
case it turns out to be a bit more than necessary, and simultaneously
not flexible enough. The tool installs a Python script as your
pre-commit hook - you can have only one - and it uses some additional
configuration just for the hook. This is unnecessary because we've
already got flake8 configuration in our `tox.ini` project file, and not
flexible enough because I want to add more than just flake8 checks to
the pre-commit hook.

The solution is a simple bash script that explicitly returns an error
code (`1`) for flake8 issues and reports them to the user.

Here's a stripped down example.

{% highlight bash %}
#!/usr/bin/env sh

EXIT_CODE=0

# flake8
FLAKE_ERRORS=$( $VIRTUAL_ENV/bin/flake8 app | tee )
if  [[ $FLAKE_ERRORS ]]; then
    echo "$FLAKE_ERRORS"
    EXIT_CODE=1
fi

# check for livereload tags
if grep -r "livereload" app/templates; then
    echo "\nFound livereload scripts in template builds! Remove these before commiting"
    EXIT_CODE=1
fi

exit $EXIT_CODE
{% endhighlight %}

After setting up an exit code variable, the script runs `flake8` using
the current virtual environment on the designated app directory. The
full script comes with instructions for adding an explicit path for this
variable. The script as-is works great for CLI users, but for GUI Git
interfaces like SourceTree you need to provide the full path.

`flake8` doesn't return an exit code if there are any errors in the code
found, so we need to raise that ourselves. We save this to a variable
rather than raise immediately so that we can finish all of the linting
and report all issues before exiting.

Now the script runs additional linting checks, like this one to ensure
that a script added by a helper application isn't accidentally
committed. Additional scripts here might include JSLint, JSHint, or even
build steps that you want carried out in the event some code is updated.

Again, these checks won't make your code *good* but they will help your
team maintain reasonable standards and keep everyone sane.
