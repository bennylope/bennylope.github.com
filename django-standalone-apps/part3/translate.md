# Translations

I think its fair to say that most native English speakers in English speaking
countries give little thought to how their software will be used by people who speak other
languages or by those in other countries. This works against your benefit since
the cost to you to make the software available in other languages is actually
not terribly significant, and you make it far more available.

## How translation works

Conceptually, translation is very simple. Have you ever used a
two-language dictionary, like a Spanish-English dictionary? You look up
a word in one language, for instance, "dog" in English, and find the
Spanish counterpart to it, "perro". Translation for most software - like Django web apps - is pretty similar. The key difference is the
*token* you use.

In a dual langage dictionary, the token is typically a word or perhaps a
phrase. In our apps, the tokens are strings. This means they
could be single words or much longer text. So instead of translating:

  The quick brown fox jumps over the lazy dog

By looking up each individual word, we'd provide a translation for the
entire string.

  El zorro marrón rápido stala sobre el perro perezoso.

This might sound inefficient, adding an entire translated string,
but there's really no sound way of translating individual words as
tokens in a way that would make sense.

String translations work by a lookup of a base string against a dictionary
for a specific language. The key here is that you need to provide that
dictionary! This may seem confusing at first, but the system software
called gettext only provides the machinery to get translations. It isn't
feasible to for this software to keep dictionaries for other languages
and it wouldn't even work well. Aside form linguistic choices based on
context, how it would it ever know to transate "Speedo" from US English
to "budgie smuggler" in Australian English?

Let's walk through the mechancis of how all of this works.

## Translatable strings

Ensuring that the user-facing strings in your app are translatable is the first and most important step in adding
translation to your app.

By user-facing I mean anything that an *end-user* will see. This doesn't mean exception message. It does mean validation
messages.

The Django docs do an excellent job of describing how to implement this, but we can afford a short summary.

For *Python code* you'll use either `ugettext` or `ugettext_lazy`. The difference between these two functions is that
`ugettext` strictly applies and returns the translation, whereas `ugettext_lazy` waits until it is called to return the
translation. This is analogous to how `reverse` and `reverse_lazy` work. You'll use the regular or eager version when
you're calling this right away. An example is a string constant with no variable formatting used to populate a standard
message.

messages.info(request, ugettext('You are logged in now.'))

Whereas if you want to define an attribute *declaratively* that requires some as-of-yet-unknown value, you should use
the lazy version.

class MyField(forms.Field):
    error_messages = {
        'invalid': ugettext_lazy('The 
    }


are translatable. That's a prerequisite for making translations here.
You'll want to ensure primarily that Python-based strings are translated
(e.g. forms, views, etc). You can likely leave the templates alone
unless you intend for the provided templates to be production ready in
any way.

Where are we going to look for them in the sample app? To start with,
form help text and validation.

What should be translatable?

1. Model field help text
1. Model field verbose names
1. Form validation messages
1. Admin descriptions
1. All template strings
1. Request messages

## Adding translations

### The locale folder

The first step is setting up a `locale` folder.

### Creating and editing files

Generate PO file.

    msgid
    msgstr

### Compiling dictionary files

mo files

## Getting help

You don't have to do this on your own. It may be worth doing if you know one
of the languages you expect or want it translated it, but chances are you don't. And without
some language knowledge Google Translate is going to get you in trouble. And you don't
really want to do all that translation work anyhow.

Instead, for your open source project you can use a third-party service. The most
popular is Transifex.

## Model-based translations

Here we mean database driven translations. These are necessarily user-owned, so theres
nothing you can or owuld do to provides these.

However what you can do is provide mechanisms to make getting this information
out of the mdoels you proivde eaiser.

django-modeltranslation
django-hvad

### Home grown system

As done in django addendum. Here the system works in a very specific way under the hood.
A template tag checks for a value, but it always check the cache first - it's a cache
oriented system. So in order to add translations, it was going to be necessary to change
this through the app itself. 


CommandError: Can't find msguniq. Make sure you have GNU gettext tools
0.15 or newer installed.


CommandError: Unable to find a locale path to store translations
- Add a locale folder
