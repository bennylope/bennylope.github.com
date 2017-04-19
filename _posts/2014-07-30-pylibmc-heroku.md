---
published: true
title: "Installing pylibmc on Heroku"
subtitle: "That which is not documented will cause you grief"
category: programming
layout: post
permalink: /pylibmc-and-heroku/
soHelpful: true
comments: true
teaser: >
    Installing pylibmc on Heroku is pretty simple once you account for
    one small, undocumented gotcha.
---

[`pylibmc`](https://pypi.python.org/pypi/pylibmc) is a memcached client
for Python. It's a requirement for adding caching with memcached to a
Python application, like a Django project. However you can find
[several](http://stackoverflow.com/questions/11507639/memcached-on-heroku-w-django-cant-install-pylibmc-memcacheify)
[instances](http://stackoverflow.com/questions/14688799/heroku-django-error-when-installing-pylibmc)
where people have had difficulty installing it on Heroku.

The solution is actually mentioned in that first link, but I missed the
significance of it until checking out the [buildback source code](https://github.com/heroku/heroku-buildpack-python/blob/533def6b57a09a60c9dd7755958f12e56d3bf761/bin/steps/pylibmc#L19).

<script src="https://gist.github.com/bennylope/0e01a8ffef65374e5e0c.js">&nbsp;</script>

The problem I was having, and all of these others folks, too, is that I
was using multiple pip requirements files. As you can see on line 2, the
buildback checks for pylibmc in one place, `requirements.txt`, the base
file. My root `requirements.txt` was used only to inlclude
`requirements/production.txt`. `pylibmc` was never detected, so
`libmemcached` was never bootstrapped, and install failed. The solution
is just moving this requirement to the base file.

Instead of:

    -r requirements/production.txt

The `requirements.txt` file now looks like this:

    pylibmc==1.3.0
    -r requirements/production.txt

### About multiple requirements files

One response to this problem was that multiple pip requirements files
add more 'overhead' and breaks dev/production parity.

I fail to see what kind of overhead a few well organized requirements
add to a project. If nothing else, it's extremely convenient to be able
to break out *app* requirements from *development* requirements. For a
Django project, the core requirements would go into a `requirements/base.txt`
file and requirements like `Sphinx` (you do document, right?) and
`flake8` go into a `requirements/test.txt` file. This lets you tell
other developers to install from one pip requirements file, instead of
checking off each that they need. Same with a CI server.

As for dev/production parity, this shouldn't be a concern for the
aforementioned requirements. Especially when slug size is a potential
concern on Heroku, don't install stuff in production you don't need to
run the application. It's as simple as that. And on some teams, some
projects, breaking that perfect dev/production parity might be
acceptable. This is a tradeoff between environment parity and
environment overhead. Mac to Linux already breaks this parity, so you
need to assume you're working with VM's, e.g. Vagrant, using the same OS
at your target production system. That's a brilliant idea, but for
simpler, short-run projects not always necessary.

**Update**: the excellent folks at Memcachier have since updated [their
documentation](https://www.memcachier.com/documentation#django) to make this
explicit.
