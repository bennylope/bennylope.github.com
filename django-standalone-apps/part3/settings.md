# App settings

## What kinds of settings

## Where to get these

The root source of these settings is the project `settings.py` file, or
`django.conf.settings`.

    from django.conf import settings

    SOME_VALUE = settings.SOME_VALUE

The problem is that that's not safe. What if `SOME_VALUE` is missing? In
that case you probably want to provide a default.

    from django.conf import settings

    SOME_VALUE = getattr(settings, 'SOME_VALUE', False)

If you have more than few of these or you want to perform any additional
validation, this will start cluttering up your app files. A better
solution is to provide an app-level settings module that performs the
necessary imports, default value settings, and validation, and can
provide these values to your app. The new import then looks like this:

    from myapp import app_settings

    SOME_VALUE = app_settings.SOME_VALUE

Now this assignment is unnecessary and it makes more sense to simply use
`app_settings.SOME_VALUE` directly.

## The format to use in settings.py

There are two basic ways of collecting application settings from a
project level `settings.py` file:

1. Individual named settings
2. Monolithic dictionary

In either case, the settings values your app looks for in
`django.conf.settings` should be consistently namespaced to prevent
collisions with other app settings and to make the settings easily
identifiable.

    SOMETHING_COOL = True

That's not helpful.

    MYAPP_SOMETHING_COOL = True

That immediately describes what this setting is associated with.

### Individual named settings

This should be your default choice, individual values in the settings
files, namespaced by your choice of app settings namespace.

    MYAPP_SOMETHING_COOL = True
    MYAPP_SAY_HELLO = 'whatever.models.Okay'
    MYAPP_IS_IT_ON = DEBUG

### Monolithic dictionary

This doesn't have to be a dictionary, e.g. a tuple would work as well,
but a dictionary makes the most sense here.

    CUMULUS = {
        'USERNAME': 'YourUsername',
        'API_KEY': 'YourAPIKey',
        'CONTAINER': 'ContainerName',
        'PYRAX_IDENTITY_TYPE': 'rackspace',
    }

This style of setting makes sense when you have required configuration,
like to a backing service. If the alternative is something like this in
every single settings.py file:

    MYAPP_USERNAME = 'YourUsername',
    MYAPP_API_KEY = 'YourAPIKey',
    MYAPP_CONTAINER = 'ContainerName',
    MYAPP_PYRAX_IDENTITY_TYPE = 'rackspace',

Then a consolidated dictionary will be easier to manage, for both you as
the third-part developer and whoever is using your app.

### Mixing settings styles

The two styles of settings are not mutually exclusive.
