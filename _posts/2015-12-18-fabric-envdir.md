---
title: "Managing configuration with envdir, remotely"
permalink: /managing-envdir-with-fabric/
layout: post
published: true
date: 2015-12-18
teaser: >
    envdir lets you manage persistent key/value data for
    environment-based configuration using the file system. It's a great
    way of adding 12-factor compatible configuration but it's no easier
    to manage remotely. Here's how to do just that using Fabric.
---

> envdir runs another program with environment modified according to
> files in a specified directory.

envdir is a component of
[daemontools](http://cr.yp.to/daemontools/envdir.html) subsequently
[ported to Python](https://github.com/jezdez/envdir)
that does one thing: it reads files from a specified directory and
injects the names and values of those files as environment variables
into the environment of a specified process (which is subsequently run).

"That's it" but it turns out to be quite handy.

### Hard coded secrets and secret settings files

How do you manage environment specific configuration for deployed apps?
Or secrets? You could put everything in a configuration file, in Django
it'd be `settings.py` and commit it and hope no ever finds the database
passwords and API keys you've added. (Hint: no). Or, to break things out
by environment you could use distinct configuration files, named after
each target environment. This works better, but you still have the issue
of secrets like passwords.

Here a common solution is to import from a non-source controlled file.
This is obviously better for security as it's not committed to your
repo, but managing the secrets file isn't obvious. You'll probably have
to log into the server and edit the file in frickin' `nano`.

This breaks down a bit if you use different releases and need to start
copying the settings file. You can edit the copy in the source cache
directory, but then you need to make a new deployment just to activate
the new settings. And if you edit the file in the latest release
directory you'll lose these updates without duplicating said update in
the cached directory.

### Keeping settings outside the project

A better solution is to keep these settings outside of the project and
its directory altogether. They can be sourced from a file kept in a
specified location or you can use the system's environment to feed
configuration values to the process.

The choice for me comes down to two questions: compatability with the
application and ease of use for managing the values.

Having worked with Heroku-deployed apps enough and Foreman/Honcho for
running Django apps locally, both the style of storing and managing the
values by envirionment variable is very appealing.

### envdir and the process

I want to motivate envdir by working backwards, from running the
process, that is.

To run an app with envdir you specify the directory where you
configuration values are stored and the process to run.

```bash
envdir /path/to/directory/ process
```

That's it.

So to run, say, gunicorn:

```bash
envdir /var/apps/myapp/config gunicorn coolapp.wsgi:application --port=5000
```

That's the only change necessary for getting these values *into* your
application.

### Storing variables using envdir

The next question is how do you store them. envdir relies on a
NoSQL database called the file system for persistent local key/value
storage.

This diagram from the Python port is useful:

```bash
$ tree envs/prod/
envs/prod/
├── DJANGO_SETTINGS_MODULE
├── MYSITE_DEBUG
├── MYSITE_DEPLOY_DIR
├── MYSITE_SECRET_KEY
└── PYTHONSTARTUP

0 directories, 3 files
$ cat envs/prod/DJANGO_SETTINGS_MODULE
mysite.settings
```

In case you missed it, you have a directory with a bunch of files, the
name of each file represents the name of the environment variable, and
the value of the variable is stored as the file content.

### Managing the values

Okay, running this is all very simple, but why use a littany of little
files instead of a single file?

The first reason for me was that there's already a well tested tool that
does what I want. I could find or write a tool to read these values from
a single file (I've used shell scripts and custom Django `manage.py`
scripts to do this), of course. The second issue is that it ends up
being simpler in the end working with many little files. The file system
protects against accidental duplication which is one nice feature.

It's also easier to manage remotely and that's ultimately the winner for
me. I mentioned using Heroku, and while most of the projects I work on
are not on Heroku, I covet the CLI-based control I have when I'm working
on something else. Especially with configuration.

```bash
heroku config
```

I want that everywhere! And with [Fabric](https://www.fabfile.org)
coupled with envdir, we can do it.

```bash
fab production config
fab staging config.set:DEBUG=False
```

The solution below, which would be the contents of `fabfile/config.py`
in a project fabfile module, makes great use of envdir's simple storage
layout to read and update configuration values. A sister module,
`services` includes some simple tasks to manage application services and
here you assume that `services.restart` causes any affected services to
reload the configuration.

```python
from fabric.api import task, run
from fabric.context_managers import cd, hide
from fabric.state import env

from fabfile import services


@task(default=True)
def list():
    """Lists the environment variables for the app user"""
    with hide('running', 'stdout'):
        with cd(env.config_dir):
            environment = {
                var: run("cat {}".format(var))
                for var in run("ls").split()
            }

    longest_key = max([len(i) for i in environment.keys()]) + 1
    padding = 30 if longest_key < 30 else longest_key
    print_str = "{{:<{}}} {{}}".format(padding)
    for var in sorted(environment.keys()):
        print(print_str.format(var, environment[var]))


@task
def set(**kwargs):
    """Add one or more shell variables to the app environment"""
    with hide('running', 'stdout'):
        with cd(env.config_dir):
            for var, value in kwargs.items():
                run("echo '{0}' > {1}".format(value, var))
    services.restart()


@task
def remove(*args):
    """Remove configuration variables from the app environment"""
    success = 0
    with hide('running', 'stdout'):
        with cd(env.config_dir):
            envvars = [var for var in run("ls").split()]
            for env_key in args:
                if env_key not in envvars:
                    print("No such variable {0}".format(env_key))
                    continue
                run("rm {0}".format(env_key))
                success += 1
    if success:
        services.restart()
```

### Constraints and alternatives

If you have multiple servers, you're going to have keep multiple copies
of the configuration set. Fabric will run against multiple machines of
course, but the script here may be insufficient for doing just that. For
instance you'd probably want to know if a value was not set on one
server or failed to remove on another, etc.

Some of you reading this may be nodding and thinking, ah, "If only he
knew about `etcd` or `consul`!" I do, and while they look like really
fine tools, they're really geared toward *cloud* deployments. Not
just deployments on cloud servers, but large multi-server deployments in
which new nodes are created and destroyed like our hopes and dreams.
With one or two servers it'd still be useful but it'd also be
yet-another-service. Let's keep it simple for the simple cases.
