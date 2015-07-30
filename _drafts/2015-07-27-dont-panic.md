---
title: "Don't panic"
permalink: /dont-panic/
layout: post
published: true
date: 2015-07-27 21:57:20
teaser: >
    On responding to [technical] disasters.
---

Is there a fan nearby? Because shit will hit it.

In an ideal world, these bad things never happen. Your team is so
thoroughly prepared, everything is tested seventeen different ways

I've learned a lot with my heels to the fire. How to deal with technical
complexity and miscommunicated requirements as deadlines loom,
unexpected bugs, and deployment disasters. I'm not proud of any of these
things, but likely it's something a great many of you have gone through
as well. After a few such beatings I would take my head out of my ass
and figure out how to prevent such a beating from happening again. In
the interim I developed ways to handle the beatings with as much calm as
possible - which serves to keep them shorter - this is an exploration of
both how to deal with such disasters and how to avoid them.

...

### The last debacle

I've largely become unaccomsted to dealing with panic level issues now.
The last one happened over a month ago when I was making a small change
to the configuration for a client's application server. Rather than go
through the whole rigamorale of updating the configuration and then
reapplying to the Vagrant environment - since it was just one known
setting - I made the change to the Puppet configuration and applied to
the production environment. Then everything started to fail. Rather than
apply this one tiny change, this resulted in applying a significant
change to the Python packages, tanking down the entire application. The
Puppet manifest somehow updated the requirements such that we lost
distutils. That meant `pkg_resource` errors and hell, even pip wasn't
workign.

(FYI to self - tried on staging first)

I started wracking my brain, I'd seen this problem before with the VM.
How did we solve it? I usually keep pretty thorough and searchable notes
but couldnt' find anything terribly helpful. After a couple minutes I
sent a quick note to the client contact I had been in contact with
apprising them of the situation in brief - primarily to let them know
that someone was working on the problem.

Back to my notes I went and trying things.... watching the clock the
whole time. This is the worst part. It's bad enough trying to solve a
problem when you don't have the answers in front of you. But when you
know that time is making it worse... In the end I just updated the
requirements file, moved the old virtualenv, and created a new one from
scratch. It took a couple of minutes but it was better to spend a few
minutes on a 'known' solution. The site was back up shortly thereafter. 

After taking a few minutes breather I sent an email to the client,
including management, explaingin that they experienced downtime, why,
and what we did to remedy this. As well as an explanation regarding how
it could or could not happen again. The response I got was along the
lines of, glad you could fix it, we had a different deployment go wrong
even worse, so that's great that you got the site back so quickly.

Wat.

### Anatomy of an 'oops'

### Responding to disaster

### Coping with disaster

So how do you deal with this kind of thing? Ideally, avoid it, that's
the first thing, but failing that?

The first thing is don't panic. Panic makes you make bad decisions.

Be deliberate. An extra minute spent being deliberate will more of than
not save so much pain - and time - later.

Take notes. This isn't just about learning from your mistakes, it's
about tracking what you're doing. 

Make backups. Even shitty, manual backups to the /tmp folder.

Application deployment? Rollback, and if you can't, or don't want to,
try to create a deployment that splits the difference between the
previous deployment and yours. If you've deployed a big change, this can
help.

Double and triple check that the things you think are same across
environments are, in fact, the same. They're probably not, by the way.

Reconsider what services in what environments you have. Production web
app is down? Point the domain at staging and point staging's config to
the production DB. Never done this, but why not?

Back out of changes slowly and one step at a time.

Communicate what's going on. You should always beat a client to email or
the phone. Tell them what's going on, don't let them have to ask. This
is generally good advice if you're in a client services business, by the
way. Needy clients aside, if your clients are asking you questions about
what's going on you're probably not doing your job.

### Learning from disaster

After the dust has settled step away. Don't start making changes
immediately. You need to regroup mentally. 

When you have calmed down, identify what happened, what kind of paths
led or could have led to that outcome, and what you could do to prevent
such a thing from happening again.

If your plan includes things like, "do a better job" or "look more
carefully" then it's going to fail. It needs to be a change in process,
not just doing better. Nobody wins more basketball games by "playing
better next time". You identify that you need to get more rebounds and
practice getting more rebounds.

Big scary amount of code changed at once? Start figuring out how to
deploy smaller changesets. Someone forgot a step in building the
application? Automate it all.

When I compare how we operate today compared to five years ago there are
so many things that have changed. For one even when we do 'manually'
deploy it's with a single script call. The CI server runs all of the
tests, builds the docs, and deploys every changest to a development
server. We have VMs that look like production and everyone can work on
the same thing. 
