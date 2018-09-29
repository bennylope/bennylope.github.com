# Static assets

"Static assets", images, CSS, and JavaScript files, are a less common
component in standalone Django apps. However they 
but occassionally important inclusion in standalone apps. It warrants
the question why, though, if in describing the use of templates we've
already covered that such assets should be minimized in including
templates.

### Why

A few of the scenarios in which you might include assets like this
include:

- Focus on a specific front-end framework (e.g. Bootstrap)
- Additional admin functionality

### What to include

A better heading here might be what *not* to include. There are two scenarios
in which you're including static files: you need them for some Django admin
functionality or you need them for some non-Django admin functionality. It's a
binary choice.

### Library dependencies

It might be tempting to think, my cool widget here requires Angular.js, so I'll
just include Angular... whoa. Unless your app is in fact a Django package for the
purpose of shipping Angular, there shouldn't be any need to include the library
in your package.

Most projects will be including fiels like this through front-end sepcific build
processes, so there shouldnt' be much need to do so here.

### jQuery and the Django admin

If you're using jQuery, it's a good idea to test that your code is compatible
with the version of jQuery that ships with Django - provided, of course, that your
intention is to include it in the Django admin.

And of course if you're calling these sources from templates then its' at the users'
discretion to change them.

The Django admin packages jQuery using the `django.jQuery` namespace. If
your app requires a jQuery version incompatible with the one shipped
with Django (unlikely, but possible), then you can safely refer to your
version loaded using the typical `$` namespace.

### How to package

This part is pretty easy. Your static files should be included in
your app folder just as if it were an app in your own project.

    |- myapp
    |---static/
    |-------myapp/
    |-------------/js/myfile.js
    |-------------/css/myfile.css

A> Don't forget to include these files in your package when you prepare it.
A> They'll need to be explicitly included in your Manifest.in file. See
A> the section on packaging for more details.


