---
author: Ben
title: "Finding the Needle: Wellfire at DjangoCon 2013!"
layout: post
permalink: /finding-the-needle-djangocon-2013/
redirect_from: /blog/finding-the-needle-djangocon-2013/
canonical: https://wellfire.co/blog/finding-the-needle-djangocon-2013/
published: true
categories: events
comments: true
description: "DjangoCon 2013 in Chicago was a great opportunity to meet other Django developers, to learn from them, and to share some of the lessons we've learned."
---

Wellfire was at DjangoCon 2013 in Chicago this year and it's high time
we reflected a bit about the conference and our experience there. This year
we had the chance to share with the community in the form of a talk I
gave on implementing search in a Django project.

### Finding the Needle

This talk grew out of a talk given at [Django
District](http://www.django-district.org) in the spring of 2013 and
reprised last month in its latest form. The talk is a *talk* without
heavily textual slides, so if you missed it you can catch a recorded
version of the talk.

<iframe width="620" height="390" src="//www.youtube.com/embed/k9NpO7VzWVw" frameborder="0" allowfullscreen="true">&nbsp;</iframe>

It's an intermediate-level talk, expecting that you have a reasonable
level of experience with Django regardless of your hands on experience
with search. It starts from the beginning, defining the search problem,
explaining how search engines help, integrating search into a Django
project using Haystack, and some strategies to consider. But you can
flip through the slides yourself.

<script async="true" class="speakerdeck-embed" data-id="a195d1e0f7050130b0617a614700254e" data-ratio="1.33333333333333" src="//speakerdeck.com/assets/embed.js">&nbsp;</script>

One question I wish I had answered differently was about why to use
Haystack; in light of some of the extensive-looking work arounds I
implemented and discussed, why not just use the `pyelasticsearch`
library directly? Especially when you want to avoid database hits when
displaying results.

My revised answer would be to mention the `load_all` keyword argument
which will reduce the database calls if you need to fetch model
attributes from a search result set and, more importantly, content
indexing. Even if you use a more direct connection to the search engine,
like `pyelasticsearch` or ElasticSearch's new official Python driver,
Haystack is *still* going to be an immense aid in identifying content to
add, update, and remove from the search engine.

### Great talks and a super community

The conference's two tracks meant that a lot of speakers got to present
and of course that it wasn't possible to get to every talk. I met a lot
of conference regulars and first-time attendees, not to mention
first-time speakers. It spoke very highly of the community at large that
so many people felt comfortable and compelled to speak for the first
time, and at their first conference, and that the quality of these
first-time presentations was so high.

The DC Django community got some great representation. Josannah Keller
gave a community-oriented talk, [My Bootcamp Brings all the Nerds to the
Yard: Lessons from
GeekChic](http://www.youtube.com/watch?v=7GhuTZLkqDU), which I heard was
awesome but I missed (again, the two tracks!). Longtime DC Python and
Django denizen Eric Palakovich Carr shared in [Winning an Election with
Django and jQuery Mobile](http://www.youtube.com/watch?v=WJGHqwdA0hw)
how he used these tools to rapidly build and deploy to the field a tool
for his wife's city council campaign. While it was great to see how he
used these tools, it was just as interesting to see someone create a
project for a real end (not just another toy project). Matt Makai
gave an overview of some of the third-party services that further enable
a site, Django or otherwise, and presented a thorough set of strategies
for choosing and integrating them in [Making Django Play Nice with Third
Party Services](http://www.youtube.com/watch?v=iGP8DQIqxXs).

Three - three! - talks explicitly focused on some aspect of database
migrations. Apparently this is a big deal. The capstone of these was
Andrew Godwin's [Everybody Loves
Migrations](http://www.youtube.com/watch?v=JXGW56CGsCM). Andrew is the
original author of South and is wrapping up the first part of a
successful Kickstarter funded project to add database migrations into
Django core as of Django 1.7.


One of the talks I enjoyed the most was Eli Ribble's [Django Toolsets:
what are they buying you, what are they costing
you?](http://www.youtube.com/watch?v=5tWnapUszn4). In one of the few
advanced talks Eli discussed how his company successfully transitioned
from their old system to Django. Along the way they found that some of
the great libraries and plug-and-play apps out there don't always scale
to your use case that well. From migrating schema changes with South to
building APIs, this talk covers what worked, what didn't, how they
improved their system, and how large projects should approach
out-of-the-box solutions.

You can watch all the talks on the [Open Bastion's YouTube
channel](http://www.youtube.com/user/TheOpenBastion).

### Portland or Bust!

DjangoCon US 2014 is heading to Portland and we're already scoping out
the city. See you all next September on the West Coast!
