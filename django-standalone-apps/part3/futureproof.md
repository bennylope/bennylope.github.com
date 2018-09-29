# Supporting future versions

Given that a new Django version is released roughly every 9 months, how
do you deal with new Django releases? A good start is running tests
against the version under development. You can do this with tox, and
it's easy to do automatically if you have your project running under CI.

The core strategies are no different than what you'd use for maintaining
bakcwards compatability. The difference here is that you're being
proactive and also defensive when you can.

## Testing

If you don't have testing set up, then you need to start there. 

The first rule about future proofing is always be testing. If you're
running tests on a continuous integration service (see part 4) then you
can have this run tests against the development version of Django to see
how things are running, or wait until an alpha for the next version is
released.

## What to look for

Once you have and are running your tests, obviously you need to ensure
that they're passing. In addition, watch for warnings. These will
provide useful information about things changing in _subsequent_
versions of Django. This is useful for you to know so you can make the
necessary updates, but unaccounted for they're annoying and noise -
rather than signal - for users of your app.

Release notes for the dev version can also be helpful.

Note that theres no need to continually follow the Django dev branch
development for this purpose. Rather, when you decide to track a new
version of Django, check out what's in the release notes, and then again
when you're ready to cut a new version of your app against the latest
Django version.

Most of the incompatabilties should show themselves as errors (test
failures or errors) or warnings. The time this might not happen - at
least warnings - is when Django internals are changed that aren't
exposed as an intended public API. 

## Syncronizing with Django's release schedule

The firsg thing to keep in mind is that you're under no obligation to
release an update to your app the moment a new Django version comes out.

That said, if you're testing your app against the development version of
Django, you can release a version of your app that is already known to
be compatiable with upstream changes in Django. It's not even necessary
for the next version to be released yet. That is, of course, as long as
you're flagging that functionality or otherwise conditionallty handling any
differences.
