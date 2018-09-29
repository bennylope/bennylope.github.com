# Migrations: some strategies

In part 1 we covered how to set up your project so that you can create database
migration files and how to handle some of the edge or not so edge cases in
which you might find yourself.

The picture gets a *little* bit more complicated when we get into new releases. At this point we've
already got a release out in the wild, and we want to release an updated version. In the new version
you might want to do something like add a field or change the structure of a field.

## Amend charitably

Beware doing things like making field lengths *shorter*. Your changes shouldn't be destructive,
and if they are, there should be strong warnings and/or a way to safely keep or test for truncated data.

## Data and muultistep migrations

Adding a non-nullable field on a large table can take a lot of time. So it's
better to add the field allowing null values, then add the default data in,
and *then* clean up by making it nullable again.

.. todo:: find original advice about this

.. todo:: test speed of migration with a large table using a default value vs. nullable

.. todo:: mention differences in how databases handle schema changes.

## Minimize the steps

As you're working through a feature you may find yourself changing the schema and rechanging
it, deciding that a field should work one way and then maybe a different way. 

## Database specific features

Do you want to use Hstore or JSON fields? Do you wnat to add them into your app?

.. todo:: verify version in which hstore came out

There have been third-party libraries for a while supporting database specific field types,
e.g. the hstore field that shipped with PostgreSQL version 9.0. Django 1.8 shipped with
a new contrib module, `contrib.postgres` that includes some PostgreSQL specific fields
and other goodies. You should at least give some thought to how to use these in your app
first before diving in, especially if one of your goals is for other peoole's use.

Believe it or not, not everyone uses the same database you use, and in fact some
people can't.

.. todo:: check what databases support GeoDJango

If your app uses GeoDjango, it doesn't make much sense to fret too much about database
specific functionality. Most of that comes through PostGIS and most GeoDjango users
seem to be using PostgreSQL (some more limited GeoDjango functionality is available
through MySQL and Sqlite).

When all is said and done it's your app of course.

## Swappable fields

Swappable fields are swappable foreign keys.

This is a topic of special interest to me and also of some annoyance.
Let's say our app has a model with a foreign key to the User. That's
simple enough. We'd add a foreign key like this:

{title="Model with specific model relation", linenos=off, lang="python"}
    class MyModel(models.Model):
        user = models.ForeignKey(User)

Ah! But that's obviously not what we want. We know that since good ol'
Django 1.5 we've been able to add custom users. Which means that our
users might not be using the User model for their users themselves
(that's a mouthful). Instead we need to replace the "User" instance in
the ForeignKey argument with the get\_user\_model function so that the
the configured model is used.

{title="Model with configurable model relation", linenos=off, lang="python"}
    class MyModel(models.Model):
        user = models.ForeignKey(get_user_model())

Oila! But there's still one small problem. Can you see it? No? Okay, run
the migration command.::

    python manage.py makemigrations myapp

And then check out the migration. Now do you see the problem? The
migration command doesn't know that the Class provided as an argument to
the ForeignKey field isn't supposed to be hard coded. Why is that? Well
the function returns a Class and that's what the migration machinery
uses. And since our project here has the django.contrib.auth installed
and - most importantly - has the auth.User model configured as the
project user - that's the default remember - that's what our migration
includes.

In order to change that you'll need to edit the migration file itself.

## Configurable model and field values

Django's migrations let you handle swappable values for *foreign keys*
but what about making *other* values swappable? This is more of an edge
case, but there are edge cases where you might want to make a model base
class configurable or a field class.

{title="Configurable base class", linenos=off, lang="python"}
    from app.settings import BaseMixin

    class MyModel(BaseMixin, models.Model):
        title = models.CharField(max_length=200)

Be careful what you put in your models because that's going to go into migrations.

### Configurable field classes

{title="Configurable field class", linenos=off, lang="python"}
    from app.settings import 

The 

### Callable choices

Choices? Pulled from settings? That's going in!

Call a function for a value? That'll be evaluated on every call to make new
migrations, even for other apps.

Hopefully this is an edge case.

