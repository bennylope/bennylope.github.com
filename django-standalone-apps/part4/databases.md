# Databases: getting specific

The great thing about using an object-relational mapping like Django's
ORM is that it abstracts not just boilerplate SQL but also differences
in database specifics. Do MySQL and PostgreSQL differ in table creation?
What about extracting dates in either SQLite or Oracle? Okay, I've never
used Django with Oracle, but I presume enough people do since the
backend is there.

These are, by and large, things we don't have to worry about when using
Django. The ORM's database-specific backends handle all the little
differences between each database. The same is true when creating
standalone apps, because even if I'm developing on and targeting
PostgreSQL in my projects, someone else can take my app with model,
manager, and queryset definitions and use it in their project on MySQL.

This breaks down when you start getting into raw SQL or
database-specific features.

### Raw SQL

I confess that I'm not, at least, anti-SQL at least when used sparingly
and well-documented in an individual project. By and large you should
think about keeping it out of a distributed standalone application.

If there's a performance benefit you might consider providing a second
ORM-backed way of accomplishing the task, even if it's significantly
slower.

### Database-specific features

Here's where things get tricky. Outside of raw SQL, there are two ways
of introducing database-specific features into your app:

1. third-party libraries
2. Django's `contrib.postgres` library

TODO

### Land of NoSQL

What about Mongo? Is Mongo only pawn in game of life?

The Django ORM is a *relational* mapping, it's geared toward relational
databases that speak SQL. While that may change in the future, for now
that's the reality of Django.

You can use non-relational database backends, but it requires that you
use a fork of Django. This is how you'd use Google App Engine or Django
with Mongo DB.

https://potatolondon.github.io/djangae/

What does this have to do with you as an author of a standalone
application? At some point you might have to decide whether to support,
or to allow for supporting, such backends. Quite obviously is your app
doesn't have any models then this is unlikely to be an issue. But if you
start adding models and especially relationships then you start entering
the territory where you are making decisions that may obviate NoSQL
databases.

An example of this is using ManyToManyField, which, for instance,
django-nonrel does not support.

Let's be frank though, the likelihood that this is going to be an issue
or that your model architecture uses some fields in a sufficiently
arbitrary way such that removing them for another backend has no impact
on your app is pretty low.
