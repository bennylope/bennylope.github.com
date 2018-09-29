# Apps from a template

The hard parts of creating a good standalone app have to do with
decisions, like structure and dependencies. Yet what frustrates many
developers more is the administrata and boilerplate that goes into
setting a new package up. We'll get into how to deal with repeated
issues later in scripting and automation, but here let's look at the
latter. Just like you pick a framework to make a lot of decisions for
you, a template serves the same purpose, setting down the foundation and
letting you add in the important bits.

## Django's own app template

Django actually ships with its own template, which you can access from the `startapp` command.

```bash
django-admin.py startapp deathstar
```

It will create an empty app called "deathstar" with scaffolding
including a models.py and a tests.py file. This is useful as included
within a Django project, but not so much when creating a standalone app.
This is the stuff you probably already have and what we need to do is
create the container for it too. You can specify an app template but
this will spit out the same thing everytime.

## Using a cookiecutter

A better solution is a package templating tool, like `cookiecutter`.
Created by Audrey Roy Greenfeld, cookiecutter is written in Python but
lets you create projects in any language based on predefined templates
that you can either create from scratch or use reused from shared
templates. The upshot is that these templates can include everythign you
need and the right structure, from package directories to test
directories, license to readme.

Quick usage overview:

A good starting template is cookiecutter-djangopackage, a cookiecutter
that Daniel Greenfeld originally shared several years ago. At the time
of writing it includes a spare app module, static files and template
directory structure, and pretty much every file you might need to set up
a package. Even if it doesn't fit your needs as is, it's a good place to
start. You can fork and edit as you see fit - want to import the version
a different way, include a different testing framework by default? These
are all the kind of things that you should include in your template.

It's probably a good idea to wait on polishing your own template utnil
you need to start using it some more. There's little benefit to
polishing a tool that you're not going to use again, utnil you need to
use it again.

It's important to make the distinction here between the concept of app
templates and the particular ones available. What's important is the
former, the idea of creating an app template so that when you need to
create 

### App templates

Other app templates.

djangopackage-cookiecutter
