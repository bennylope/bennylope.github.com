# Basic configuration and namespacing

Sometimes what is obvious when you're working with multiple apps in a single project becomes less so when you focus on an app on its own. One such thing is namespacing.

Namespacing comes not just from the module-level namespacing, but how the app is named when included in the project. You can name all your views something generic or very detail specific and allow overlapping view or URL names provided the URLs are namespaced.

## AppConfig

Django's `AppConfig` class lets you specify configuration data for your application including the name of your application, i.e. how Django identifies an installed instance of your application, how it is presented to users on a site where it is installed, not to mention letting you set up aspects of your application works at process start up.

At a basic level you should set up an `AppConfig` class that provides a name and verbose name for your app.

```
from django.apps import AppConfig
from django.utils.translation.ugettext_lazy as _

class SubscriptionsConfig(AppConfig):
    name = "subscriptions"
    verbose_name = _("Subscriptions")
```

Note the `name` isn't translated as this is used programmatically, whereas the verbose name may be presented to end users.

## URLs

URL namespacing is easy given that it's something you anyone using your app can add. They just need to add the `namespace` keyword argument to their `url` declaration and they can use whatever namespace they want.

The simplest thing to do is provide an application name as an argument for your URLs as an *object* in your `urls.py` file and instruct users to include this.

Modified from the docs:

```
url_patterns = ([
    url(r'^$', views.PlanList.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.PlanDetail.as_view(), name='detail'),
], 'subscriptions')
```

Instead of having your end users include your URLs module, they would include the object created above, e.g.

```
urlpatterns = [
    url(r'^plans/', include(subscriptions.urls.url_patterns)),
]
```

Avoid using `app_namespace` as this is deprecated.
