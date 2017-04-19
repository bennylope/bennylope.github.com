---
title: "Python refactoring: comprehensions for great good"
permalink: /python-refactoring-with-comprehensions/
layout: post
category: programming
published: true
date: 2015-12-14
teaser: >
    List comprehensions help keep code both concise and clear while
    adding a slight performance boost. Comprehensions of all kinds,
    including set and dictionary comprehensions, as well as the related
    generator expression form, are useful tools for building and
    cleaning up existing codebases.
---

When digging into a codebase to either for the expressed purpose of
cleaning it up or starting to work on features or bug fixes, one of the
first things to look for in refactoring are interfaces with iterables:
their selection, their creation, and how they're selected from.

Invariably, you'll find code like this:

```python
mylist = []
for something in more_somethings:
    if something.is_valid():
        mylist.append(something)
```

If you were to try explaining what this does in English, you might be
tempted to start from the top: this creates an empty list, and then it
loops through the `more_somethings` variable... stop!

That is how the code works above, but that's not really what it does. It
creates a list of items from `more_somethings` that are valid. That's
it! So what's the problem with the above code? It can and should be
written like this:

```python
mylist = [thing for thing in more_somethings if thing.is_valid()]
```

Which block of code better fits our description of what the code does?
That's right, the list comprehension.

## What are comprehensions: a quick review

List comprehenions are a syntactic feature in Python (borrowed from
Haskell) that allow you to create a list from another list using a
set builder notation. Or to be more specific, that allow you to create a
list from another *iterator*. Further, the syntax provides for logical
conditionals that allow you to filter the source iterator into your new
list.

And better yet, beyond list comprehensions there are other iterator
comprehensions that let you create iterators other than lists, including
dictionaries, sets, and even streams.

## Why comprehensions

Whether refactoring or otherwise, why bother with list comprehensions?
I'll give three broad reasons:

- Pythonic
- Explicit
- Fast\*

Let's go through these one by one.

### Comprehensions are Pythonic

The first reason to use comprehensions is that they're idiomatic Python. This is not a silly
reason! In general I think its worth doing things the idiomatic way for
a given language, barring good justification to the contrary. When
working with other people it helps to work in an expected way. To do
otherwise is like walking into an Australian coffee shop as an American
and asking for a venti soy latte. If anybody does know what you're
asking about you'll be lucky to leave with an eyeroll. You learn how
people work in a system and you go with it. Not because it's good to be
a conformist but because you need to make sure everyone understands.

Further, the idiomatic way of doing things, Python specifically and
often other languages, is quite often an optimized way of doing them.

### Comprehensions make explicit what they return

The strongest reason to use comprehensions is their clarify. It's not
just line count. Comprehensions make clear what they return by their
syntax. They allow you to skip the mechanics of constructing a list and
do it in place. Look, it's a list, it's got *brackets*. 

### Comprehensions are faster (usually)

For at least basic list assignment, a comprehension is faster. I ran a short and
informal benchmark starting with this code, simply executing with `time
python test.py` to check execution times. Here's the original:

```python
sentence = "thequickbrownfoxjumpsoverthelazydog"
vowels = {'a', 'e', 'i', 'o', 'u'}
for x in range(1000000):
    blah = []
    for i in sentence:
        if i in vowels:
            blah.append(i)
```

Here's the comprehension version:

```python
sentence = "The quick brown fox jumps over the lazy dog"
vowels = {'a', 'e', 'i', 'o', 'u'}
for x in range(1000000):
    blah = [i for i in sentence if i in vowels]
```

In fact, I tested this with by adding `blah = []` before the
comprehension line to see what the variable assignment was doing, and
the list comprehension version was still reliably about 15% faster than
the list iteration and append version.

I'm not going to make any grand claims about list comprehensions always
being faster, but a little testing leads me to believe that all things
being equal, they're faster than looped list-appending.

## Beyond the list

The structure of a list comprehension is something like this:

```
<delimiter> <element expression> for <element> in <iterator> <conditional with element> <delimter>
```

Breaking this down we see that the square brackets are the delimiters
used to contain the scope of the comprehension. They also indicate the
type of object returned. We can change the delimiters used and now also
change what kind of object is returned.

Let's start switching around the delimiters.

### Dictionary comprehensions

It's probably best to start with the syntax.

```python
some_dict = {k: v for k, v in [('a', 1), ('b', 2)]}
```

This comprehension iterates through the list of tuples, unpacks each
tuple into a pair of two independent values, and then uses those as the
key and value to create the dictionary.

Of course you can create the same dictionary using the dict constructor.
So when would you use a dictionary comprehension? The obvious answer is
when you want to transform or conditionally include items pulled from
the iterator.

```python
some_dict = {k: v for k, v in [('a', 1), ('b', 2)] if v % 2 == 0}
```

You could build the same dictionary using the dict constructor and
tuples from a generator expression - more on that below. I tend to think
the curly bracket expression for defining dictionaries tends to be more
immediately descriptive.

### Set expressions

Set expressions landed in Python 2.7 and work much as expected.

```python
some_set = {value for value in some_iterator()}
```

Here's the set of vowels from our sentence, in uppercase:

```python
sentence = "The quick brown fox jumps over the lazy dog"
vowels = {'a', 'e', 'i', 'o', 'u'}
set_of_vowels = {upper(i) for i in sentence if i in vowels}
```

### Tuple... nah! Generator expressions

Despite appearances, there is no tuple comprehension. Instead, we have
generator expressions.

Why? I'd reckon for two reasons: unlike lists, sets, and dictionaries,
tuples are immutable and in the context of most Python code it doesn't
make much sense to construct them in the same way you would a list or
set. They're really record types. Secondly is because, well, we have
generator expressions instead, and these can actually be warped into tuple
generators, so they've got that going for them, too.

Here's a sample list comprehension:

```python
birthdays = [day for day in list_of_days if day.has_birthday()]
```

And here's the same rewritten as a generator expression:

```python
birthdays = (day for day in list_of_days if day.has_birthday())
```

The syntactical difference is the use of parentheses instead of
brackets, as if we were constructing a tuple. The result of this
expression, however, is a generator object. It has no value itself,
rather it computes each sequential value as you iterator over it.

## Refactoring and usage notes

Comprehensions are useful in projects new and old. In working on older
projects however I've found them to be useful in reducing crufty code
and bringing into relief what the real purpose of the code is.

With a grain of salt at the ready, you can go through old code and just
start replacing any instance of a list, set, or dictionary built in
place by initializing an empty object and adding to it with a
comprehension equivalent. As a default strategy this will yield fewer
unnecessary lines, easier to read lines, easier to comprehend code, and
quite often fewer bugs (I've seen more than my share of poorly attempted
assignment in for loops that did nothing - harder to get away with that
in a comprehension).

### Function returns

The most obvious case for a comprehension of any kind is a function that
returns an iteratable of that type (note that I say iterable not
iterator; if you want to build a generator there's no benefit to using a
generator expression).

```python
class SomeClass:
    ...
    def odd_children(self):
        return [child in self.children if is_odd(child)]
```

### Side effects

Don't use comprehensions for the purpose of creating side effects like
file output. That may well not work as expected and it occludes what
you're trying to do. Comprehensions scream "object constructed and
returned here" so if that's not your purpose then they're the wrong
tool.

### Nested and long statements

A refrain I've come across is that you should only use comprehensions if
they span a short single line, otherwise get rid of them. And likewise
with nesting. That's not *bad* advice but it's not good advice, either.
The real answer is always, "it depends".

A long comprehension expression can be split.

```python
mylist = [transform(item) for item in somelist if condition(item)]
```

Can be written instead as something like:

```python
mylist = [
    transform(item)
    for item in somelist
        if condition(item)
]
```

There's not much of a gain in this particular example - the original
isn't that long - but it's hardly bested by the recommended alternative.

```python
mylist = []
for item in somelist:
    if condition(item):
        mylist.append(transform(item))
```

What about complex nested comprehensions? My answer here is that if the
comprehension *clearly* shows the structure of the returned object, then
it's a good idea.

```python
class Region:
    def city_json(self):
        return json.dumps([
            {
                state.name: [
                    {
                        city.name: city.population
                    } for city in state.cities
                ]
            } for state in self.states
        ])
```

This is going to return a structure that *looks* like the JSON it
renders.

```javascript
[{
    "Virginia": [{
        "Richmond": 220000
    }, {
        "Charlottesville": 50000
    }]
}, {
    "Maryland": [{
        "Baltimore": 622000
    }, {
        "Frederick": 67000
    }]
}]
```

## Skip for more complex logic

For anything more complex or that requires some knowledge of the object
under construction you'll just have to skip comprehensions. This
includes complex predicates.
