# South migrations

It is possible, however unlikely, that you may want to support older,
outdated version sof Django. This is the only reason why you'd need to
with this section. Much of my own struggles with migrations in
standalone apps came from pre-Django migrations, so for the one or two
of you supporting ancient Django versions, this is for you.


## Swappable fields with South

In most respects the Django migrations module is more advanced than its
predecssor, South. However there are some things that South actually
made *easier* because it wasn't aware of them. Effectively, South
monitored changes to the database - tables and columns - and ignored any
other changes to fields or models that wouldn't result in a change to
the underlying schema. The upshot is that once you've created a schema
migration file with South, you can edit the file to suit other purposes.
If you try the same thing with Django's migrations, you'll just end up
with another migration file, regardless of whether there was a change to
the database, as Django's migration module seeks to represent fully
what's represetned by the model classes.

So, the topic is migrations. Django Model Migrations with swappable fields when
you’re using south. The kinds of swappable field as an authoritative concept is
fairly new to Django-1.7, which is a non-south compatible version of Django,
but such a thing existed prior to this with the introduction of custom user
models in Django-1.5. And to be fair, you could introduce custom user models
prior to Django-1.5, they just didn’t take the place of off.user and it becomes
a little trickier later.

So, let’s examine what you need to do. We’ve already walked through how to make
these migrations with Django’s migrations module. The Django migrations module
takes care of the swappable migration for you. If you look at the migration
file, you’ll notice that right here we have this end of the field and it’s
calling this setting here the swappable model. So, it’s going to pull this from
the Django project. It doesn’t matter where this is installed, it’s going to
pull this data in. So it could be off.user, mycooloff.mycooluser or any other
kind of model. And this is true for other swappable models, as well.

South doesn’t do this. So let’s go ahead and look at a south migration. In this
project, we’re using Django’s contrib.off and we declared it. We make a south
migration. This is going to go in our app, by the way, so we’re packaging this.
What do we see? It’s making this link to contrib.off. That’s not what we want.
We actually want to see something more flexible. So if we go ahead and change
this in our project to myprofileapp.mycooluser and we run a migration, make the
?? migration, we see that all of the sudden that is in there, too. This
works if it’s our own project. We want to link to our own models, but if we are
distributing this or want to make it flexible, that’s not going to work. So how
do we address this?

We could do it through some sort of really painful method, but in terms it
doesn’t take much effort to do this. We just have to edit the file directly and
that is not horribly complicated. So what we’re going to do is go ahead and
look here, we’ll edit these files. We’re going to look for all of the places
where we found the hard coded model and we’re going to remove that. These are
strings and it’s going to replace it with the path to our model. In this
instance here, where we see a dotted path in the model, we want to have the
dotted path for the optional model and the same thing here in each and every
other place. I said it’s not that much effort, but it is going to take a little
bit of effort. It’s mainly you just have to be careful and look for this. So,
we’ll go through and we can now edit our model here and we see if that is
working.

How do we test this? The best way is to have two test projects or two test apps
and to test that each one works. One will use contrib.off and one will use
something else and just verify that they work. One issue is that you’ll have to
do this, or you should probably do this, each time you go through and make a
schema change, especially of course if you’re touching this field. You’ll have
to do if you’re touching this field. It’s probably a good idea to do it
elsewhere so that south can look at this and its introspection here will
understand that you haven’t changed something and won’t try to make any
changes. It’s going to know what is there. The main thing to do is to make the
changes in the south schema operations area.

This is a note more for the beginning, but it’s a question, why are we
bothering? Django-1.7 has been out for over a year and Django-1.4 is going to
be deprecated soon or is now deprecated. Why do we do this? The fact of the
matter is that there is still a lot of people using Django projects. The cost
of upgrading a ?? opication in nontrivial. There are often all kinds of
dependencies streamed throughout, updating your production database from south
?? migration isn’t always super easy. You might have dependencies elsewhere,
you’ll have to run through all the migrations and do all this stuff and this is
of course, taking time out of working on an app that is likely running a part
of a business. This is why I’m including it. This is not to say that you have
to do this, I don’t think anyone has expectation that this new app is going to
support Django-1.3 or even Django-1.4 soon. Here at least we have this option
of doing that.

For apps that I have, Django organizations that I’ve published before, I kind
of aim to have some sort of support there for that. I don’t really want to
focus too strongly on it, but you know, I have apps, I know that pain. I don’t
want to, in my own app, I don’t see the need to so quickly deprecate this. That
is of course an individual policy. I think it’s totally fair to simply support
the Django versions that supported themselves, but again, I would argue it’d be
better to be aggressive in supporting ?? versions, be very liberal with
that, and be conservative with deprecating older versions.
