---
published: true
title: "Single value unpacking in Python"
layout: post
permalink: /python-single-value-unpacking/
teaser: >
    Unpacking single value tuples because asking forgiveness is better
    than asking permission.
---

Just a short description of a non-surprising but non-obvious feature of
tuple unpacking in Python (2.7, not even the cool new unpacking in 3.5).

Tuple unpacking is the extraction, the unpacking, of values from a tuple
into an equal number of new variable names.

{% highlight python %}
>>> point = (45.34, -23.12)
>>> x, y = point
>>> x
45.34
>>> y
-23.12
{% endhighlight %}

You can do the same thing with a tuple of one value.

{% highlight python %}
>>> value = (123,)
>>> x, = value
>>> x
123
{% endhighlight %}

I said this is unsurprising because unpacking is kind of like pattern
matching into another tuple on the left side (emphasis on "kind of") and
a tuple of one value is represented by a trailing comma like in the
assignment above to `value`.

Here's an alternative to unpacking this way:

{% highlight python %}
>>> value = (123,)
>>> x = value[0]
>>> x
123
{% endhighlight %}

So what's the benefit of single value unpacking versus using the index?

It's certainly more idiomatic *with regard to tuples* so there's that
reason. It also may make for more consistent code if you're unpacking
other tuples of more than one value in the same code block. A better
reason is Pythonic *forgiveness seeking* when extracting values with
constraints.

The motivating example is handling `*args` for one and only one value.
For example, a
Django management command has a `handle` method which must be defined
and accept an `*args` argument. If you want to get the first argument,
you can just use the 0 index.

{% highlight python %}
class SomeCommand(BaseCommand):
    def handle(self, *args, **options):
        my_value = args[0]
{% endhighlight %}

However you should handle the case where no arguments were passed.

{% highlight python %}
class SomeCommand(BaseCommand):
    def handle(self, *args, **options):
        try:
            my_value = args[0]
        except IndexError:
            raise CommandError("No arguments provided")
{% endhighlight %}

This may be sufficient for cases where you have one or more arguments,
but if you want to enforce only one positional argument then you'll need
to do something else.

{% highlight python %}
class SomeCommand(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("One argument must be provided")
        my_value = args[0]
{% endhighlight %}

That works(!), but it's not *Pythonic*. The Pythonic way is to ask
forgiveness, not permission. So we use single value unpacking and watch
for a `ValueError`.

{% highlight python %}
class SomeCommand(BaseCommand):
    def handle(self, *args, **options):
        try:
            my_value, = args
        except ValueError:
            raise CommandError("One argument must be provided")
{% endhighlight %}

It's worth reiterating that the previous example is perfectly valid and
absent single value unpacking is the way I'd go.
