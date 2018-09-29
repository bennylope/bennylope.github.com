# Separating functionality from another app

The goal in this section is to extract functionality from one or more
apps, either removing a monolith or consolidating from across apps, and
put this into a distinct and project-agnostic app in your project. By
project agnostic what we mean is that the app knows nothing about the
specifics of your app.

For example, this might mean extracting subscription plan information
out so that it is compltely separate from the product aspects of your
project if it is a SaaS app, or perhaps extracting workflow components
out of a larger app.

So at this point you should have identified at least a *target*
hierarchy. It might take some work and some time to get the apps to the
final point, but that's okay.

--~-~-~-~-~-~~-~
Diagram of architecture here. We want to show that you're pull
foundational apps or perhaps from above, what this is depending on.
--~-~-~-~-~-~~-~

It is imortant to note that the end goal of the work outlines in this
section is not a ready-to-go standalone app. Rather, it is the
foudnation of your standalone app, an isolated local app.

## Naming

Bad or overly specific naming can occlude where the lines are between the functionality in your app.
Do the names describe what each thing is or does? Do they do so in a very narrow
or project specific way?

While not inherently wrong its hard to see that something could potentially
be generic or used in multiple places if you only think of it as
specific to this one use case because that's how it's named.

## Refactoring first

Extracting the app is itself largely an exercise in refactoring. However
that part will largely be based on changing the module level namespace
of classes and functions.

If your code looks confusing then refactoring the code where it is, for
example breaking out functionality into additional methods or renaming
methods and functions, or even cleaning up formatting and imports, is
something you should do first. Not only will you have *two* clean
apps when you're done, but it will make the job of identifying and
moving things easier.

It will also spare you the temptation of refactoring too much as you
extract.

## Setting up the new app

## Testing, testing, testing


## Moving components out

The very first step you'll need to take if you haven't yet is to create
the new app. At first this will be nothing more than scaffolding, just
an empty Django app.

    /__init__.py
    /apps.py

What you move first will depend in part on how you're using the app as
well as how many steps you want to take while doing this. **You do not
need to make this move in a single step!**. In fact in most cases, I
if the app is already deployed to production I would want to make the
changes in discrete steps that can be deployed one by one.

Let's examine an app where the functionality is pretty well spread out.
There are models, views, forms, template tags, middleware, tasks,
templates, you name it.

Here's an idea - start with tests! If you don't have tests covering what
you're moving then you'll definitely want to add them. For example, if
you're moving URL configuration, hold off on changing URL names and add
tests that the URLs are configured (SHOW EXAMPLE). Add these tests to
the new app, running against the configuration with the URLs in the old
app. Then move the URL configuration, and keep testing.

    /__init__.py
    /apps.py
    /tests/
        /__init__.py
        /test_urls.py

(This is an example set up. Your URL tests, if you have any on their
own, will probably be quite small and don't require their own test
module.)

A> Good tools can help this process along. I use vim quite a bit, and if
A> you're a vim user then you should take a look at vim-rope, a tool for
A> refactoring in Python. That said, for refactoring work especially I tend
A> to rely on the PyCharm IDE. It's not foolproof, but it easier to make
A> these changes and to do so reliably.

So what's easiest to move? Functionality like middleware
and context processors are usually low hanging fruit. Especially if
you're not changing any *internal* names, just the namespace.

    /__init__.py
    /apps.py
    /templatetags/
        /__init__.py
        /app_tags.py
    /tests/
        /__init__.py
        /test_urls.py

A> While refactoring like this it may be tempting to rename components.
A> This is an improvement, but especially if your test coverage is low you
A> should hold off on making these small improvements in favor of making
A> one change at a time and keeping the sequnece of changes consistent.
A> The first reason is that it makes understanding the history in your
A> source control much simpler. Seeing the changes in steps like that,
A> moving from a module and refactored in separate diffs, makes it easier
A> to understand what changed, when, and how when reviewing source history.
A> It also makes understanding the changes when you're making them easier.
A> There are fewer mental diffs to keep track of.

If you're moving template tag you'll want to ensure you have tests that
load the templates in which your tags and filters are used. Thoses tests
belong associated with whatever app loads those templates.

You can extract the URL routes from your old app and put them into the
new app and maintain the old imports from the original app. Once the
URLs are configured you can then move the views.

### Viscious Import Circles

Another thing you'll need to mind extracting functionality is dependence
circularity. In the ideal set up you'll create new, isolated app "X"
which knows nothing about app "Y", and app "Y" imports from app "X" but
not vice versa. While extracting from X into Y you may end up with
imports from each app respectively.

What you need to avoid is the case where imports occur from individula
modules. That will create a circular depdnence issue.

The first step in doing this is extracting out top level things first.
This is one reason why an order like URLs, views, forms, models, tends
to work, as this is fairly typical dependence order, as far as imports
go.

If you're making this change in steps, you might find a stopgap solution
in local imports.

    def some_function():
        from my_new_app.models import Blah

These are ugly and not exactly best practice, but they can be useful in
a case like this.

### Extracting tight coupling

For overly tightly coupled code there is no easy answer. The st

Tight coupling and monolithic apps are common as projects grow in
response to customer and business needs, changing requirements and
changing teams.

## Moving models

Models are typically the last thing to move. It can seem like a big
deal, too, if you've tried it unsuccessfully before. Do it wrong and you
lose database tables. That doesn't make Jack a happy boy.

Again, decent test goverage and good tools will help you quite a bit
here, although alone those will not do the work for you.

The first step in moving the models is to move managers and queryset
classes. When you move the model classes they should be the last parts
of the new app to be moved out - everything else they require should be,
to the greatest degree possible, importable from the new app. Again the
importance of this is greater if you're making the changes and deploying
in piecemeal.

What you do for the second step depends on how aggressively you want to
make the leap to a standalone app. At a base level, what you need to do
is ensure that your models define their database table names explicitly,
so that the database need not change when classes do. This involves
adding the `Meta` class attribute like so:

    class Meta:
        db_tablename = "oldapp_modelname"

Check the database to ensure you get the table name right. Then create a
migration which will alter the tablename - in practice a non-event.

A> Alternatively you could name the tables based on your new app's name
A> so that this operation involves simply renaming the tables. Just
A> ensure that the steps are done in a strict sequence: name table,
A> genreate migration, then move (below).

The third step, is to just move the classes. That's it! For the second
step at least. At this point you should at least have no linting errors.

Of course, there's a step 3.5, which is creating the datatabase
migration in both the old app and the new app.

After creating the new migration files take a look at them and examine
what they'll do. Django's migration package interprets this move as
field deletion and table creation, which is not what we want to happen.
So you'll need to edit each migration and override the `apply` and
`unapply` methods so that depsite what the migration declares, it
doesn't actually make any database changes.

## Removing from the project

Once the code has been extracted you can move it out of the project.
There's no need to race off and publish to the Python Package Index
just yet.

From here you can include the code in your project as a submodule, using
Git, or set up the basics of an installable package and include the
requirement from a remote source repository. This allows you to start
using a single codebase in multiple projects.
