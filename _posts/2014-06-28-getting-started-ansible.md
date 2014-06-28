---
published: true
title: "Introducing Ansible into Legacy Projects"
subtitle: "Getting started when you've already started"
layout: post
permalink: /getting-started-with-ansible/
soHelpful: true
comments: true
teaser: >
    When you start looking at tutorials and guides for a configuration management
    tool like Ansible, most of them show how to get started or provide a great
    picture of what a nice complete set up looks like. That's great if you're
    trying to figure out the basics or start building a new project, but it leaves
    open the question of how to start applying these tools - and concepts - to
    existing projects. This is a story on how to do that.
---


When you start looking at tutorials and guides for a configuration management
tool like Ansible, most of them show how to get started or provide a great
picture of what a nice complete set up looks like. That's great if you're
trying to figure out the basics or start building a new project, but it leaves
open the question of how to start applying these tools - and concepts - to
existing projects. This is a story on how to do that.

### Why Ansible and not *just* Ansible

We'll look at how to do this using Ansible as the tool but the principles are
largely tool agnostic, so if you're using Puppet or Chef or Salt or Bash
scripts it shouldn't matter too much.

For smaller projects and for getting started in general the barrier to entry
with Ansible is considerably lower. You can eschew needing agents on your
target machines and for most configuration the playbook YAML is simpler to work
with.

### The existing project situation

For the example I'll use a project we've been working on. It's a site that
we've been working on in maintenance mode for the past couple years after
taking over that role from another agency and inheriting the existing system.
We're now working with this agency to redesign and overhaul the site, which is
going to include some significant upgrades to core components.

The stack includes Nginx to reverse proxy requests and serve static media,
Apache running mod\_wsgi to serve Django requests and to serve PHP for the
WordPress site running on the same domain; PostgreSQL for the main Django site;
MySQL for the WordPress blog; Memcached for caching; Postfix for email routing;
and of course the assorted other system components like cron jobs and general
system configuration.

The stack was overdue for an upgrade along with the design, but with an OS
upgrade due itself, it was time to start updating everything else. We wanted
more up-to-date versions of Python and PostgreSQL, to start with, and better
control over logging and montioring.

### So where to start

The best advice I heard about implementing testing in a software project
without it is to start with the bugs. Every time you encounter a bug, write a
test to replicate the bug and solve the problem (and fixing the test). You just
keep doing this, and writing tests for new features, rather than trying to
approach writing a complete test suite from scratch, and eventually you get a
decent test suite with reasonable coverage.

Similarly, I found it start your configuration management with problem areas,
and notwithstanding that, start with anything you need to immediately change.
It also helps to pick things that require minimal configuration. Something like
memcached is a pretty good candidate here. You're installing it and then
modifying one configuration file. That's a cinch.

Start with the small pieces. Don't try downloading a complete set of roles
(Ansible) or modules (Puppet) to manage the entire service. Let's take Nginx,
for example. It's a fairly simple configuration albeit one with several
components. A full configuration will ensure that it's installed, manage the
service configuration, maybe update the startup scripts, and then let you add
your local sites.

So in our scenario what you need to do is update some minor item in the site
configuration for one site. Let's make it simple, it's just a redirect at the
web server level. Now you have a staging site and a production that you need to
make this change on, sequentially. You could decide to fully manage Nginx at
this point, but here I'd argue that it's enough to just manage that one file.

We'll set up an Nginx role - you could also just add a single playbook to do
this - with one task to copy the file. I noticed the staging and production
configuration files differed, too, so I'm going to add a site configuration
file for each environment. And all I'm going to do is copy (scp) the current
file directly from the server into my local repo. I've got a variable in the
playbook that knows what the environment is named, so I'll just use that to
pick the file. And to start, don't even make the change yet! Just run the
playbook (using the `--check` flag first) and ensure that it's now managed by
Ansible. First staging, now production, great, make the change, staging, now
production. We're done!

Here's our tasks file:

{% highlight yaml %}
{% raw %}
- name: Add default site
  template: >
    src="{{deployment}}_site.conf"
    dest=/etc/nginx/sites-available/default
  sudo: yes

- name: Enable the default site
  file: >
    state=link
    src=/etc/nginx/sites-available/default
    dest=/etc/nginx/sites-enabled/default
  sudo: true
  notify: Reload Nginx
{% endraw %}
{% endhighlight %}

Okay, we *do* need to add a handler here to get Nginx to reload with the new
site, so we'll add that in and execute again.

{% highlight yaml %}
- name: Reload Nginx
  service: name=nginx state=reloaded
  sudo: true
{% endhighlight %}

Here's the basic layout.

    roles/
        nginx/
            handlers/
                main.yml
            tasks/
                main.yml
            templates/
                staging_site.conf
                production_site.conf

This is overkill! There's a method behind this madness though. This gives us
easy access to the files.

And why templates?

Short aside, why roles? They're a good way of organizing code into like
components. They're much like Puppet modules or Chef  cookbooks if you need an
analog from those systems.

And for good measure add some comments to the file to the effect that one
should not make changes to it directly since its' now under new management.
(new management image here).

Now that this is working, hey, you know what, let's add in the instructions to
ensure that the service is installed and working. This is backwards, for sure,
but on the systems we're dealing with *it's already installed and running*.

{% highlight yaml %}
{% raw %}
- name: Install Nginx
  apt: pkg=nginx state=latest
  sudo: yes

- name: Add default site
  template: >
    src="{{deployment}}_site.conf"
    dest=/etc/nginx/sites-available/default
  sudo: yes

- name: Enable the default site
  file: >
    state=link
    src=/etc/nginx/sites-available/default
    dest=/etc/nginx/sites-enabled/default
  sudo: true
  notify: Reload Nginx
{% endraw %}
{% endhighlight %}

Obviously you'll need to change this a little bit if you're using `yum`. And if
you're not using Ansible you can still follow a similar pattern.

In this case here we're going from staging to production, but ideally this
would be going from local VM to dev to staging to production.

If this sounds crazy and exceptionally conservative, you're right. And that's
how I like it. We have an existing system, a production system even, and our
goal is not to make tons of changes at once, but incrementally in the smallest
fashion possible. Eventually as you start checking more systems and making more
changes you'll get more pieces of more services configured authoritatively and
codified.
