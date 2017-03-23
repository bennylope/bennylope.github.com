---
author: Ben
title: "Safe Content Updates Through Testing"
layout: post
comments: true
category: content
permalink: /testing-url-remapping-with-pyresttest/
canonical: https://wellfire.co/learn/testing-url-redirect-remapping/
teaser: >
    Your content is an asset - you already know this - but this also includes the rich web of links 
    on and outside your site that bring people to your site and help lead them through your content.
    When your site goes through an update that involves updating your URLs, how do you make sure
    you're not left with broken links and bad search results? A brief introduction to pyresttest for
    smoketesting and testing URL mappings.
---

When you change the information architecture of your site this often
entails URL changes as well.

Top-level sections may get renamed or removed. Individual asset URLs may
also be remapped based on architectural changes below. If you don't properly
map old URLs to new URLs then site users may suffer broken links,
and worse search engines may, too, resulting in less indexed content and
a drop in site traffic.

For most web sites this is a no good very bad thing!

Beyond a handful of URLs, verifying that everything is working as it should
be is challenging to manage manually. A better option is to script this testing.

### Testing URL remapping

If all you want to do is verify a set of URLs then it would be tempting to
use a CSV file and write a script to verify your redirect mapping. An ideal
solution would allow you to verify redirect URLs, check HTTP response status
code, and name tests individually and by group to identify issues.

Such a mapping file would include, at a minimum, the target URL, expected status code,
and the destination URL for redirects. Here's a short example:

    "/about-us/", 301, "/about/"
    "/buy/", 301, "/buy-today/"
    "/contact/", 200

A script to test these results is a simple enough exercise. We've included scripts
using the Python `requests` library to do just this. The script will take a host name
as an argument to use with the data file so that it can be targeted at development,
staging, and production systems. It then requests each URL, verifies the status code
matches the expected code, and then for redirection codes verify the redirected URL.

It works, with a few caveats. CSV is a great format for making data simple to edit and
machine readable, but it *can* get unweildy. This is especially true if you want
to do anything beyond these simple GET requests, like modifying or testing headers
or testing different request methods. Add to this that the fewer moving components
to maintain the better, and it'd be nice to find something that works better than a
homegrown solution.

This is where [pyresttest](https://github.com/svanoort/pyresttest/) comes into play.

### A very brief introduction to pyresttest

pyresttest is tool for testing RESTful HTTP requests. It's written in Python (hence the py
prefix) but unless you intend to write extensions this does not require any Python
programming. It will work just fine in a Ruby, Go, Node, or PHP project.

As a command line tool it works by specifying a root URL (host) address and then the
path to a YAML configuration file. The configuration file enumerates a list of URLs
to request and tests against the expected status code.

Here's a very basic configuration file adapated from one of the sample files.

{% highlight yaml %}
---
- config:
    - testset: "Basic tests"
    - timeout: 100  # Increase timeout from the default 10 seconds
- test: 
    - name: "Load the homepage"
    - url: "/"
- test: 
    - name: "Redirect the old page"
    - url: "/some-old-page/"
    - expected_status: [301, 302]

{% endhighlight %}

It includes three blocks, a configuration block and two tests. The important thing to note
about the configuration block is that it lets you modify a few values that affect
the entire test suite, like the timeout value.

Each test here includes an identifying name and a URL. Without specifying anything else a
few other values are given defaults.

- the expected status is 200
- the request method is 'GET"
- the body is empty
- the headers are empty

For basic smoketesting the defaults are enough. For the purpose of verifying remapped content we'll need to go a *little* deeper.

### Testing redirects

As you can see in the example we can test other status codes, and test against more than one. This
verifies that the resultant status code is *in* the list of expected status codes.

As an example this works, however in practice for URL remappings you should be looking for one specific status code.

> It's a good idea to deploy with temporary redirects (302) first and then change them to permanent (301) redirects
after verifying the production mappings.

Testing the status code is a start, but what we really want to test is where the response is
redirecting the request. To do that we use pyresttest's validator functionality.

Here's a complete test that 

{% highlight yaml %}
- test:
  - group: "URL remappings"
  - name: "Donation page redirect"
  - url: "/help/donating/"
  - expected_status: [302]
  - validators:
    - compare: {header: "location", comparator: "regex", expected: "/donate/$"}
{% endhighlight %}

The difference here is the `validators` key, and we give it one comparison. The test should compare
the `location` header (you probably know it as "Location" with a capital 'L') using a regex comparison
against the included regular expression.

It might seem a little strange to use regex here. The alternative would be to use an equality
comparison, however the Location value will include a full URL including the HTTP scheme and the domain.
So we'd need to include the domain in the test value. Doing so is fine if you are only testing on one environment
but this allows us test against different hosts. Due to the nature of the example regex using the
full URL will give you a more accurate test.

pyresttest will load the URL, ensure the status code matches one of our expected codes, and then validate
the header comparison we've included. We get a complete test that the original URL redirects, and that in
fact the redirected URL is as expected.

If you're explicitly checking hundreds of URLs, rather than, say, a couple dozen or so patterns, it may make sense
to use a different strategy, like the CSV-backed script alluded to at the beginning. With that much
data the YAML structure will get in the way. For smaller sets of URLs however you get a nice testing
tool out of the box.

### Post-deployment smoke tests

An added benefit once you set up your configuration file is that you can use it continually as a smoke test.
Add in some basic 200 code tests and run it as part of your deployment process to ensure that, if nothing else,
you haven't taken down your site and that it's still running for your visitors.
