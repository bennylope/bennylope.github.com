---
published: true
title: "Geocoding with Pygeocodio"
subtitle: "Writing a Python API wrapper"
layout: post
permalink: /geocoding-with-pygeocodio/
redirect_from: /2014/geocoding-with-pygeocodio/
soHelpful: true
comments: true
teaser: >
    In January 2014 a new bulk geocoding service landed with the public
    announcement of Geocod.io. I took a look at the service offering and
    their documentation and immediately thought about client projects where
    their tool would be useful. Their API is a pretty clean JSON based HTTP
    interface but on any given project I still don’t want to have to deal
    anew with sending requests, serializing data, and handling errors - even
    if it is simple. So to give myself a chance to test it out I started on
    the task of writing a Python wrapper for the API.
---

In January 2014 a new bulk geocoding service landed with the public announcement of [Geocod.io](http://geocod.io). I took a look at the service offering and their documentation and immediately thought about client projects where their tool would be useful. Their API is a pretty clean JSON based HTTP interface but on any given project I still don't want to have to deal anew with sending requests, serializing data, and handling errors - even if it is simple. So to give myself a chance to test it out I started on the task of writing a Python wrapper for the API.

### README driven development

After setting up the project scaffolding, I went to work on the README. What I wanted was a high level explanation of the wrapper's behavior and specific examples of what that should look like. In a small enough project like this you can define most of that very nicely in a single user-friendly document, and it's easier to design the end behavior from a user read document than from tests.

If you're asking, well, what about tests?, this certainly doesn't preclude writing tests or even following a test-driven development style. But jumping into testing first is getting into the weeds before you've decided what direction you're going to march. Describing the types of requests and writing sample code for making those requests and getting the data makes it much easier to reason about whether its sensible before getting into the project code.

### Design decisions

Given the simplicity of the service and the data, there weren't a whole lot of critical design decisions that I had to make.

The data returned from Geocod.io is in JSON and so easily serialized into Python dictionaries (and lists and strings). With a geocoded address, you're returned your query, the address parsed into components, and a list of geocoding address in order of predictive accuracy. It's tempting to think "I'll just need this particular piece of data" but past experience has taught me  that you should know that for sure when making that decision. So rather than flatten the data and choose a few attributes to keep in the end, it'd be wiser to make use of the return structure as it is. I didn't see a need to do anything 'extra' to throw away data that wouldn't be in the way. 

So rather than replace the existing data structure, I just added some convenient accessors. Each data structure is a slightly specialized Python list or dictionary to which convenience accessors have been added. Maybe somebody *wants* to use all of the alternate geocoded data, I don't know. There's a very good ethic that you shouldn't add features in anticipation of what someone *might* do or need in your software. I think that's very good. Here though we're not adding, we're simply not removing, and I think that's a sensible approach.

The benefits of this decision are several, but one was revealed in mid-February when Geocod.io started providing county names in their parsed addresses. Because pygeocodio provides a light wrapper around the serialized data sent back rather than wholly transforming it, existing versions of pygecodio make this new data accessible. There's no need to update the library to add an attribute, it's right there in the address dictionary.

### Choose the conventional

The only controversial decision I made was returning the coordinates of a location in (longitude, latitude) format, rather than the common (latitude, longitude) format. 

The typical way we represent geogrpahic coordiantes is latitude, longitude. We list the parallel first and the meridian second. I'd gotten into the habit of thinking of this in reverse, however, from working with PostGIS and GeoDjango. Further I presumed that since PostGIS represented points in this manner, that it was the GIS standard. It's atypical, but damnit, it's the data standard, and if it works for me *and* its the "one right way" then let's do it.

So the points method and the points returned in the lists were returned longitude, latitude. I knew that this was atypical so made a point to call this out in the documentation. I even gave thought to including alternate properties to retrieve the points in latitude, longitude pairs, but then thought better of it. That is until I discovered that the typical way is the typical way for a reason, and in fact PostGIS is the one doing things backwards. Legacy reasons, as it were. So with some serious thought I reversed this decision. Given that the project is still listed as alpha at the time, and that I was going to be doing this with ample documentation and in a new version, I felt comfortable doing that.

The lesson learned is that conventions are conventions for a reason. It's okay to do things differently when there's a solid expected payoff, but that expectation needs to be well grounded.

### Testing and environment choices

README driven development aside, you do need tests. The one significant point worth noting is the choice of Python versions to test against. I do the overwhelming majority of my Python work in 2.7 (thanks, dependencies) but look forward to adopting Python 3. At the same time I know the feeling of being screwed out of using a new library because a particular system I'm on is a version behind. So I included Python 2.6 and Python 3.3 in the testing suite. I've also made a habit of including PyPy in my [tox environments](http://tox.readthedocs.org/en/latest/). It seems like a really promising way of running Python programs, and frankly, the additional work of testing against it is close to zero. 

### More geocoding

Other than some minor tweaks here and there, there isn't really anything else that needs to be added to the library, so I don't plan on adding new features. I do like the idea of being able to geocode from the command line, however I'm not sure about the utility of a single geocoding service CLI tool - for now.
