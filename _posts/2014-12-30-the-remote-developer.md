---
title: "The portable developer"
subtitle: "Writing code away from your desk"
layout: post
permalink: /the-portable-developer/
published: true
comments: true
teaser: >
    Writing code is freeing and you can do so from anywhere. Or almost
    anywhere.

---

I mostly work from a home office. Also co-working spaces. And coffee shops,
friends' homes, occasionally hotels, airport terminals, airplanes, even
historic lakeside palazzos, and over rural satellite connections in
[Middle Earth](https://en.wikipedia.org/wiki/Haast,_New_Zealand). I've
been writing this draft on the road in Philadelphia.

The freedom to work from anywhere you want can be wonderful but it's
mostly a function of having available wifi. Wifi is prevalent, it's
pervasive. Reliable wifi not so much. Learning how to work in
anticipation of total downtime or unusable Internet not only makes those
situations less problematic but will also help you work faster in
general.

### WiFi is an unreliable friend

The first rule of working on the road is do not expect usable Internet
access. The second rule of working on the road is do not expect usable
Internet access.

At home I can mainly ignore this rule. My
overpriced, underperforming FiOS connection is at least incredibly
stable. But on the road that connection will be slow, it will be expensive, it will
not be consistent, it will not be available. It will somehow manage to
be a combination of all of these things.

Okay, turn off your networking. Now try to work. What is failing? Is
this going to be a problem?

### The magical cloud

To the cloud! "Cloud" based services let you offload work and storage
from your local computer to a magical realm of virtual machines. What
you gain in sharing between devices you often lose in offline access,
from mail to project management.

The solution here is to use a tool or process that at least mirrors this
information locally.

Important emails? If not available in a local email client, ensure
they're in a notes application (e.g. Evernote). Sharing files? Use a
tool like Dropbox, Box, or Spider Oak to sync files across devices and
to publicly available shares, as opposed to an FTP server.

### Make the most of distributed source control

Hopefully this one sounds blazingly obvious to you, but use a DVCS like
Git or Mercurial. Get to know it and understand how to use its features.

### Reference code

I keep local copies of projects and libraries I use. This is helpful anyhow, as
ack is a lot faster and more effective than opening up a web based repository
and searching there. For projects that bundle documentation in the project
repository now I've got that too.

### SSH with more than a remote chance of success

#### tmux

Intermittent wifi connections are the bane of SSH users. You're going to lose
your connection, and its going to kill your session in the middle of something
rather important. This is where a terminal multiplexer is your friend. No,
don't run away, it's much simpler than it sounds.

Think of a multiplexer, like
[tmux](http://tmux.sourceforge.net/) or screen, as another layer for your console. When you log into a remote
machine via SSH, you start a terminal session that is associated with or attached to your SSH
connection. Lose the connection, lose your terminal session. With tmux, you
create a terminal session associated with a *tmux deamon*, a background
process that is running independently from your SSH connection. Close your SSH connection and it's still there. This will
not only save you when your connection inevitably drops but lets you close
your connection and walk away to let some job keep running.

#### Jump host

A jump server is in and of itself a great help. I keep a small (1GB)
instance available on [Digital Ocean](https://www.digitalocean.com/?refcode=5eeefd1f4dfe) with my SSH configuration synced and
various deployment scripts, etc. If I need to initiate an SSH based
deployment, I typically do so from there in a tmux session. I don't
worry about even a slight network burp interrupting it. (Of course the
same could happen to my droplet, the data center, or something between
the data center and the target machine, but I'm pretty confident the
likelihood there is far less than from a coffee shop).

The benefit of a separate server over just maintaining a tmux connection
on the target machine is that's available for moving data between other
servers, as well as long running processes that you might otherwise run
on your local machine. For example, working from a hotel connection last
night I could barely browse Yelp for a dinner spot, and I wanted to
start working on some data found in a couple multi-gigabyte files.
Downloading those to my laptop was out of the question, so I downloaded
them to my server and unzipped them there to start working on them.

This might be quicker on a laptop, but this is now out of my
workflow and I can close my laptop, walk the dog or get on a plane, and
let the script do its work.

### Documentation

No internet connection means no Stack Overflow, sorry. For a while I
relied on local copies of major packages I used so that I could
read the docs when I had poor connectivity (I still keep local copies!
see below). Now my primary documentation source is a Mac app called
[Dash](http://kapeli.com/dash) which manages numerous documentation sets
in one place. I have [Alfred](http://www.alfredapp.com/) connected to it
so I can search documentation by name for module and function names.

Dash isn't perfect. It's best suited for lookup up documentation about
named symbols. Even when how-to material is available it's easier to
browser than to search for it. But it's incredibly convenient to be able
to look up a function with only a few keystrokes.

### Package caching

If you do any kind of work where you need to frequently rebuild
environments or reinstall language-specific packages, look into a system
wide cache to avoid downloading packages more than once.

As most of my work is Python-based, I also use devpi as a PyPI caching layer.
The short of this is that if I try to install Django 1.6.5 in a new virtualenv
but I've already downloaded it from PyPI, I'll actually download it from
localhost, skipping the hit to PyPI. This is faster, to be sure, but also saves
a lot of headaches when there's no network connection. It solves those edge
cases where you want to add a requirement to a project that you've
already downloaded, but moreover it makes running tox tests 'safe' to do without an
Internet connection. I can add or rebuild all of my tox environments to test
against different versions of Python, different versions of Django, and rest
assured that I can do that without having to hit PyPI.

### Databases

Use local databases whenever possible or at least set up your workflow
in such a way that you can. It's that simple. Even if you primarily use
a shared remote database for development, ensure that you have a local
version you can work with when necessary.
