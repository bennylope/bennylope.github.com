---
author: Ben
title: "Simple search managers: fat managers & skinny views"
subtitle: "A basic search and filtering pattern"
layout: post
permalink: /simple-search-manager-methods/
canonical: https://wellfire.co/blog/simple-search-manager-methods/
published: true
category: programming
comments: true
teaser: >
    Most search requirements are pretty simple and can be satisfied
    without a search backend. Keeping the code clean and testable is
    easier with this manager based design pattern.
---

Not every search feature requires a third-party search system, like
[Haystack coupled with
ElasticSearch](/blog/custom-haystack-elasticsearch-backend/). In fact
a great many are served sufficiently well by basic SQL querying: A
case-insensitive similarity query on a single character field, e.g. a
title or description. Not even full-text search is required.

In a simple search view you might write something like this to let a
user search for and filter a list of countries:

{% highlight python %}
{% raw %}
def search_view(request):
    countries = Country.objects.all()
    form = SearchForm(request.GET)
    if form.is_valid():
        if form.cleaned_data["q"]:
            countries = countries.filter(name__icontains=form.cleaned_data["q"])
        elif form.cleaned_data["government_type"]:
            countries = countries.filter(government=form.cleaned_data["government_type"])
        elif form.cleaned_data["industry"]:
            countries = countries.filter(industries=form.cleaned_data["industries"])
    return render(request, "country/search.html",
            {"form": form, "country_list": countries})
{% endraw %}
{% endhighlight %}

There's nothing too complex here, but with additional filtering fields or
more complicated logic, it might not be something you want left to the
view function. Especially when testing is considered.

Since this deals with pulling from an entire database table it makes
sense to consider a manager for our solution.

### Using the manager method

Moving the search operations out of the view makes the view simpler,
keeps like functionality together, makes the code portable, and makes
testing much saner.

One of the goals is a clean interface, so to keep this simple we should
be able to pass in a dictionary of search and filtering parameters.
Turns out our search form already provides just the dictionary we want.

{% highlight python %}
{% raw %}
countries = Country.objects.search(**form.cleaned_data)
{% endraw %}
{% endhighlight %}

Now all the search and filtering logic can be encapsulated in the
manager method, and tested separately from the view.

{% highlight python %}
{% raw %}
class SearchManager(models.Manager):
    def search(self, **kwargs):
        qs = self.get_query_set()
        if kwargs.get('q', ''):
            qs = qs.filter(name__icontains=kwargs['q'])
        if kwargs.get('government_type', []):
            qs = qs.filter(government_type=kwargs['government_type'])
        if kwargs.get('industry', []):
            qs = qs.filter(industry=kwargs['industry'])
        return qs
{% endraw %}
{% endhighlight %}

Again, this small example might not look like it needs much testing, but
more complicated filtering scenarious typically do.

### Simplified search view

Now the logic in the view is far simpler and will remain this simple
regardless of what's added to the search form.

{% highlight python %}
{% raw %}
def search_view(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        countries = Country.objects.search(form.cleaned_data)
    else:
        countries = Country.objects.all()
    return render(request, "country/search.html",
            {"form": form, "country_list": countries})
{% endraw %}
{% endhighlight %}

You don't *have* to use the form to validate the data, instead passing
the request GET dictionary to the search method directly, however it's
good practice to clean this before sending it to our query.

Our view could be made yet more compact by adding and calling a method on
the form class like so:

{% highlight python %}
{% raw %}
form = SearchForm(request.GET)
countries = form.search()
{% endraw %}
{% endhighlight %}

This is how Haystack's `SearchForm` works. Here however it only serves
to move a single conditional statement down the chain and doesn't
provide much benefit.
