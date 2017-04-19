---
title: "Heroku's little helper script"
subtitle: "Or, typing is tedious"
category: programming
layout: post
permalink: /a-heroku-helper-script/
soHelpful: true
published: true
comments: true
teaser: >
    The Heroku toolbelt is a CLI tool for managing Heroku apps. As command line
    interfaces go, it's pretty nicely designed. In a
    multi-environment Heroku deployment, i.e. with staging and production
    deploys, using a project specific script helps consolidate app naming and
    pipeline based deployment.

---

In a standard single application Heroku deployment, the app name is usually implicit if your
working directory is a Heroku app with your Heroku repository. Once you
introduce another deployed environment, like a staging environment, you need to
specify the app name, e.g. `myappname` or `myappname-staging`. So that instead
of running something like:

    heroku config

You'll need to run:

    heroku config --app myappname-staging

Some extra keystrokes but nothing too horrible.

For our standard Django deployment there are a few minimum tasks that need to
be run as part of a deployment, including updating dependencies, collecting
static files, and making database changes. The standard Heroku Python buildback
takes care of the first two, so we just need to make database changes. It's one
extra step, but it's one extra to remember every time.

Instead, the helper script here wraps several common tasks, like those
associated with deployment, and provides consistent environment naming, across
projects, for interacting with Heroku deployments.

### Named environments, not apps

Instead of pushing to the specified Git remote and then executing commands
against the specified app like so:

    git push heroku-staging master
    heroku run python myapp/manage.py migrate --app=myapp-name

It's one environment based command:

    ./heroku staging deploy

And this is similar for executing any basic Heroku CLI command. Updating
configuration:

    heroku config:set MYVAR=True --app=myapp-name

Becomes:

    ./heroku production config:set MYVAR=True

This last command isn't such a big win in saving you from typing, but it does
introduce consistency, focused on environment rather than app name. Leading
with the environment name makes it very clear where your command is targeted.

### Django management commands

Since the particular focus here is for Django projects, the script has a helper
for running Django management commands. Instead of:

    heroku run python myapp/manage.py custom_management_command --app=myapp-name

The script environment handling gets us to this:

    ./heroku production run python myapp/manage.py some_management_command

And a simple command addition let's us replace that boilerplate.

    ./heroku production dj some_management_command

### Pipeline deployment

With multiple environments it makes sense to adopt Heroku's [pipelines
feature](https://devcenter.heroku.com/articles/labs-pipelines) for deployment.
This feature allows you to deploy from one Heroku environment to another by
copying the entire slug. This means full replication of course and very
quickly. We can wrap this up in the script, too.

In the workflow we have set up, the user should be shown the environment diff
first, then verify that they do want to promote, and then promote the staging
environment. Instead of:

    heroku pipeline:diff --app=myappname-staging
    heroku pipeline:promote --app=myappname-staging
    heroku run python afficon/manage.py syncdb --noinput --app=myappname
    heroku run python afficon/manage.py migrate --app=myappname

This can be run using:

    ./heroku promote

The script will first take a diff and ask for confirmation, then promote the
slug, and lastly run any commands necessary to complete deployment.

### The script

You can grab a copy of this script (which requires modification, of course)
from the embedded gist below. It's also included in my [cookiecutter Django
project template](https://github.com/bennylope/cookiecutter-django).

<script
src="https://gist.github.com/bennylope/42993351581b248a364b.js">&nbsp;</script>
