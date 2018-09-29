# Documentation

Have you ever found a package that looks like it just might work like
you need it to, and then realized that something didn't quite make sense
- and there was no documentation for how it worked? How frustrated were
you? And do you remember doing that when you were facing down a hard
deadline? Not fun.

Documentation is important for users to understand why your app exists,
what it does, and how it does it. How do they add it into their project?
What does it need them to do? Beyond that, how exactly can they hook
into their app?

Before you have a panic attack about writing lots of docs, keep in mind
that for many projects, especially smaller ones, a good README file is
sufficient.

## What should you document?

No matter how extensive your project documentation, there are a few
basic things you should include, wiehter in a full docs folder or merely
in a README.

### Purpose and goals

Even a readme file should start with a minimum of one sentence
explaining what the project is for. There is of course a marketing
benefit to this if you want other people to be able to find your
rpoject, but it's also helpful for people to understand how or wehter
this si the tool they're looking for.

Examples of projects explaining what they are:

- Django
- Sphinx
- django-organizations
- django-rest-framework

If this sounds daunting let Unix `manpages` give you an idea of how even
a short description can be helpful.

### Installation

The first thing that any and all documentation shoudl cover is
installation. This might be as minimal as `pip install my-app` but no
doubt should be left to the user.

If you're including an installed app even the step adding this to the
`INSTALLED_APPS` list should be included.

### Configuration

Beyond installation, does your app incldue any necessary additions to
the settings, such as adding middleware classes or adding optional - or
required - app specific settings, then this should be documented, too.
If URLs are required, pointing out that these should be included and any
expected namespaces is something you should document as well.

### The top level interface

Lastly in our list of prerequisitie documentation, you'll want to
include an overview of the top level interface for your app. You don't
need to explain how everything works, but you should provide a brief
expalanation and example or two about how to integrate and use your app.

If you have template tags, show a template snippet loading the template
tag library by name and showing a short example of tags and filters.

If this some kind of mixins, show a user class including the mixin and
any changes they'd include in their class's methods.

Note this is the minimum you should include in external documentation.

## Some notes on markup language

You've probably noticed that the predominate chocie of markup language
for Python projects is reStructuredText, using the rst extension. This
is a good default, even if you're used to Markdown. The basics of
restructuredtext aren't that much different than Markdown. Probably the
biggest difference is the link syntax.

This is a good default choice for external documentation, from your
README, changelog, and docs folder. For starters, its what docutils and
PyPI understand.

You may not use many of the features of restructuredtext, but as you
continue developing - and documenting -

If you really want to use Markdown you certainly can - documentation in
plain text is better than none, and Markdown is a very palatable choice.
If you choose to write documentation in Markdown, use TOm Christie's
`mkdocs` package. It'll provide a lot of the structure allowing you to
build multipage documentation that's structured and links to each other.
At the very least keep your README and anything else that you want
properly formatted on PyPI in restructuredtext. If you don't care how it
looks there, then damn the directives.

Both restructuredtext and Markdown are supported on Read the Docs, you
can just do a lot more with restructuredtext.
