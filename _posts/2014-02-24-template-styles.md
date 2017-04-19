---
published: true
title: "Cleaning Django template tags"
subtitle: "Lint-like checking for spacing style in templates"
layout: post
category: programming
permalink: /cleaning-django-template-tags/
redirect_from: /2014/cleaning-django-template-tags/
soHelpful: true
comments: true
teaser: >
    Web application templates should be readable. Sometimes the allure of
    killing "unnecessary" spaces or migrating styles from another templating
    paradigm leads to squished template tags in variables. If you're using
    Django, Jinja, or Liquid templates, these scripts can help.
---

Django templates, which share some common syntax with Jinja2 templates and
Liquid templates use curly brace delimiters to designate template context
variables and template tags (which perform functions in the code). The
variables look like this:

    {% raw %}
    {{ some_variable }}
    {% endraw %}

And tags look like this:

    {% raw %}
    {% some_tag var1 var2 %}
    {% endraw %}

The space between the delimiter and the content is important for readability.
And it's because of that readability that this spacing is a convention.

Sometimes the space gets lost, either from mistyping or mentally porting the
style from another language. Aside from violating our nice convention, it makes
the template code harder to read, and in dense templates difficult to reason
about.

    {% raw %}
    {%for x in list%}{{x}}{%endfor%}
    {% endraw %}

The curly-spacing.sh script in the
[template-cleaners](https://github.com/bennylope/template-cleaners)
repository automatically cleans up these mistakes.

    {% raw %}
    {% for x in list %}{{ x }}{% endfor %}
    {% endraw %}

For Django users it also includes a bonus django-url.sh script to upgrade old
style url tags in which a URL name is provided without quotes.
