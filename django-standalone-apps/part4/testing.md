# Testing, part II: version environments and test runners

When you build and test an app in your Django project, you're testing
against the app's version of Django and Python respectively. It just
so happens that not everyone is or will be using the exact same combination
of version that you are, including it should be noted future you, who may
find yourself upgrading Django or deploying with a new Python distribution
and hoping that everything still works.

The solution is to run your tests against multiple versions of Django and
Python, respctively, from the get go. And it just so happens there's an
app for that, or at least a very helpful Python utility: tox.


Python
Django

You're probably running your project in one place, using the same Django
version and Python version. But you might want to change that, and
besides, there's no guarantee that everyone else is using the same
Python and Django version combination as you. If you're going to bother
publishing a package, you might as well test against other versions.
It's not much extra work, as you'll see shortly, and it goes a long way
to making your app useful to a broader audience. It will also make it
easier for you to update your own projects, knowing that your app runs
in several versions of Python and different versions of Django to boot.

## Multiple versions of Python

- which versions to support
- configuring tox to do this

Running tests against several versions of Python is easy enough - you
just use a different Python binary! Instead of running `python manage.py test`,
how about `python3.4 manage.py test`. That'll work just fine, provided
Django is installed in each Python path for each version of Python you
want to use. That sounds like a case for using a separate virtualenv for
each version of Python. This will look like mypackage-py27,
mypackage-py33, etc.

If that seems like it'll be a pain to manage, you're right. First off,
you have to remember each. Secondly, you're going to need to multiply
these for each different version of Django you want. And oh you'll need
to ensure you're app is installed in each one. Oy vey.

Thankfully there's a tool that does this for us, tox. It'll keep all of
the environments out of the way, manage them using a simple definition
we provide, keep them updated from our app, and even map the test suite
across all of the specified environments. Hot damn!

It starts with a tox.ini file. I happen to love the ini file format, so
this makes me happy. I don't think there's any configuration format
that's more human readable, not even YAML. The first thing that goes
into the tox.ini file is telling tox what command to run for to test.
Here I'm just going to tell it to run py.test. I'll also tell it what
dependneices it needs to install for running tests - in this case it
needs to know to install py.test before running the tests. I've included
this in a separate requrieemnts file.

Next I can define different environments. This is what we showed up for.
Here I'm listing them each out, starting with different Python versions.
I'd like to run this against Python 2.7 and Python 3.4. You can add any
Python you want though. When possible I recommend adding more, and not
just CPython versions.


## Multiple versions of Django

- which versions to support
- configuring tox
- setting up your desired matrix

As with Python itself, testing against multiple versions of Django is
the only reasonable way of ensuring that your app works with each
version of Django you want it to support. And as with Python versions,
the solution is not to manage a bunch of virtual environments for each
Django version, but to 

A> Watch out for how you specify the required Django version, if any, in
A> your `setup.py` file.

For Django I've picked a similar path, but found that a good idea is to
make your basleine the current activelys upported versions of Django.
Support older versions only if you have projects using those older
versions still. Unless someone is volunteering to do the work necessary
to keep your project in line with older versions (see Collaboration
later) then you don't owe anyone.

On the one hand it's great to support more versions, on the other make
sure that's something you want to commit to. Make ti clear what versions
your project supports. Of note here is that with tox you can test
against more combinations than specified in the default, amking it
accessible to test against other versions of Django, for example, while
only testing against the current supported versions by default.

## Yes, multiple versions of other dependencies

- this is only necessary if you're including _variable versions_ of
  other dependencies.

## Other plugins

### Coverage

Test coverage shows you how much of your code, usually by statements or
lines, are executed when you run your tests.

> Coverage is a false god. (Ben Lopatin, DjangoCon US 2016)

Okay, I'm quoting myself.

If you aspire to 100% code coverage, keep in mind that what matters is
that you achieve this *across* all Python, Django, and other dependency
combinations. If you 

    # Can't run both at the same time!
    if six.PY3:
        # Python 3 code here
    else:
        # Python 2 :( code here

100% test coverage may very well not be possible for any given combination
of Python, Django, and/or other dependencies, as you may skip code used
only conditionally 

### linting

Do you like tabs in your code? How about unused imports? I didn't think so.
One strategy you may be using already to keep code smells out, consistent
formatting, and avoid errors is code linting + static analysis.

I'd argue that this is far more important in a base project than an app,
but it's still helpful, especially when more than one contributor gets
involved. If you're not willing to state and enforce an opinion, then
don't bother.

.. todo:: why is more important in a project than an app?

## More tox configuration

When you run the command "tox" you'll notice that it runs through the
test suite for each environment, after setting up each environment. The
testing virutalenvs live in the '.tox' directory by the way, and you
should make a point of excluding this directry from source control,
globally, at the project level or both.

Side note: this is one of those cases where it makes sense to always
excldue the directoy in a global setting like ~/.gitignore\_global,
since you'll never want this. But if you're going to be expect any
collaborators, it's not a bad idea to add it to the project .gitignroe.
While there are hundreds of things more annoying that collaboraotrs
adding superfluous files to repositories, it's still pretty annoying.

Your app is installed in each tox environment, so you can simply run
'tox' to test all changes again. You can specify just one environment as
well using the -e flag, e.g. "tox -e py27". Need to change another
dependency in the environments? Use the -r flag to rebuild; this is
compatible with the -e flag in that it can be applied to all or only
specified environments.

What makes this one step better is that we can deeply specify whats in
each environment, they needn't be limited to Python versions. Here, the
environemnt listed include different versions of Django as well.

.. tox envs listed here

This is called the testing matrix. It's verbose, and tox has a way of
letting us simplify the naming and specs

.. cleaned up sample spec

How do you decide what versions to test against? Well, start with what
you're using! As a baseline I like to test against Python 2.7 and Python
3.4. Most of the client projects I come across are in Python 2.7 so I
like the packages I work with to work on Python 2.7. Then I figure that
it should run against the latest Python (although that'll be Python 3.5
soon enough). For more complete testing I'll including Python 3.3 and
PyPy versions. PyPy is a Python interpreter written using a Python
subset called RPython - Python written in Python! I've tried to set up
Jython testing as well to no avail.

TODO get Jython testing actually working in a project.

## Alternative test runners

### nose, django-nose

### pytest
