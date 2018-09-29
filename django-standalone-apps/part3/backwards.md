# Maintaining version compatability

## Older Django versions

Supporting older versions of Django concurrently with advanced versions
can start to post a problem. For example, if you want to support both
Django 1.6 and Django 1.8 (or 1.9), you need to accommodate two
different ways of migrating database schemas. Not to mention changes in
the Django package API.

In order to support multiple database schema changes, you'll need to be
able to toggle settings values based on the Django version. In any
Django environment for Django 1.4, you include South as a requirement
(the precursor to django's native migrations).

Remember how we called django.setup() in our test file? Now we'll need
to make sure we don't do that.

Building schema changes works the same way, and you'll still need to be
on the lookout for swappable models for which the field change needs to
be edited by hand.

Why would you ever support older, deprecated versions of Django? Well,
if you have one or more projects stuck on an older version, then it's
probably helpful to keep your own app compatible with said older
version. And if barring great complexity or reliance on fast moving
features, if the cost of keeping it compatible with older versions is
cheap, it enables a greater number of people to use your app. Few people
start projects with older versions, at least on purpose, but a lot of
projects keep running on older versions due to the cost of upgrading.

## Backwards compatability for your app

This is something you'll need to start considering when later down the
road once you have a few releases out there. At some point you might
find that you or someone else using your app wants to make a non-trivial
change.

### Multistep migrations

### Interfaces for compatability

This is your interface design for your code. And it's good defensive
programming in general. Where you have code of your own that may change,
or code that refers to Django code that has or will change, wrap it in
another function or method so that despite what else may change, app
users (including your future self) don't have to worry about their
calling code changing.

### Compatability modules

You can handle much of the changes within your own code by pushing these
checks and imports to a distinct module which encapsulates the necessary
changes based on Django or even Python versions.

For instance, let's say your app makes use of Django's `mark_safe` for
marking HTML rendered strings as safe and not requiring escaping. This
moved in version 1.6 from XXXXX to ZZZZZ. A natural workaround for this
might be:

{linenos=off, lang="python"}
    try:
        from django.utils.text import mark_safe
    except ImportError:
        from django.html import mark_safe

Which in and of itself is fine, but after a while seeing your code
littered with try/except blocks to import a few functions gets pretty
old. A cleaner way is to push all of these conditonal imports into a
compatibility module, and import from that module in each calling
module.

{title=Compatibility module, linenos=off, lang="python"}
    from myapp.compat import mark_safe

The [django-compat](https://github.com/arteria/django-compat) library 


## Defining a cut off

At a certain point it doesn't make sense to support older versions and
it's just no longer worth it. Unless you or significant users of your
app are still on Django 1.3, the work required to maintain compatability
on Django 1.3 *and* Django 1.10 might just be too onerous.

## Known issues

Every major Django version brings backwards incompatible changes. Some
of them are 

### Migrations

If you plan on supporting anything prior to Django 1.7 you'll need to
provide support for database migrations using South.

### Custom users

If you plan on supporting anything prior to Django 1.5 you'll need to
provide compatability with regard to custom users.


