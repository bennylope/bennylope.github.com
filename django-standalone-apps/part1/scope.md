# Defining the scope

There's a line you're going to draw whether you deliberately choose to
or not. You probably drew it when you extracted this from another app into
its own, or created it to fill a gap in one of your projects.

## With or without Django?

Occassinoally otherwise helpful functionality is packaged as "Django
Such and Such" for use in Django projects, but without having any
necessary dependence on Django. This probably sounds untroubling, and
indeed there's nothing awful about this, however the first scoping
question you need to ask when creating a standalone app is "Does this
require Django?".

Why ensure this separation? Well for starters, if you're going to be
sharing this with the rest of the world, and the core functionality
doesn't actually depend on Django, then you've broadened the audience.

You're also reducing yet another dependency in your package, which, even
if you're using it in Django projects, is another line of dependencies
that can break. Where it makes sense, reference the standard library
instead of Django utilities. If something moves in a new Django version,
you're now insulated from that change.

It's worth keeping in mind that you can add functionality to Django projects
without Django-specific modules, or without necessarily requiring Django.

And lastly, it's often easier to test.

In Chapter 17 on mixed dependency support we'll examine how to separate
out what's Django specific vs. what's not.

## Choosing your dependencies

The great thing about packages like the one you're creating is that they
give you funcitonality for free - maybe not free, but without the cost
of writing the code and figuring out the edge cases yourself.

These benefits presume that the dependencies you're using are adequately
tested and work as advertised.

Each dependency you add increases the surface area that you
need to test as well opportunties for broken interactions. This is true
in a Django project (site) and its equally true in your own standalone
app.

Now, it's certainly unwise to rewrite everything yourself! But give
thought to whether you really need to use a certain dependency or class
it provides.

Among the guiding questions you should ask:

1. Does the dependency provide *required* functionality for your app?
2. Is it up to date with the Django version(s) you will be supporting?
3. Does it have tests that cover its core functionality?
4. Does it have documentation? This could be complete documentation on
   Read the Docs or even a fully fleshed out README, depending on the
   scope of the app.

A>  This is a "mistake" I've made. An example of this in my own case is a
A>  decision to use the otherwise fantastic
A>  django-extensions app as a dependency for my own, django-organizations.
A>  I wanted a timestamped models - a good thing to have which you'll notice
A>  when its missing - and moreover I wanted slug fields that took care
A>  of themselves. For this I wanted the AutoslugField. This wasn't a bad
A>  decision so much as a restrictive one. I could've just used a typical
A>  Django slug field but for my own needs the Autoslug was where it was at.
A>  Later I realized that some people, including myself, might need to be able
A>  to configure how slugs are made, and this shouldnt' be so fixed.

## Getting specific

Does your app 

The more
narrowly specific your app is the more is the more rigid it is and the
fewer use cases it can handle.

Note that this is not a call to make your app radically generalized and
take into account every edge case. However it's worth considering
whether certain features or dependencies are really *necessary* for
inclusion.

## Django version support

.. todo:: move much of this to a later section

The last scoping consideration we'll mention here is the range of Django
versions that you intend to support.

For a new app it's safe to specify the latest major version and
then, dependent on testing against different environments (see the
section on testing multiple v$ersion). If going back to a certain
version requires tortuous changes due to backwards compatability issues,
that's a sign to stop.


Be conservative with what you'll require, and liberal with what you'll
allow.


The error of not specifying any level of version for your
project's dependencies is that it may encounter dependency versions that
are too old to work properly with your app, or that are newer such that
they break API compatability. On the other hand, you can easily
overspecify the versions. Aside from restricting what other people need
to use, this runs the risk of modifying dependencies they have set for
their own reasons.

![Mismatched dependency versions](images/dependency-mismatch.png)

It can make testing that much harder if you have lots of dependencies
which can break themselves or create breaking probelems on their upgrade
- especially if your app requires a version window that is suddenly
behind the major published version. If that becomes the case it may be
worthwhile to vendor the dependency, creating a specific copy that is
bundled with your app. But that's not something you should be worrying
about right now.

## Example project

Our example project is an international ecommerce site, and we have to do
a lot of things with different currencies. In fact, we know we've got another
project in the planning stages that's going to need to use much of the same
functionality. This would be a good time to start pulling this stuff out.

It allows us to print Decimals as currency by default for easy formatting,
without obscuring the underlying numeral value.
