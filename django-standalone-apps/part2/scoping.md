# Scoping the extraction (drawing boundaries)

Just as when you're starting from a clean slate, when you start from an
existing project, you need to define where the boundaries of your app
are. What will it do? What *won't* it do? What is core to its job and
what should be left to the developer-as-user to configure?




- Business goal (unix philosophy-ish)
- Views
- Template tags
- Middleware
- Forms
- Models
- Signals
- Tasks
- Templates
- Circular relationships in your code
- Multiple apps
- Namespacing

When you start scoping out the new app to be extracted, you need to look
at two different kinds of scope: obviously what code need to come out,
that is classes and functions, but first what job these components have.

## What does it do

Put yourself in the shoes of a marketer (no, really). How would you
describe your app? What problem does it solve? How does it solve that
problem? How does it solve this problem for many other applications?

The answers to these questions *will* be helpful in marketing your open
source package, but that's not why we're asking them.


Ie 's easier to

For each 

You m

Problems answering these questions might mean there are other problems
you need to solve first with how the codebase is designed.

## Dimenions to break up code

- Domain
- Base functionality

## How does your code use this

- Where are there dependencies? What do they look like, that is,
  directionally?
- Are they necessarily like that?
- Can dependencies (not import but directional code) be substituted
  using something like signals or dependency injection?

This is the starting point for most reusable apps. If you're on your
second use for your app, it's already in the rinse repeat cycle. 

- you may need to change the app - remove stuff, make two apps
- remove proprietary things
- identify the work that there'll be for you

## Can it handle agnosticism?

The usefulness of an app is related to its agnosticism about user choices. 

On one level: Is your app a Stripe subscriptions app, or is it a subscrptions app that can speak to Stripe?

On another: if it's a Stripe subscription app, can it play nicely with the end user's account models, or must it absolutely connect to the one you specify?

On the other hand, you can't handle every possible scenario, and if you try to handle anything and everything you're going to be left with a limp mess of an usable app. Is everything configurable? Ew.

## Typical kinds of apps

- miscellany apps (django extensions)
- utility apps (model-utils, form utils)
- specific service apps (twilio)

## When an app is too small

There's a nebulous critical mass that an app should reach before it's
released and maintained as a standalone app. First of course, if we're
drawing a distinction around Django _apps_ is that it shoudl provide
some kind of necessarily installable feature like models or template
tags (Django 1.9 _might_ allow for tags to be loaded without installing
an app, check on this). 

## When an app is too big

It's easier to _add_ features into a program than to remove them, and
that goes double for library code like standalone apps.

## When to turn back

If there's a lot of coupling in a big app _and_ you're dependent on it,
_and_ you're not willing to put in the time and risk to refactor, then
it might be worthwhile reconsidering. There's no value in having a
standalone app in and of itself, it's the 

## Saas example

Product & account & account management & subscriptions are all separate things.

This is a gross simplification in the example of course, where "product" is going to represent quite a bit. However 

## Allowing customization

### settings values

### class specifications

### middleware

### "backends" - inverted control

settings

registration (decorators)

## How to integrate back

mixins

decorators

the trouble with base classes (relationships to abstract classes


## When should you start thinking about extracting?

This is a subjective question to which I don't have a concrete answer
for you, but I tend to like this probabilitistic reasoning:

> If I do something twice there's a pretty good chance I'm going to have
> to do it again.

If you're building functionality into a project for a second time - or
certainly beyond that - then you almost certainly have a justification
for extracting.

It's worth noting that even in this case the answer may not be
extracting into a reusable app. If each time you reuse the code you make
a lot of changes, even little ones, you may end up creating a
monstrosity of configuration checks just to make a usuable app. The key
here is if you're really repeating the same thing or the similar thing
you're creating is approaching a stable set of features and code.

### Separation anxiety: Reasons and excuses for not extracting

The first of course is that it's *work* to extract an app and turn it
into a standalone app. We're going to take that as a given here though.
Yes, it's work, but in the goal of reducing future work. The net present
value should be *less* work.

You may also find yourself working through the structure and trying to
figure out how everything in yoru app shoudl relate to the rest of the
project.

It could also be that what we have is not really a distinct foundational
app. The solution here is either to leave it alone or change how you're
building your apps in your project.

### Beat it, or at least breaking it up

The best way to start with the mechanics is to remove the app from your
project.

You may need to work on the app in place, first.

In isolation it will soon become clear if your app has unnecessary or
troublesome coupling with other parts of your project.

### Pulling it out, adding it from outside

The proof is in the tasting of the pudding, and the saem is true of
adding your app back into your project.

The easiest way to do this is to keep it in a private version control
repo, and use a version control pip requirement, e.g.::

```
git+https://myvcs.com/some_dependency@sometag#egg=SomeDependency
```

More on this can be found in the [pip requirement files
documentation](http://pip.readthedocs.org/en/stable/user_guide/#requirements-files).

Barring any changes to namespace, you shouldn't need to change
anything in your settings file.
