# Automate with CI

We've built up quite a bit of steps in developing the app, and we'll need to
keep them going for continued maintenance. We want to ensure the tests are run
all the time, that we're building documentation We want to ensure the tests are
run all the time, that we're building documentation We want to ensure the tests
are run all the time, that we're building documentation We want to ensure the
tests are run all the time. When you're writing code on your own, you may not
care to run the entire test suite against every single commit.

Automation is a good idea in any project, but its the payoffs that
differ. For a standalone app, especially once that's out in the wild
with other users, potentially other collaborators, and your limited
time, the benefit is quickly enforcing rules and taking work off your
hands. Okay, that's the same benefit for your regular projects too - but
there are ways to make this all work for distributed teams of people who
don't even know each other.



## The Cloud vs. Self-hosted

It used to be that you had to have your own continuous integration server, that
you had to set it up, configure it, and keep it running. That might have been
fine for a large dedicated project or a whole bunch of them, but what about
that one-off that you write on your own?

Just as hosted version control replaced the need for most people to have their
own version control servers, a whole slew of hosted CI services have sprung up
in the past few years enabling the common man to host projects and run tests
automatically.

The big difference between hosted version control and hosted CI is that in the
former case, services are providing a hosted version of a common product, e.g.
Git, Mercurial, Subversion. No one is making up their own thing. Especially in
the case of a distributed system like Git or Mercurial this makes sense. The CI
services are largely proprietary though. Travis, Circle CI, and Codeship, to
name a few, is each built on a custom system with a different interface.

This doesn't pose the same problem, since we really just need the interface, but
there will be differences between each. Unlike setting up your own Jenkins server,
for instance, you might not have the ability to control what version or
versions of Python are available. On the other hand, you don't have do much
work for 90% of scenarios.

## Continuous integration

### Travis

Travis was the first non-Jenkins hosted CI platform that was widely available.
It began as an open source project.

To get started, add a `.travis.yml` file to your project root.

.. highlight:: yaml

    language: python
    python: 2.7
    env:
      - TOX_ENV=py34-django19
      - TOX_ENV=py34-django18
      - TOX_ENV=py27-django19
      - TOX_ENV=py27-django18
    install:
      - pip install tox
    script:
      - tox -e $TOX_ENV
    sudo: false

### Circle CI

### Codeship

### GitLab

Gitlah

### Jenkins

Jenkins is the granddaddy of continuous integration servers, or at least
one of the most mature open source offerings. It dates back over a
decade to a project called Hudson, from which Jenkins was forked due to
disagreements with Oracle, who had acquired control of Hudson. Jenkins
is written in Java and if you want to host it yourself you'll just need
to run it in a Tomcat container or something similar.

This is probably a better idea for internal projects which aren't
intended to be shared with the world due to the setup and maintenance
requirements.

## Coverage and more

### Coveralls

Coveralls is a *cover coverage* monitoring service. The 

### Require.io

