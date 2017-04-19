---
title: "Migrating assets to Django Filer"
permalink: /migrating-to-django-filer/
category: programming
layout: post
published: true
date: 2015-08-13
teaser: >
    django-filer is a great tool for reusing uploaded content across
    Django sites. It's an easy choice for new projects, but what about
    existing projects? Painless steps for migrating existing image and
    file uploads to django-filer.
---

When you want to add image support to your Django app, like allowing
content editors to upload images, how do you do that? Probably by using
Django's built in `ImageField` model field, which will store the file on
the file system (or other storage backend). But what about when you want
to be able to reuse images? Using a plain `ImageField` means you have to
upload images for each new use or perhaps create your own `Image` model
as a related entity... neither option tends to work out well for the
people actually using the site.

For Django projects, the best solution we've found so far to this
problem is
[django-filer](http://django-filer.readthedocs.org/en/latest/). Filer is an application that combines
convenient model fields for developers with a familiar file
tree like structure for users. Combined with standard image fields like
captions and alt text, as well as extra thumbnailing support, filer
stands out as a superior way to manage image content.

This is all well and good when you're starting a new project, but it's
never too late to make the transition to django-filer. Here we'll walk
through the process of rescuing your image content and surfacing it for
your users.

### Install Filer

Installation is a perfunctory first step. You'll need to download
django-filer (preferably by adding it to your project's pip
requirements file) along with easy-thumbnails, which filer uses to show,
well, thumbnails of your images.

{% highlight bash %}
pip install easy_thumbnails django-filer
{% endhighlight %}

Next add it to your `INSTALLED_APPS` tuple:

{% highlight python %}
INSTALLED_APPS = (
    'easy_thumbnails',
    'filer',
    'breeds',
)
{% endhighlight %}

'breeds' listed above is an app which tracks dog breeds in our imaginary
project.

Filer maintains its own database tables for tracking files and folders,
so you'll need to migrate the database changes it introduces.

{% highlight bash %}
python manage.py migrate
{% endhighlight %}

At this point you should be ready to start uploading media using the
filer backend. However to make any significant use of the filing system
you'll need to add filer's fields to your models.

### Add the new Filer fields

Here's a snippet from the basic breed model used to show different
breeds of dog:

{% highlight python %}
class Breed(models.Model):
    name = models.CharField(max_length=140)
    image = models.ImageField(upload_to="breeds")
    description = models.TextField(blank=True)
{% endhighlight %}

Using the Django admin to add and edit breeds, each form will have a
standard file input like this:

<input type="file">

What we want is the ability to upload a new image _or_ select an
existing image.

Given that we have a bunch of content already present, the first thing
we need to do is add the new filer field in addition to the existing
fields.

{% highlight python %}
from filer.fields.image import FilerImageField

class Breed(models.Model):
    name = models.CharField(max_length=140)
    image = models.ImageField(upload_to="breeds")
    description = models.TextField(blank=True)
    img = FilerImageField(null=True)
{% endhighlight %}

Pretty easy! You'll notice two important things right off the bat. The
first being that we have to use a new name for this field since two
fields can't share the same name, and two that the new field is
nullable.

Regardless of what you want your final data model to look like, the
column has to be nullable in our first step in order to simply add the
database column. After we've added all the content in you can go ahead
and remove this 'feature' if you want.

### The great data migration

The big step then is the data migration. We need to move all of the data
from the old image fields to the new image fields. The nice thing is
that we don't need to move the files themselves! That's a misconception
I've heard voiced before, but in reality all we need to do is ensure we
capture the references to these files and then delete the old references
- which is really all a file field is, image fields included.

For current versions of Django that looks like this:

{% highlight bash %}
python manage.py makemigrations --empty breeds
{% endhighlight %}

Using South with an older version of Django, the command looks like
this:

{% highlight bash %}
python manage.py datamigration breeds migrate_to_filer_images
{% endhighlight %}

That will create a data migration file named `migrate_to_filer_images`
for the app `breeds`.

In our data migration we're going to cycle through all of the existing
`Breed` instances and either find or create new `FilerImage` instances
for each image path.

{% highlight python %}
def create_filer_images(apps, schema_editor):
    from filer.models import Image
    Breed = apps.get_model('breeds', 'Breed')
    for breed in Breed.objects.all():
        img, created = Image.objects.get_or_create(file=breed.image.file, defaults={
            'name': breed.name,
            'description': breed.description,
        })
        breed.img = img
        breed.save()


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('breeds', '0002_breed_img'),
    ]

    operations = [
        migrations.RunPython(create_filer_images),
    ]
{% endhighlight %}

And using South for older versions of Django:

{% highlight python %}
class Migration(DataMigration):
    def forwards(self, orm):
        from filer.models import Image
        from breeds.models import Breed
        for breed in Breed.objects.all():
            img, created = Image.objects.get_or_create(file=breed.image.file, defaults={
                'name': breed.name,
                'description': breed.description,
            })
            breed.img = img
            breed.save()

    def backwards(self, orm):
        pass
{% endhighlight %}

The first thing to notice is the no good, very bad, terrible thing here,
directlyly importing the models into the migration file. This is
exactly what the default migration template tells you **not** to do!
There are good reasons for not doing this, generally, however here
following the guidelines doesn't work. Filer uses multitable inheritence
to subclass `File` in the `Image` model, so South's internal schema (and
likewise the subsequence Django machinery)
doesn't see a relationship between our table and the `Image` table. So
instead we import the models with the implicit understanding that we'll
squash these migrations later (its terrible anyhow to find long since removed
apps in your migrations).

The next thing to notice is that we're using the `get_or_create` method
here to avoid creating duplicates. We _shouldn't_ find any, but this is
an excellent way to avoid problems with edge cases. We can populate some
of the initial data from our model directly and change it later as
desired.

The `ImageField` on our model is really a foreign key so we need to
create our `Image` instance and then assign it to the individual breed.

{% include image.html src="/images/django-filer-vizsla.png" alt="filer" caption="Both the old ImageField and the FilerImageField shown" %}

### Update all of your \{\{ templates \}\}

We have filer images now so we're ready to start using them.

A simple URL reference like this:

{% highlight django %}
{% raw %}
<img src="{{ MEDIA_URL }}{{ breed.image.url }}" />
{% endraw %}
{% endhighlight %}

Now references the `image` attribute using the `ImageField` as a foreign
key:

{% highlight django %}
{% raw %}
<img src="{{ MEDIA_URL }}{{ breed.img.image.url }}" />
{% endraw %}
{% endhighlight %}

If you happen to be using easy-thumbnails you're simply change the field
name provided to the template tag, from this:

{% highlight django %}
{% raw %}
<img src="{% thumbnail breed.image 400x200 %}" />
{% endraw %}
{% endhighlight %}

To this:

{% highlight django %}
{% raw %}
<img src="{% thumbnail breed.img 400x200 %}" />
{% endraw %}
{% endhighlight %}

If for some reason it turns out that changing your templates is too much
of a hassle, keep reading for a few alternatives.

### Update references in forms and views

Similarly with templates you'll need to update any forms and views. This
is usually pretty straightforward, with the exception of any custom
validation or data handling.

As with templates there's an alternative way of getting around this at
least for simple cases. Any code in your forms or views that references
the image field _as an image field_ will need to be updated to ensure
comptability with the foreign key presented by the `ImageField`.

### Swapping out the old field

The last step is swapping out the old field. The primary way of doing
this is to make the old field nullable and ensure it's no longer
required. You can take care of this in your forms, and if you're using
the Django admin's default ModelForm you'll need to ensure this field is
allowed to be blank.

{% highlight python %}
class Breed(models.Model):
    name = models.CharField(max_length=140)
    image = models.ImageField(upload_to="breeds", null=True, blank=True)
    img = FilerImageField(null=False)
    description = models.TextField(blank=True)
{% endhighlight %}

### Removing the old field

The follow up here would be to remove the old field altogether. This,
however, is a post-deployment step. **You should only do this once you're
ready to squash or remove your migrations, since the way we've
implemented the data migration here depends on the presence of specific
fields on the model.** Simplest way to do this? Just remove the content
from the data migration so that it does nothing and imports none of your
models.

This kind of data migration is a one-shot migration to deal with
legacy content. Once you've executed it you don't need it anymore. You
won't be running the migration again in your production environment,
only in fresh environments like test or development machines, in which
case there is no legacy content. So if you do decide to get rid of the
old field and/or rename the new field, clean up that data migration
first.

I referenced a couple of work arounds with regard to changing the field
name in the rest of your code, i.e. templates, forms, views, etc. Both
options require that you've gone ahead and removed the original field.
The first is to add a model property with the name of the old field.
This should return a file instance just like the `models.ImageField`
would.

{% highlight python %}
class Breed(models.Model):
    name = models.CharField(max_length=140)
    img = FilerImageField(null=False)
    description = models.TextField(blank=True)

    @property
    def image(self):
        return self.img.file
{% endhighlight %}

If, say, what you're primarily worried about is templates *and* you
happen to be using easy-thumbnails then there's an alternate solution:
rename the new field to that of the old field. You'll need to specify
the database column name to avoid having to do yet another migration, a
rather pointless one by this time.

{% highlight python %}
class Breed(models.Model):
    name = models.CharField(max_length=140)
    image = FilerImageField(null=False, db_column="img_id")
    description = models.TextField(blank=True)
{% endhighlight %}

### Rehashing the game plan

The key to everything here is ensuring that you have the required
sequence of database migrations.

1. Add the new _nullable_ field
2. Create and link filer images
3. Make the old field nullable
4. Deploy
5. Remove the old field and clean up migrations (optional)
