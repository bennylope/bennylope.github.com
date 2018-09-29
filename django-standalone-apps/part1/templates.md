# Templates

Not every Django app needs templates, but if your app renders any kind
of content to an end user, either in a web page or even an email, it
certainly will make use of them.

If these were templates directly in your own project, you'd probably
include very specific templates, with your markup, perhaps using your
chosen front end framework, and content specific to your app. This
doesn't make sense to include in a standalone app though.

However if your app provides any content that does render template
content, you should include basic templates bundled in your app, both to
faciiltate testing and to provide guidance to users.

### What to include

You don't need to and should avoid including elaborate templates. For
most cases, just basic HTML without extraneous CSS or JS.

The purpose of including templates is three-fold: to show clearly what
templates are available and to make it easy to update them, and secondarily
to show how context variables are used in the templates.
Not to mention that if you want to test your views you'll have a bad time if
the templates they refer to are missing.

This might seem redundant because this is already apparent from your
views or perhaps you've done a good job of including this in your docs. However
its important to think of the different audiences working with your app.

For a designer working on a project using your app it'd be easy to
copy the complete directory of templates into the base project - the copies
of which should now be loaded first and used to override the original
app templates.

This will also allow you to effectively test your apps functionality
that uses these templates. Otherwise you'll need to skip testing these
areas or provide templates from a separate testing project.

What else should you know? Be careful with base templates. There's a
convention in Django projects to base everythign on a `base.html`
template, but that's not a given. So behind inheriting from a template
your app provides - that is central to your app - avoid extending from
presumed project templates.

But, you say, these templates should really include a lot of complex
content! Then just include the bare essentials. Alternatively, include a
bit more generic content if the template is intended to be uses as is.
And of course if you're targetting specific output like a front end
framework, then include the expected finale product.

### How to package

This part is pretty easy. Your templates should be included in
your app folder just as if it were an app in your own project.::

    |- myapp
    |---templates/
    |-------myapp/
    |-------------/list.html
    |-------------/detail.html

This ensures that provided your users are using the
`django.template.loaders.app_directories.Loader` that their proejcts will
load the app templates and that they're properly overloaded
when your users override in their own project's `tempaltes` directory.

A> Don't forget to include these files in your package when you prepare it.
A> They'll need to be explicitly included in your Manifest.in file. See
A> the section on `Packaging` for details.

### Email templates

If your app makes use of email, for notifiying users of events, for
example, then you'll want to include email templates as hinted at above.

I've found that a good, easy to understand way of organizing these is
using a `templates/email` directory.

    |- myapp
    |---templates/
    |-------myapp/
    |-------------/email/
    |------------------/email-body.html
    |------------------/email-subject.txt
    |-------------/list.html
    |-------------/detail.html

A named preface may suffice, but if you more than a handful of templates
using a separate directory can make identifying the templates easier.

It's not a firm rule, but if you're not sure then do include the subject
from a template. This may not make sense for every email, but it makes
changing the email subject easier for end users. (And don't forget to
use `{% spaceless %}` tags in the subject or otherwise strip out
incidnetal line breaks before adding rendered content to the email
message itself).

### Alternative template engines

.. todo:: fact check whether we want to call this shipping iwth an engine

Django 1.8 introduced support for multiple template engine backends
including both an interface for custom tempalte engines and shipping with a
Jinja2 template engine. Should you include alternate templates?

Unless you plan on using both Django templates and Jinja2 templates (or a custom
template engine), probably not. While Jinja2 is a powerful template engine and
incredibly popular outside of Django, it's not a common choice.

What are some scenarios where you would want to include alternative,
non-Django templates? Well for starters, if that's what your app
specifically targets, such as a Jinja specific library, then by all
means include them. Or if you're including *both* Django and Jinja
templates, then that would work well.

These are of greatest importance where a template is designed to be
included without the rest of the templates of a site. If your app's
templates are designed to be used in a way to render content independnet
of the typical views, that is, in some way that shouldnt' be based on a
site wide base template, then these issues are not of great concern.
