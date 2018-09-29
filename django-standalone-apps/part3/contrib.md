# Contrib libraries: Mixing dependency support

We've already covered that there's usually a line between what should be
part of a *Django* app and what might be generally applicable in a
non-Django Python package. Sometimes you want to package everything
together. Here's how to do that without forcing the kitchen sink down
everyone's throat.

## Separate packages

This one should be obvious, but the first option is to simply create
separate packages. One that includes the general functionality, and
another, the specific app functionality, which uses the former as a
dependency.

TODO: Example(s) of this

## Django applications all the way down

The alternative to this is to create submodules. Not just any
submodules, but submodules that are installable Django applications.

It will look a lot like this in your app (using AppConfig style app
definition here):

```
myapp
		myapp_specialized
				__init__.py
				apps.py
				special_hooks.py
		__init__.py
		apps.py
		models.py
		urls.py
		views.py
```

Now the project settings to use both apps will probably look like this:

```
INSTALLED_APPS = [
		'myapp',
		'myapp.myapp_specialized',
]
```

## Handling different backing services and dependencies

Two concrete examples to motivate this is providing some specialized version of some feature set for payments and CMSs.

Let's say you have a subscriptions application that allows people to manage subscriptions across accounts on their site, including an interface to the payment service and things like limited access to feature based on subscription level and status. You might make this a Stripe or PayPal based system depending on what you're currently using, or you might end 

A geographic-related application that provides support for geocoding. Here you could provide different geocoding service backends bundled with your app.


And its the same thing within the Django universe, too. You might want to have some functionality that pertains to a CMS like Django CMS or Wagtail. Except if you start adding this stuff to your app, you're introducing some unnecessary dependnecies. Do you really need every use to install all of these things? Do you want to do that?

Probably not, so this is where you can create separate sub-apps for working with specific installable instances.

my_app.cms_lib
my_app.wagtail_lib

## Non-Django support

You can invert this, too, if you have some kind of package that you can use in both Django and Flask projects, for example. In this case you'd want your core functionality in the top level, and then Django and Flask submodules.

```
super_awesome/
		django_awesome/
				__init__.py
				apps.py
				views.py
		flask_awesome/
				__init__.py
		__init__.py
		awesome.py
		core.py
```

Installing in a Django project then looks like this:

```
INSTALLED_APPS = [
		'super_awesome.django_awesome',
]
```
