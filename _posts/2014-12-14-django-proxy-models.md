---
title: "How to use Django's Proxy Models"
subtitle: "Modeling custom behavior without touching the database"
permalink: /using-django-proxy-models/
layout: post
published: true
teaser: >
    While proxy models aren't the most critical feature in the Django
    framework, they do seem to get short shrift. Here's a look
    into how to use this feature to create new and clean interfaces to
    data without making changes to your database.
return_link: /simple-search-manager-methods/
return_text: Proxy models? How about search managers!?
---

Django's proxy models are one of those features that I remember reading
about and thinking, "oh, cool... I guess" and then moving along. From
time to time, they do come in very handy, but there's not that much
written about how to best make use of them

### What are they?

A proxy model is just another class that provides a different
interface for the same underlying database model.

That's it. Really.

A proxy model is a subclass of a database-table defining model.
Typically creating a subclass of a model results in a new database table
with a reference back to the original model's table - multi-table
inheritance.

A proxy model doesn't get its own database table. Instead it operates
on the original table.

{% highlight python %}
class MyModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UpperModel(MyModel):
    class Meta:
        proxy = True

    def __str__(self):
        return self.name.upper()
{% endhighlight %}

In the contrived example above we've created a second model class, a
proxy class. If you were to compare the field values for the instance at
primary key `12` for either an instance of `MyModel` or `UpperModel` they
would be exactly the same. The only difference is that the `UpperModel`
instance would print as the uppercase name of the model.

It's a contrived example, so let's examine the real usefulness.

### When to use them?

There are certainly legacy or brownfield use cases, when you need to fit
your models around an existing database, but they're useful in new
projects too.

Let's say you've got a content type that has some different sub-types
which all differ in some minor way. There's the main content type, which
we'll call a "story". Some stories have slightly different content needs - one may require an
image file that is displayed and another a geographic reference.
With these exceptions the content types all look
roughly similar and behave in the same way.

You could create distinct models for each of these with a distinct
database table for each, but do we really need a separate table for each
of these? This is unnecessary and it'll make aggregating these stories
significantly more challenging if we want to use the ORM.

An alternative is to create a field - a column, if you like - for
tracking the type of story and then creating proxy models for each story
type based on this value.

### Working with them in practice

In our example we want to be able to provide simple editing interfaces
to all of these models to the content editors. On the front end, there's
going to be a single list view of all stories, and then list views for
the different types, as well as detailed views for individual stories.

Aggregating heterogeneous types isn't straight forward using
Django's ORM. We could make use of the `ContentType` model and filter on
objects that were in one of our several story model types, or we could
join together several querysets as Python lists. We could
also perform a UNION query in a Raw queryset. That's pretty appealing,
but the one thing I don't like about adding too many raw queries into
Django apps is the fragility.

So what we want to do is use proxy models to create unique editing
experiences with one underlying database model.

We'll start with the base model.

Here's a simplified and contrived example `Story` model.

{% highlight python %}
STORY_TYPES = (
    ('f', 'Feature'),
    ('i', 'Infographic'),
    ('g', 'Gallery'),
)

class Story(models.Model):
    type = models.CharField(max_length=1, choices=STORY_TYPES)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    infographic = models.ImageField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True)
{% endhighlight %}

The field of note here is `type`. This is going to be used to toggle the
story type.

Our proxy models will look like this:

{% highlight python %}
class FeatureStory(Story):
    objects = FeatureManager()
    class Meta:
        proxy = True

class InfographicStory(Story):
    objects = InfographicManager()
    class Meta:
        proxy = True

class GalleryStory(Story):
    objects = GalleryManager()
    class Meta:
        proxy = True
{% endhighlight %}

The `proxy = True` statement in the `class Meta` section indicates that
these classes are proxy models. It's the manager class that we're using
here to differentiate the classes.

Each manager class simply returns a queryset that filters for the
appropriate `type` value.

{% highlight python %}
class FeatureManager(models.Manager):
    def get_queryset(self):
        return super(FeatureManager, self).get_queryset().filter(
            type='f')

class InfographicManager(models.Manager):
    def get_queryset(self):
        return super(InfographicManager, self).get_queryset().filter(
            type='i')

class GalleryManager(models.Manager):
    def get_queryset(self):
        return super(GalleryManager, self).get_queryset().filter(
            type='g')
{% endhighlight %}

Well what good is this, you say?

For one, it provides a nice interface for content type specific views. If
you have an infographic view, for example, the view can fetch the
specific infographic from `Infographic.objects.get(pk=view_pk)`.

And moreover, now we can create distinct admin interfaces.

### In the admin

The benefit here is that we can create different admin interfaces for
different objects that happen to be stored in the same database table.
Perhaps a blog post has an author and an author photo while a news item
should only have a title, summary, and outbound link.

Since we have proxy models for these, we can create different admin
interfaces (remember that Django picks up on registered models).



### Managers and a better interface

In this second example, we have media assets that need to be used in a
gallery. There are two useful models: an image and a video.

{% highlight python %}
class MediaAsset(models.Admin):
    type = models.CharField(max_length=5, default='image')
    caption = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

class Image(MediaAsset):
    objects = ImageManager()
    class Meta:
        proxy = True

class Video(MediaAsset):
    objects = VideoManager()
    class Meta:
        proxy = True
{% endhighlight %}

Again with the managers. Here's what these managers look like though:

{% highlight python %}
class ImageManager(models.Manager):
    def get_queryset(self):
        return super(ImageManager, self).get_queryset().filter(
            type='image')

class VideoManager(models.Manager):
    def get_queryset(self):
        return super(VideoManager, self).get_queryset().filter(
            type='video')

    def create(self, **kwargs):
        kwargs.update({'type': 'video'})
        return super(VideoManager, self).create(**kwargs)
{% endhighlight %}

You see what we did here is extend the `create` method available for
the `Video` class and *not* for the `Image` model. What we want to do
be able to do is create an instance of one of our classes without having
to specify the `type` value. Since the default value for the base model
is `image`, we don't need to specify a `create` method for `Image`
instances - they're the default.

The base model's default type is `image`, so if we do this...

{% highlight python %}
image = Image.objects.create(image=some_image_file, caption="")
{% endhighlight %}

...we get back an image, or rather, a `MediaAsset` with its `type` attribute
set to `image`. For a video, we need to ensure that the `create` method
updates the keyword argument to the base manager, and then this is
valid:

{% highlight python %}
video = Video.objects.create(video=some_embed_url, caption="")
{% endhighlight %}

Now, why bother with this? It's not *necessary*, but what it allows us to
do is provide an interface that differs in class only. If you're using
class based views, all you need to do is specify the class name in the
view and everything else flows from that.

Now we have a gallery view that displays all of the media assets for a
given gallery, and for any asset CRUD needs we can provide class specific
views without checking for the `type` value in the code and filtering on
that in our views.

In the case of the gallery view, we don't want logic checks in the
template for the type of asset used for generating the thumbnails, so we'll
add this method to the underlying `MediaAsset` class to provide a
consistent interface.

{% highlight python %}
class MediaAsset(models.Admin):
    type = models.CharField(max_length=5, default='image')
    caption = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def thumbnail(self):
        if self.type == 'video':
            return some_video_thumbnail(self.video_url)
        return some_image_thumbanil(self.image)
{% endhighlight %}

Seeing the specific class name is also helpful for understanding exactly
what you're working with.

Having unique manager classes allows you to treat the proxy models as
first class models in the rest of your code. You can use the managers to
ensure the standard model interface is applied.

### To use and not to use

There's nothing complicated about proxy models, there's just a little
bit of thought required in regards to how they can solve your problems.

The use case for proxy models, I've found, is the exception rather than
the rule. The key here is that our models, our end models that is, are
all pretty closely related. The content attributes don't differ all that
much. If your models differ greatly and you've no need for simple
aggregation, then skip the proxy models.
