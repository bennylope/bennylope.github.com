# Model migrations

Database schema migrations are a way of tracking and automatically
making changes to the database *schema* to match changes in app
models, such as adding new models, new fields, or changing field
parameters.

It's important to keep these updated in your standalone app. Prior to
Django 1.7 the accepted way of doing this was by using a third party
standalone app called South. Without South installed a user could
install an app and set up the database tables using Django's `syncdb`
command but would have no control over later changes to the database.

You're probably already familiar with model migrations but in the
context of your own project.

Django 1.7 introduced native database migrations, obviating the need for
a third-party tool like South and at the same time making database
schema or migration files a core part of Django apps.

## Using a sample project

In your existing Django projects you can easily make a change to a model
and then run the `makemigrations` to automatically generate a schema
migration file.

    python manage.py makemigrations myapp

With a standalone app we're in a similar position as we were with
testing: finding a project substitute. As with testing, we'll need to
substitute a way of using these commands.

The first way to do this is to add a stripped down
example project to your app's package folder from which you can include
your app and build migrations. This is far superior since there's no
copying and pasting like a dummy.

You do this by starting a project, called "example" right in the root of
your package directory. You can strip down the settings file to just the
bare minimum, including the `INSTALLED_APPS`.

This turns out to be something of a pain in the tucchus too.

A> The first way of going about this is including and installing the app in
A> another project somewhere, creating the migrations, and copying them
A> over to your app. I'm not telling you this because you should do it.
A> Don't do this. But I have, and if you have, then you're not alone. If
A> you haven't, good for you.
A>
A> A significant downside to this method, aside from being boneheaded and
A> requiring lots of extra work that's not repeatable by anyone else, is
A> that it requires you to ensure you're always running the other project
A> on the same Python PATH (i.e. virtualenv).

## Using a helper script

A yet better way of doing this is inspired by the runtests.py test
script so beloved in standalone apps. We create a single script in the
root of the project - I'll call it manage.py here since its going to
function in the same way - and before running the command it will
configure Django's settings. Now we can run Django commands like
makemigrations right from the package root.

<<[App management script](code/manage.py)

A> This is part of release management (chapter X), but aim to include only the
A> migrations necessary for each change. For your first app, this would
A> ideally be one initial migration. There shouldn't be a need for anyone
A> to create the table initially and then make successive changes, if it's
A> never been out in the wild before. Obvious exceptions to this are if
A> you're already making extensive use of this app and it's got to be drop
A> in into your own projects.

For your first release, we'll just make an initial migration and call it
a day.

    python manage.py makemigrations myapp


