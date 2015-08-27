---
title: "Git commits for collaboration"
permalink: /git-commits-for-collaboration/
layout: post
published: true
date: 2015-08-27
teaser: >
    Professional kitchens hum by practicing mise en place, ordering
    everything carefully and keeping this clean. You can do the same in
    a distributed software project by taking care with how patches are
    created and merged in.
---

This post is a note to self and an explanation for present and future
team members and collaborators. YMMV.

The goal is twofold: to ensure a *useful* history of project changes
with explanations for what and mostly why things changed the way they
did, and to make merging the change into the main project - with
everythign that entails (testing, building, deploying) - as easy as
possible for the people doing that.

The goal outlined below simplifies the process by limiting us to one
commit that can be cleanly merged into the main project.

### Assumptions

There are two remote repos, yours and the main project repo.

You have a local feature branch, called `my-cool-new-feature` where
you've been working on code. The only changes right now in this branch
are commits you've made specific to your feature.

The `master` branch of the main project repo represents code that is in
the wild.

The `master` branch has been getting updates since you created your
original feature branch.

People like it when you make their lives easier for them, even if that
means a bit of extra work for you right now!

### Step 1: updating from the main repo

Make sure you have the main repo referenced locally. Since this is the
Acme Corp's repo and I'm going to name it `acme`.

{% highlight bash %}
git remote add acme git@githost.com:acme/serious-software.git
{% endhighlight %}

Next I'll make sure I have a copy of everything they've been working on.

{% highlight bash %}
git fetch acme
{% endhighlight %}

And since I've left my master branch alone since I cloned their
repository, I'm going to update it.

{% highlight bash %}
git checkout master
git merge acme/master
{% endhighlight %}

Again, note the **strong asumption** that my preexisting master branch
had only commits present in `acme/master`. This would have resulted in a
merge commit otherwise - most likely. The master branch should mirror
the main remote master branch, which means never commiting directly to
it or merging to it from a local branch - and as a safeguard, never
doing that even if you know the outcome will be as expected by pulling
from the `acme` repo!

### Clean patch commits

Let's look at what clean patch commits mean before proceeding.

The goal of the patch commit - or pull request commit - is to be
readable, to explain to the maintainer what happened and most
importantly why, and to code archeologists, too. You'll often find
yourself trying to track down a change in some code, either related to a
bug or to explain why something is the way it is, and quality commits
and commit messages help this a lot.

{% highlight bash %}
commit 1bb539d83916c7a34d714ba87f4e2a8782f132dc
Author: c0d3r <manic.coder@juno.com>
Date:   Fri Aug 14 13:05:52 2015 -0400

    update

commit 3560993da4f024bf2d3babc7a765af86ab884282
Author: c0d3r <manic.coder@juno.com>
Date:   Fri Aug 14 12:26:46 2015 -0400

    new thing in class

commit 84f1fe2bfd7f34d2a35a969a547b3e7db53e5d2e
Author: c0d3r <manic.coder@juno.com>
Date:   Fri Aug 14 12:22:56 2015 -0400

    fixed
{% endhighlight %}

Wat. This is not helping anyone.

{% highlight bash %}
commit 1bb539d83916c7a34d714ba87f4e2a8782f132dc
Author: c0d3r <manic.coder@juno.com>
Date:   Fri Aug 14 13:05:52 2015 -0400

    Updates financial model class calculation order

    Refactored the primary calculation method into several less stateful
    methods which calculate components individually. The interface is
    the same to respect existing code, but this makes testing easier and
    will make scheduled feature updates much simpler.

    [#123123123]
{% endhighlight %}

### Step 2: crafting a clean patch commit

So we want to create a single commit from the numerous feature branch
commits. There are two methods for doing this.

**Squash method**

We want this to be clean with regard to `acme/master`, so having updated
our local `master` branch to mirror `acme/master`, we'll just create a
new branch from `master`.

{% highlight bash %}
git checkout -b feature-patch
{% endhighlight %}

Now we'll merge the feature changes in using the `squash` flag.

{% highlight bash %}
git merge my-cool-new-feature --squash
{% endhighlight %}

You may encounter merge conflicts here, so now you'll need to fix these.

This won't drop us into the commit message editor right away like
normal, so we'll have to explicitly issue the commit command.

{% highlight bash %}
git commit
{% endhighlight %}

Then you'll be presented with something like this in your editor:

{% highlight bash %}
Squashed commit of the following

    commit 1bb539d83916c7a34d714ba87f4e2a8782f132dc
    Author: c0d3r <manic.coder@juno.com>
    Date:   Fri Aug 14 13:05:52 2015 -0400

        update

    commit 3560993da4f024bf2d3babc7a765af86ab884282
    Author: c0d3r <manic.coder@juno.com>
    Date:   Fri Aug 14 12:26:46 2015 -0400

        new thing in class

    commit 84f1fe2bfd7f34d2a35a969a547b3e7db53e5d2e
    Author: c0d3r <manic.coder@juno.com>
    Date:   Fri Aug 14 12:22:56 2015 -0400

        fixed
{% endhighlight %}

At the very least you should change the commit title (the first line of
around 50 characters), but in most cases just replace the whole message
with your own helpful message.

**Rebase method**

Instead, create your patch branch from your feature branch:

{% highlight bash %}
git checkout my-cool-new-feature
git checkout -b feature-patch
{% endhighlight %}

Then rebase against the master branch:

{% highlight bash %}
git rebase master
{% endhighlight %}

You may encounter conflicts in the rebase process, so you'll need to
address these. There's a thorough explanation in the [Git book
online](http://www.git-scm.com/book/en/v2/Git-Branching-Rebasing), but a
short answer is as follows:

1. When prompted with a conflict, you should see which files have
   conflicts listed. `git status` will also show you this; they are the
   files that are not staged.
2. Open the unstaged files with conflicts and fix the conflicts! If
   you're not familiar with what changes to expect from the main repo,
   doing this manually is important to ensure you're not arbitrarily
   overwriting changes that should be included. Alternatively you can
   use `git checkout` with the `--ours` or `--theirs` flags, but keep in
   mind that when rebasing these are inverted from what you expect them
   to refer to when merging.
3. Stage the files you've changed with `git add <fixed-file-name>`. Be
   careful about this! Either wait until you've fixed all of the files
   or explicitly add files by name after they've been fixed. `git diff`
   should not show any differences before you stage a file.
4. Continue rebasing, using `git rebase --continue`.
5. If there was only one file listed, Git may complain after a
   `continue` command that there were no changed. Just run `git rebase
   --skip` at this point.

This will have the effect of taking your feature branch commits and
putting them at the end of the git log, after all of the new
`acme/master` commits, regardless of *when* they were made.

Next we'll rebase again! But this time interactively, in order to squash
and cleanup *our* commits.

{% highlight bash %}
git rebase --interactive HEAD~4
{% endhighlight %}

This will open our editor displaying the last 4 commits. I chose 4 here
because there are 3 in my fictional feature branch and I want to see the
last commit from `acme/master` for reference.

Each is listed with 3 columns, 'pick' in one, a short version of the
commit SHA in another, and then the commit title. For the bottom two
entries - the lastest - I'm going to change 'pick' to 'f', short for
fixup, which will squash the commits into the one above, and then in the
second commit - the first in my feature branch - I'm going to change
'pick to 'r', short for reword, to change my commit message.

When I'm done rewording the commit message I'll be dropped back to the
command line with a patch branch that we know will merge cleanly (absent
further conflicting changes added to `acme/master` before it's merged
and a patch that only shows the changes that need to be applied.

### Step 3: write a helpful commit message

We already wrote the commit message, so let's back up a bit. Commit
message expectations and content will vary somewhat from project to
project, but there's a general style that ought be followed. Tim Pope
more than adequately [explains in
full](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
Here's his model commit message:

{% highlight bash %}
Capitalized, short (50 chars or less) summary

More detailed explanatory text, if necessary.  Wrap it to about 72
characters or so.  In some contexts, the first line is treated as the
subject of an email and the rest of the text as the body.  The blank
line separating the summary from the body is critical (unless you omit
the body entirely); tools like rebase can get confused if you run the
two together.

Write your commit message in the imperative: "Fix bug" and not "Fixed
bug" or "Fixes bug."  This convention matches up with commit messages
generated by commands like git merge and git revert.

Further paragraphs come after blank lines.

- Bullet points are okay, too

- Typically a hyphen or asterisk is used for the bullet, followed by a
  single space, with blank lines in between, but conventions vary here

- Use a hanging indent
{% endhighlight %}

I prefer a more present tense for the message, the "Fixes bug" example,
because that answers the question, "What does this commit do?" and
because I don't like using too many generated commit messages.

Commit messages are for other people, your future self included. They
are wayfaring points for future travelers, not bathroom graffiti for how
you feel about the world. If you fucking hate this stupid shit then
fucking open Twitter, not your commit editor.

And if the commit references something like a bug ticket or even a
project conversation, by all means make reference to that in the commit.
Many of these will have a convention of their own based on system
integrations, but otherwise including the URL with an explanation of the
reference will almost certainly prove helpful.

### Step 4: merge request!

That's it! Now it's time for a pull request. Push your patch branch and
issue the request from that branch. If you wrote a good commit message
you should not need to add much more explaining your pull request beyond
the commit message.

### Some notes

Using a *GUI Git client will probably be a problem*. I've found them to be
confusing beyond handling basic commits and merges. The confusion you
may see using the command line is less because of the command line
itself and more because you're being exposed to the changes you actually
have to make to the repository.

There's no special need to reduce everything down to just 1 commit.
*Often several commits will be better, but only when they're logically
reduced*. Let's say you have 12 small commits including a couple of
commits interspersed where you couldn't help yourself from reformatting
some nearby code (probably don't do this though, right?), some test
updates throughout, and then feature code updates. Using an interactive
rebase you can reorder these and then squash them down into a
reformatting commit, a tests update commit, and then a feature code
commit.

Whether this is necessary or valuable is going to be depend on the
situation. Working with inherited code I often find the need to reformat
the entire file before really working on it, and that I maintain as a
distinct commit so it doesn't obfuscate the changes I'm making to the
codebase.
