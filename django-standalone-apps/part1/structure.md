# The structure of an app

.. todo:: include a few layouts


## Key criteria

A Django app shares the same structure as any Python module, with a very
very specific requirements depending on what features you include with
your app.

The most obvious is including data models, and for this you'll need a
`models.py` file. Historically including the `models.py` file, empty or
not, was sufficient to make an app installable, however with the advent
of AppConfig this is no longer necessary.

The first you *should* include though is an `apps.py` file with some
basic AppConfig configuration. This allows your app to be installed
wihtout a models file and it allows your end users to change
configuration for using your app as necessary (e.g. changing the name in
the admin). Note that the apps.py file is not strictly required, and
that including a `models.py` file in sufficient to make your app
installable. However adding an APpConfig is best practice as it allows
end users to make modifications and, in the event that you do not have
any models, it provides a much clearer foundation without a superfluous
and empty module file.

You can use any Python code in your Django project from another PYthon
librayr without that library being an installable Django app. SO its
worth looking at some of the things that require having a Django app
structure to use:

- templates
- templatetags
- static files
- management commands
- models (and admin)

Of course there may be ways to make use of some of these features, like
templates, without an app by means of extensive configuration, but
that's hardly a superior options.


## Example app: currency

We'll start with a very basic example app. This is an app to make working with
currencies easier. At their base currencies values are just numeric values,
specifically decimal values, that refer to an amount in a specific denomination, and
often at a specific point in time. $10 in US dollars is not the same as €10,
and $10 USD in 2015 dollars is not the same as $10 USD in 1990 dollars.

What we want to do is make it easier to toggle the display of currency amounts
and easily format them. To start with, we just want to change the formatting of
certain of numbers, so we're just adding a couple of template filters.

The question in front of us is whether this is necessarily a Django app? As we
build this out more and more of it may be more generalizablely *not* Django
specific, but if we're going to add template tags they necessarily must be part of a Django app. Otherwise
we can't load the tags library. So this will be a Django app.

I'm going to start out the app, called `currency`, with just the necessary files at first. The
file structure will look like this::

    currency
    |── __init__.py
    |── apps.py
    |── templatetags
    │   |── __init__.py
    │   |── currency_tags.py
    |── tests.py

The `currency` folder including an `__init__.py` file makes a module. Our core
functionality is just template tags and filters for now, so we just have a `templatetags` module,
again with the `__init__.py` file and then the tag library name.

> Pedant's note: you can create a module without recourse to
> `__init__.py`, but that makes a namespace module, and is only
> available in Python 3, an assumption this book does make for the
> reader.

There's one tests.py file for our tests and then an `apps.py` file. In order to
satisfy the requirements of a Django app, our package must define a models.py file
or an app.py file, ideally including the latter even with a models.py. This allows
us to define things about our app and ensure that it's picked up by Django as
an app.

So now let's look at the content. Our `__init__.py` files are empty (for now).

Here's our apps.py file.

.. code:: python

    from django.apps import AppConfig

    class CurrencyConfig(AppConfig):
        name = 'currency'
        verbose_name = "Currency"

Heres our tags library:

.. code:: python

    from django import template

    register = template.Library()


    @register.filter
    def accounting(value):
        return "({0})".format(value) if value < 0 else "{0}".format(value)


And here's our tests.py file.

.. code:: python

    import unittest
    from currency.templatetags.currency_tags import accounting


    class FilterTests(unittest.TestCase):

        def test_positive_value(self):
            self.assertEqual("10", accounting(10))

        def test_zero_value(self):
            self.assertEqual("0", accounting(0))

        def test_negative_value(self):
            self.assertEqual("(10)", accounting(-10))


## A basic setup.py file

In order to package this we need a way of defining the package: what is it
called, what version is it, where is the code.

If you're familiar with Ruby gemspec or Node package files, the setup.py file
serves a similar purpose. And it's just Python. Let's look at the file.

.. code:: python

    from setuptools import setup

    setup(
        name="currency",
        version="0.0.1",
        packages=["currency"],
        test_suite="currency.tests",
    )

This is about as basic and stripped down as we can get. This isn't enough to
release our package, but it's enough to install it and run tests. We've got a name,
version, packages, and test suite defined.

The version is important because this is how we determine what to install when something
changes, and it's used for tracking dependencies by other apps as well.
