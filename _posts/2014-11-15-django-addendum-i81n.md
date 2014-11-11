---
title: "Mulitlingual Django Addendum"
subtitle: "Adding internationalization suppport for the non-CMS snippet manager"
layout: post
permalink: /adding-i18n-support-django-addendum/
soHelpful: true
published: true
comments: true
teaser: >
    Django Addendum lets you easily edit arbitrary text snippets on a site
    without a full-fledged CMS or issuing another site release. It's like a
    micro-CMS for any site. Now you can add text snippets and translations in
    any language your site supports. This is a feature description and
    explanation of the design decisions and development path.

---

Django Addendum is a little library I wrote a couple years back to solve a
recurring problem: making copy snippets on a web page editable. More
specifically, making arbitrary blocks of text in Django templates admin
editable regardless of the template's application source.

It's pretty simple: you tag a block of text using the `snippet` template tag -
this is the default text - and then by using the snippet name you can add
updated copy via the admin. The template tag does the lookup. It's designed to
work with caching enabled so that after the first cache miss - if there is one
- there's only one database query until the cached value is added.

A few people requested multilingual support and it became apparent that this
would be really valuable to quite a few people. I put it off long enough and
after some investigation into the alternatives decided to draft up a new
release.

### Model translations

The obvious strategy was to integrate with an existing Django model translation
app. I had previous and fairly happy experience with the fittingly named
`django-modeltranslation` package so looked there first. However based on my memory
and a fresh review it seems a better fit for direct project integration. It
works by adding new attributes (i.e. table columns) for each translated
language of each targeted content attribute (table column). As you might guess
this requires migrations, project specific migrations. This is a non-starter
for a reuasable app.

I also took at a look at `django-hvad` which uses a different strategy to
accomplish a similar goal. Regardless of schema migration issues this package
would require subclassing a custom meta model class for the core models, which
means requiring the hvad package with Django Addendum. Using either one of
these of course means making a decision about what model
translation library Django Addendum users should use on the rest of their
sites, or at least add an additional requirements.

At this point is just seemed more straightforward to add in some translations
directly.

### Model and table strategy

There are three ways to go about adding the translations:

1. Allow the addition of language specific attributes/columns (e.g. `text_en`, `text_es`)
2. Create language specific rows/instances using a language attribute/column
3. Add a distinct model/table for translations

The first would be my choice for a totally project-managed app, but for a
reusable app this goes out the window for reasons stated above.

In comparison to the third strategy the second has a lot going for it: it's
simple and especially in the context of the Django ORM would require fewer
queries (pretty hard to run a UNION query in the ORM). However I really wanted
to be able to use a default snippet and to be able to edit all the content for
a given snippet on one page.

The uniquness constraint - the key and language - would suffice as a
composite primary key but Django doesn't support that. Without this
constraint the only real risk is duplicates and then getting an
unexpected translation value.

The Django admin's inline admin classes make editing related content on one
page a cinch, so it made sense to add the new model. There's a side benefit for
non-i18n users as well - it makes it easy to hide this functionality if you
don't need it.

### Modifying the cache strategy

The next component was the cache. Caching is very important for how Django
Addendum works. Performance in general is a good reason, but also it just
feels dirty initiating database calls from a template.

The previous release used a manager method cache lookup that returned a Snippet
instance from cache, a snippet instance from the database (after updating the
cache), or None. The new version needs to account for multiple languages in a
different model as well as a fallback snippet (the default).

The first strategy I tried was adding each snippet-language combination to the
cache using its own key. The downside to this is the cache miss scenario. Worst case:
language specific cache miss, language specific database miss, default snippet
cache miss, default snippet database miss. In the scenario of a missing
translation for a present snippet that still means an aniticpated cache miss
every single time to check for the translation.

*I'm quite opposed to inserting unnessary backend service calls in other
people's websites.*

The updated content caching strategy consists of caching all of a snippet's
content - translations included - in a single language-keyed dictionary for a
given snippet. For a given snippet a missed translation is simply handled by a
default dictionary lookup for the given snippet.

Moving away from caching Snippet objects means deprecating the manager class,
which was used only for getting cached snippets. Cache management is handled by
two functions - a getter and setter, respectively - including an update
function called on save by both the Snippet model and the SnippetTranslation
model, ensuring the cached content is always up to date.

### Creating an upgrade path

Adding translation support is now as simple as enabling internationalization in
your Django project - and writing snippet translations, of course.

To ensure the new cache format plays nice with existing installations a new
management command is available to update all snippets. And as mentioned
earlier, if i18n is disabled in your project, you won't see any of this. The
SnippetTranslation class is not exposed in the Django admin except through an
inline, and that is condtionally hidden based on the i18n setting status in the
project. Monolingual sites won't change, cache excepted.

And if anybody has any advice on fixing PyPI Readme formatting I'd love to
hear it!
