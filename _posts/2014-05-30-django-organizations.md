---
author: Ben
title: "Meet Django Organizations"
layout: post
comments: true
permalink: /meet-django-organizations/
redirect_from: /blog/meet-django-organizations/
canonical: http://www.wellfireinteractive.com/blog/meet-django-organizations/
teaser: >
    Useful open-source projects start by first scratching your own itch,
    then scratching it again, and yet again. One of our own itches has been
    setting up group based user systems for applications, and the way we
    scratched it was by creating Django-organizations.
---

Useful open-source projects start by first scratching your own itch,
then scratching it again, and yet again. One of our own itches has been
setting up group based user systems for applications, and the way we
scratched it was by creating Django-organizations.

### Two users, one account

The concept of associating an account of some type with a person is
pretty common. It makes sense where the account
represents an individual identity, like a Facebook account, but less so
where an account represents something like a business with multiple
people who may need access. It can be pretty awful, to say nothing of a
security risk, forcing multiple people to share an account. Just think
of the last time you had to share a username and
password with coworkers. We wrote more about this travesty a few months
back in a post about [designing multiple user
accounts](/blog/multiple-user-accounts-best-practices/).

### App architecture

Django-organizations solves this by linking individual users to the
account - the organization - separating individual identity and
authorization from a central group account.

At the heart of the application is the organization. The base
organization model is a timestamped model with an id and a name. This model
then serves as the customer or group account.

To connect users, the `OrganizationUser` model simply links your user
model back to the `Organization`. Rather than use a plain many-to-many
relationship, the organization user model serves as a custom through
model for a many-to-many relationship on the `Organization` model. This
allows for additional attributes on the through model and more
importantly a database constraint on user membership - no duplicates
allowed.

The final data component is the `OrganizationOwner` model. This model
allows one user to be identified as the prime owner of the account, and
is enforced by a one-to-one relationship against the `OrganizationUser`
model. You can never have more then one owner of an account and an
organization user can never own more than one account.

Note that this does not prevent a *user* from belonging to or owning
more than one account. It simply separates individual identity - name,
password, email, personal profile, etc - from the business account.

### Niceties: views and registration

Beyond the data models, Django-organizations provides some class based views
for accessing and editing organizations and users. These are based on some
handy mixins for restricting access to a user based on organization membership
and role.

In addition there's a pluggable backend system for handling user registration
and invitations. A registration backend allows you to hook up something like
email validation into your organization creation process, while an invitation
backend provides a way to invite and register new users to an existing
organization. The default backends will work without much work in most
cases. By design they are fairly basic, allowing room for customization.

### Design choices and the big 1.0

It's getting close to two years since its first PyPI release. In that
time we've launched it into production for several
clients, and many more people have used it on their own projects, but
it's still not at the 1.0 mark. Strictly speaking it's not even at the 0.2.0
mark, but that's due to a shortsighted view of how it'd evolve.

When I started planning on some of the changes I wanted to make for that
release I examined how our own use cases had changed. The initial code
was based largely on immediate uses cases. We wanted auto-created
account slugs and the ability to distinguish between users with admin
rights on account and those without. Since we use django-extensions
quite a bit we required django-extensions in order to get the
`AutoSlugfield`, plus the `TimeStampedModel` base model. These work
well, but this means we're requiring everyone else to install
django-extensions for these two relatively minor features.

Then there's the through model, the `OrganizationUser`. When it came
down to it, we never actually made use of that `is_admin` field on the
model. Aside from distinguishing between account owners and other users
- which turned out to be used quite a bit - it made sense to treat
everyone else largely the same. Dare we get rid of that? And if we do,
possibly to the chagrin of some people, how do we make it possible to
add some of the other features that people have requested, like account
user permissions? Just add it all and hope everyone wants it?

The `users` field on the `Organization` model is a `ManyToMany` field, a
convenience in case you want to add users via the typical M2M interface,
but is a problem for non-relational databases. django-nonrel doesn't
support this field.

And of course there's the organization model. In all but the simple
example mentioned previously we've extended this model to provide things
like business contact information, subscription information, college
admissions data, etc. And occassionally requiring multiple types of
organizations.

The downsides to the way this is handled in Django organizations now is
that it requires mulit-table inheritence and prescripted use of the slug
field. Mutliple organization types all build off a shared organization
table with incremental IDs and slugs that must be unique across *all*
organizations. In a scenario with only one type of organization the slug
must be unique against the entire set of organizations, when in some
instances it may be more useful to restrict uniqueness to a combination
of other factors or simply not at all.

In 1.0 we're going to remedy all of this.

### The release of 1.0

Here's what we're targetting for the 1.0 release:

* Default models still be timestamped, but using the TimeStamp base of
  your choice
* Default base `Organization` model will stil have a slug field, but it
  will not be required, nor will it be unique by default
* If you want, you can extend the base organization architecture without
  resorting to multi-table inheritence (which will still be supported)
* Django support for 1.4\* through 1.7
* Python support for 2.6 through 3.4 (plus PyPy... Jython?)
* Works with django-nonrel and MongoDB\*
* Documentation for new features
* Documentation for maintaining 100% backwards compatability with
  existing installations
* Cookbooks in the docs. You should know if you need to use it or not,
  but we've got some good examples to share.

The release timeframe is by end of June. As of the end of May we've pushed out
new feature versions, including the
abstract base models, Python 3.4 and Django 1.7 compatability, and
documentation cookbooks.

I'd ask readers to note the
support for Django 1.4 and django-nonrel. The former represents a
committment to support supported versions of Django. Django 1.4 is the
first long-term support release of Django and we intend to support it in
this app and all others we've release. The latter is a
good faith effort to support a user group with minimal required effort
but not a committment to support. At such time as the framework supports Django
without forking or we decide to ditch PostgreSQL for Mongo, we'll
reconsider.
