# Packaging

You've probably installed Python libraries before using `pip` like so:

    pip install Django==1.9.3

And then like magic you could start using Django scripts and importing
Django code into your own project.

But how did that command get Django installed? We're not going to do a
deep dive on packaging here because it's a lengthy subject, but we are
going to explore enough so that you understand how to take your app and
make it installable and usable by other users.

## The basics: setup.py

The basics of a Python package include a (1) Python module and (2) a
setup file that identifies your package and locates the code.

At a bare minimum you'll need a `setup.py` file that tells the package
manager infomration about your Python package such as it's name, the
version, and what source code to include when installing.

{title="app.py module", linenos=off, lang="python"}
    def hello_world():
        print("Hello!")
        return {}

{title="setup.py", linenos=off, lang="python"}
    from distutils.core import setup

    setup(
        author="Me",
        name="hello",
        version="1.0",
        packages=['app'],
    )

Okay, it's a silly module. But it's an installable silly module. The
first part should be self explanatory. It's a Python module. The
setup.py does one very important thing, it calls `setup` from distutils
whcih is Python's way of declaring this a module. This file is what you
will use when intsalling a package, either directly or indirectly.
Without getting into the details of all of the possible arguments you
can see that we're providing meta information, e.g. who wrote it, the
name of the package, and where to find the packages.

This file provides data at the installation level so that when you run
`python setup.py install` Python knows what to get out to install on
your Python path.

-  where the package itself is, i.e. the source of the Python modules
-  where tests are
-  what else is required for the package to install and/or test
-  descriptive information about the app itself

It also provides useufl data for package indexes, like PyPI (nee
Cheeseshop). Additional argumetns like `license` make it easy for people
to search for modules by how the software is licences, and `classifiers`
provies useful information for searching for software by targeted
purpose, environment, and Python version.

### Version

The version is critical. It needs to be a string, and you can
hard code it here, but that turns out to be a pain in the tuchus. Look,
you probably declare the version elsewhere, so declare it one place and
be done with it. That one place should be in the package root itself,
either in ``mypackage.py`` or ``mypackage/__init__.py``. The canonoical
way of definit it is with the variable name ``__version__``.

To get this into your package's setup.py file, either import or, if that
causes problems, read it from the file directly as text.

### Classifiers

The most important thing you'll use classifiers for is specifying which
Python versions your code works with.

Classifiers won't create hard constraints on how your package can be
installed - at least using typical tools - but they do provide strucuted
information in the package index that allow people to find useful
software and identify if itwill work for them.

As we're still in the transition phase between Python 2 and Python 3,
including the Pyton version classifier is one of the most important you
can fill out. Beyond that you can include other classifiers such as the
stability of your package (e.g. is it alpha? stable?).

## Everything else

Your Python package will need to include more than just your code and a
setup.py file. Here's a short overview of what else should be included.

### README

Hopefully this one is obvious. But what should this include? At a minimum
it's helpful to include a brief description of the project, author
identification with contact info, and initial installation,
configuration, and usage instructions. It needn't cover everything.

Thanks to the GitHubification of open source software, README files are
read just as much as web pages as they are in text editors, and so the
content has changed. They can include project diagrams, logos, dynamic
images for build progress, in short they often serve as much a purpose
as marketing material as they do mini-documentation.

If you're keen on promoting your app then you'll probably want to delve
into all of that, but consider that a well written README, written for
the developer trying to understand the code in front of them, will
typically server as decent marketing, whereas great marketing READMEs
dont' necessarily work for the developer's aid.

Your README can be in text format, but if you're going to put your
package on PyPI you should use reStructuredText.

### License

More on this later, but you should include a file explaining ownerhip of
your code and how it's licensed for end users. More on this in another
chapter.

### Requirements

You probably know what this is already, but it's common to see project
requirements, dependencies, included in a pip requirements file. This
may be joined by additional files like a requirements-test.txt file
specifying dependencies used solely for testing.

If the former is present by itself it's frequently read from to populate
the setup.py file in an effort to break out more of the information.

A separate testing requirements file is very helpful and these
dependencies are *not* required and needn't be installed in the deployed
environment and in many cases testing requires a few additional
packages.

### Manifest.in

One thing the setup.py file doesn't include is project assets. There's a
package specification and a test packages spec, but it may come as a
surpise that this only includes Python files. If you're writing a number
crunching library this might of no import to you (rimshot) but if you've
got templates or images, you're at risk of losing those.

What's this manifest business? We need to tell setup.py what to include
in the package. By default it will include Python files, but often we
want to include other files, like a README or assets like HTML and CSS
files. These we specify in the MANIFEST.in file.

{title="MANIFEST.in", linenos=off}
    include setup.py
    include README.rst
    include MANIFEST.in
    include LICENSE
    recursive-include myapp/templates *

### setup.cfg

What's this setup.cfg file? That's a configuration file that we're using
here for creating a ``wheel`` file. A wheel is a way of packaging Python
programs that replaces the previous style, called an 'egg'. I kind of
prefer the term 'egg', it fits more with the Python namespace, if you
will, although Larch might have been even better. Wheel can be
configured in several ways and we want to just make universal wheels.

{title="setup.cfg", linenos=off}
    [bdist_wheel]
    universal = 1

There are other uses for this file that go beyond the scope of what
we're discussing here.

### tox.ini

This is easily my favorite of these files (yes, I have a favorite, and
no I don't get out much). We'll go into greater depth about how this
file is used in the advanced section on testing, but is short it's a
configuraiton file used primarily but exclusively by tox, a tool for
managing test environments. It's worth mentioning here because you'll
likely see this in many Python packages.

### Changelog

Somteims named HISTORY, this file should be used to catalog what changed in
the package from version to version. When properly updated this tells
your users when you introduced a backwards incompatible change (and why)
explaining the justification for a new release.

There's a chapter on releases, but suffice to say there's a lot of value
in keeping this kind of thing uptodate even for small projects that the
public will never see.
