---
title: "Don't panic"
permalink: /dont-panic/
layout: post
published: true
date: 2015-07-27 21:57:20
teaser: >
    On responding to [technical] disasters.
---

Is there a fan nearby? Keep an eye on it, because sooner or later it's
going to turn into a high performance manure propulsion device.

In an ideal world, bad things never happen. You and your team are
so thoroughly prepared, everything is tested seventeen different ways,
and lady luck never leaves your side. Of course bad things *do* happen
and you have to be prepared to respond to them.

I've learned a lot from haing my heels to the fire. How to deal with
technical complexity and miscommunicated requirements as deadlines loom,
wildly unexpected bugs, and of course deployment disasters. I'm not
proud of having suffered these micro catastrophes happened, but I
imagine I'm not alone in having
suffered through such things.

After a few such beatings you take your
head out of your ass and figure out how to prevent similar a beating from
happening again. In the interim you still have to respond to the problem
itself though. Learning how to do that is just as important as figuring
out how to prevent the problem from recurring.

### Rule number one: don't panic

![Marc Almeida's zombies
http://marcalmeida.deviantart.com/art/Zombies-are-coming-331734882](/images/zombies.jpg)

Whatever happens, don't panic. Mere words here may not be sufficient to
keep panic at bay, but there's little else to it. Panic is the enemy of
the solution. It's Loki's toy for introducing chaos into otherwise tractable
problems. Panic makes you overcorrect your steering when your car
slides, try to gain altitude when you're losing speed. Panicking is a
sure way of making bad knee jerk decisions that grossly exacerbate
whatever issue you're dealing with.

As for how you actually do this, there is a mix of techniques and
perspectives to keep on hand.

The first is that your must remember that no one is going to die because
of this (unless they *are* because of the nature of what you're working
on, in which case just read on). This is an exceptional perspective
shift, that as bad as everything might be, no one is going to die.

As well, keep in mind that you want the problem to go away, and the only
way for that to happen short of the gods' intervention is to start
deliberately working to solve it.

In many cases, things are worse than they seem.

### Communicate about the existince and scope of the problem

It's easy to feel responsible for your crisis at hand and then reticent
about it, or to feel that you have the power to take care of it right
this second before anyone really notices. These instincts are
understandable but must be put away.

Firstly, the idea that maybe no one will notice is usually wrong. In a
client relationship you want to avoid the client asking you about what's
wrong - you should be telling them. And if you're working on a client's
product, they'll likely know. You can take control of the situation by
alerting them to the problem and letting them know that you're actively
working on a solution. Those two pieces of information are the most
important things to tell the client.

It also helps to explain, briefly, the scope of the problem and
your estimated time to resolution or at least next update. How urgent
this is will vary a lot based on what kind of problem you're dealing
with and the context of both who the client is and what the system is,
but in all cases its important that you take control.

But taking control is different than doing things off on your own. You
may need help from your client, like information about some other part
of the system that could be helpful. You'll likely want help from your
teammates, either technical or at least moral support. A second set of
eyes on what you're doing in the heat of the moment is especially
valuable. It's difficult to second guess your own assumptions otherwise.

Moreover, you don't want to give other people the opportunity to make
things worse. Maybe while you're working on the fix everyone holds off
deploying to ensure that everything's right and level again.

### Be deliberate and take notes

> Everybody has a plan until they get punched in the mouth.

I can't overstate the importance of being deliberate. Instead of
swinging away wildly and just tiring yourself out, you need to step back
and explicitly figure out what you're going to try. What do you expect
to happen? Why? How long will it take? What are the downsides?

If you don't have a checklist to guide you then build one, even just a
temporary checklist.

More often than not it's better to ask someone for help or do some quick
research before wildy trying things, the secondary effects of which you
may not understand.

Take notes with information about the problem, the state of the problem,
and what you've tried, along with the sources of any information you've
discovered. You will be tempted not to do this because it takes extra
time, but in most cases this extra time is negligible and you'll recoupe
this either during your crisis resolution, the next one, or hopefully
when you design a solution to prevent the problem from recurring.

Make backups of everything! In any way you can, ensure you have backups
or copies of what you're trying. Extra files, copy-and-paste into notes,
a new Git repo to track little things, it really doesn't matter. What
does matter is that you can track what you did, the state of the system,
and can go back to a previous state if necessary. If you don't know what
didn't work it gets hard to identify what will.


### My last face of manure

In the first couple years of going into business for myself I became
too accustomed to panic, triage, and putting out fires. Its a rare
occurance now but they still happen from time to time.

The last was only a few months ago, during an otherwise routine
configuration deployment. I changed some logging configuration on an
application server - managed with Puppet - and because it was such a
small change, didn't bother testing against the Vagrant dev environment.
I deployed the change to the staging environment without a hiccup, and
then immediately deployed to production. And then the server went down.

The first thing I did was curse, loudly, and then try simply restarting
the server. Nothing. So next I tried running the initialization command
without the script and saw errors about the Python module `pkg_resources`
being missing. Looking at the Puppet run it was clear that the pip
requirement files (used for managing Python dependencies) were already
different in the two environments and the Puppet run on production only
ran there. Somehow it ended up removing or reinstalling a packaging
related package and nothing else could be installed.

At this point - maybe a couple of minutes into the server halt - I
emailed the client POCs and told them the site was down, that I did it,
the brief context, and that I'd have it up shortly with updates in the
interim.

Luckily, or so I thought, I had notes on dealing with a similar problem
- I'd seen this error after fetching new versions of the Vagrant box. My
notes were insufficient and I was left staring at a Python virtual
environment that I couldn't recover. Which is when the solution revealed
itself - just create a fresh environment!

I moved the old virtualenv so that I had a full copy, whatever benefit
that might be at some point, and created a fresh environment in the old
one's place, ensuring too that the previously missing pinned dependency
was present. Then I tried starting the application server again and...
oila!

The immediate step here was emailing the client POCs with a summary of
what happened, why, how it was fixed, and plans for ensuring it doesn't
happen again. The scary reply from my client? "Thanks for the update and
solving it so quickly." I later learned that they had made a deployment
disaster of their own the week prior and by comparison the issue I
thought was a big deal was resolved rather neatly.

### Learning from disaster

>  Fool me once, shame on — shame on you. Fool me — you can't get fooled
>  again.

After the dust has settled step away if you can. Let everything, take a
breather, and regroup mentally. 

Don't start making changes
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
