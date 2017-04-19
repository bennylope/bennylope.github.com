---
published: true
title: "Introducing Ansible into Legacy Projects"
subtitle: "Getting started when you've already started"
category: programming
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

### Picking a starting point

The best advice I heard about starting testing in an existing software project
it is to start with the bugs. Every time you encounter a bug, write a
test to replicate the bug and solve the problem (satisfying the test). You just
keep doing this, and writing tests for new features, rather than trying to
approach writing a complete test suite from scratch. Eventually you'll end up
with a decent test suite with reasonable coverage.

Similarly, it's simpler to start your configuration management with problem areas,
and notwithstanding that, start with anything you need to immediately change.
It also helps to pick things that require minimal configuration, i.e. use the
snowball method. Something like memcached is a pretty good candidate here.
You're installing it and then modifying one configuration file. That's a cinch.

Start with the small pieces. Don't try downloading a complete set of roles
(Ansible) or modules (Puppet) to manage the entire service. Let's take Nginx,
for example. It's a fairly simple configuration albeit one with several
components. A full configuration will ensure that it's installed, manage the
service configuration, maybe update the startup scripts, and then let you add
your local sites.

### By example: configuring the status quo

So in our scenario what you need to do is update some minor item in the site
configuration for one site. Let's make it simple, it's just a redirect at the
web server level. Now you have a staging site and a production that you need to
make this change on, sequentially. You could decide to fully manage Nginx at
this point, but here I'd argue that it's enough to just manage that one file.

### Role call

We will go so far as to set up an Nginx role, rather than just using a one-off
playbook. This will require a small folder structure and will make further work
simpler, but the immediate benefit is that it'll be easier to work with files
and templates. There's a staging environment and a production environment, so
this difference needs to be accounted for. There are several ways to handle
this, but for simplicity in this example we'll use distinct files for each
environment.

Here's the role structure:

    roles/
        nginx/
            files/
                staging_site.conf
                production_site.conf
            handlers/
                main.yml
            tasks/
                main.yml

The files folder should be self-explanatory. There's a site configuration file
for each environment. The tasks folder is where all of the Ansible task files
go. When executing a role Ansible will look for `main.yml` - you can include
other task files to break up tasks into logical groups, but you'll still need a
`main.yml` file to include them from.

Here's what the tasks file looks like:

{% highlight yaml %}
{% raw %}
---
- name: Add default site
  copy: >
    src="{{deployment}}_site.conf"
    dest=/etc/nginx/sites-available/default
  sudo: yes
  notify: Reload Nginx

- name: Enable the default site
  file: >
    state=link
    src=/etc/nginx/sites-available/default
    dest=/etc/nginx/sites-enabled/default
  sudo: true
  notify: Reload Nginx
{% endraw %}
{% endhighlight %}

Your site configuration file names may differ.

A handler, as referenced by `notify` above, is a task executed in response to
another. Making the changes to Nginx's configuration isn't enough, we need to
reload those changes, too. I've added it for both tasks because I want Nginx to
reload under any change here, but definitely after the second task. However
since the first task could result in a change without the second doing so (the
link should be unchanged) I'll add it twice.

{% highlight yaml %}
{% raw %}
---
- name: Reload Nginx
  service: name=nginx state=reloaded
  sudo: true
{% endraw %}
{% endhighlight %}

For the contents of each site configuration file, start by copying the exact
contents of the target file from that environment. The first step is ensuring
that our process matches what's on the server. We're going to codify
the existing setup before making even a tiny change.

### Environments and execution

In order to deploy this change, we'll create a playbook to specify which roles
to include. Here's that file, called `configure.yml`:

{% highlight yaml %}
{% raw %}
---
- hosts: all
  roles:
  - nginx
{% endraw %}
{% endhighlight %}

Next create a hosts file for each environment, e.g. `hosts.staging`,
`hosts.production`. You can name them otherwise, of course, but that's my own
convention. The `hosts.staging` file will include your host servers, e.g.:

    [staging]
    mydomain.com

Note that you can add domains, IP addresses, or named servers from your SSH
configuratiNote that you can add domains, IP addresses, or named servers from
your SSH configuration.

One last thing: the tasks file references the configuration file paths using a
variable and that's not set anywhere. We'll use the `group_vars` folder to
include a file for each environment with variable definitions.
`group_vars/staging` will look like this:

{% highlight yaml %}
{% raw %}
---
deployment: "staging"
{% endraw %}
{% endhighlight %}

Pretty simple. You can also include an `all` file for variables which apply to
all hosts. These are overridden by host specific variables.

Your file structure should look like so now:

    group_vars/
        production
        staging
    roles/
        nginx/
            files/
                staging_site.conf
                production_site.conf
            handlers/
                main.yml
            tasks/
                main.yml
    configure.yml
    hosts.production
    hosts.staging

Now you're ready to execute:

    ansible-playbook -K configure.yml -i hosts.staging --check

The `-K` option will prompt for the sudo password; the `-i` option is followed
by the path to the hosts file we want to use; and the `--check` flag tells Ansible
not to execute any of the tasks but just report back whether changes would be
made. Our expectation is that no changes will be made - presuming, of course
that the file contents are exactly the same. Go ahead and run this without the
check flag on staging, and do the same sequence on production.

### By example: incremental changes

Now let's add our change to the configuration. It's a simple redirect rule, e.g.:

    location /redirect/ {
        rewrite ^(.*) http://www.othersite.com/ permanent;
    }

Drop that into the appropriate place in the site configuration file for each
environment. For good measure add some comments to the file to the effect that
one should not make changes to it directly since it's under new management.
Now execute the playbook again as before. Your one redirect is now active
across your environments. Woohoo!

### Complete configuration

Of course it'd have taken a fraction of the time to make this change directly,
but now you can repeat changes, exactly, across environments. You have the
benefit of being able to more easily test these changes and to retain a history
of what changed, by whom, and why.

Once you've got your immediate changes out of the way, start fleshing out your
configuration of the status quo. Add a task to install Nginx, and include
additional configuration files in their present state. For each addition,
execute the playbook across your environments in sequence, using the `--check`
flag as desired. This is a tad cautious, but the goal is to make small, easy to
track changes.

As you build out your configuration, including additional roles, the best test
of your configuration's completeness is how well you can rebuild your current
environment from the group up using your configuration code. A disposable
development environment such as a local VM or cheap cloud instance is your
friend here.

### Wrap up

Your strategy should be to start small, both in terms of the scope of processes
or files to manage, and to work incrementally. Work incrementally with both the
changes you make and the systems against which you make your changes.

If this sounds crazy and exceptionally conservative, you're right. And that's
how I like it. We have an existing system, a production system even, and our
goal is not to make tons of changes at once, but incrementally in the smallest
fashion possible. Eventually as you start checking more systems and making more
changes you'll get more pieces of more services configured authoritatively and
codified.
