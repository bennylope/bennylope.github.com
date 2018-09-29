# Example starting point

To motivate this, let's start with an example. It's somewhat contrived
but based on code that I've seen out in the wild - and if I'm being fair
some that I've probably written myself.

This app in question provides  the business functionality of a really
cool app that does jiggery magic stuff (we'll come up with something
later). That is to say, it's all really necessary, the foundation of the
core app itself.

Let's look through the code a bit.

- MOdels

- Views

- Template tags

The full code for this example can be found in the appendix and in the
book repo.

What do you see here? Let's start with the models.

Let's generalize a bit about not just a Django app, but a web app, or
any app in general. It has a way of representing some state, of allowing
us to see that state, to change it in some way, and that's pretty much
the crux of it. Sure there's more stuff going on, but that's what most
of our web apps do: Create, Re.., Update, Delete.

The models include some way of organizing individual users into groups
that allow them to interact with or be related to other content
together, like teammates on a team. It actually has two of these models
and they're related in a simple hierarchy.

And of course there's the mdoels for tracking subscriptions, including
the plans that correspond to different prices and levels of account
access.

### App hygeine

Sometimes a little house cleaning is a prerequistie for pulling code out
into a standalone app.

### WHat to remove first?

If an app is getting cluttered, what do you remove first? The simplest
answer is the smallest thing. Ideally the least related to everything
else, and something which is primarly a dependency and doesn't depend
itself on other components in the app.

For easy, the first thing is utility type functions that are used or
might be used elsewhere. These should have a tight logical grouping. In
the case of our app here, the template tags don't really have a strong
relationship to the core of app in question. Theyr'e obviously useful,
but they seem ancilliary.

So these would be a good candidate to remove.

There are several other lines we can draw.

Identifying where to cut can be helped using a graph of the model
relationships.

It looks like the customer related functionality as well as the service
account provider functionality could be extracted, respectively.

### Moving subscriptions

The first step here is quite simple - we refactor the code so that all
of the subscriptions related code is in the subscriptions app.

The trickier parts here and in any app move like this will be the models
and URLs. Models are tricky because of database table names and
migrations. The last thing we want to do, with an application already in
production, is rename the database table in our migrations - the
migration won't rename the table, it will remove the table and create a
new one.

Here you'll need to use `RenameModel` from

If you're supporting South then what you'll need to do is ensure you
specify the *existing* table name in the model `Meta` class, then create
your migration *in each app* - the new one and the old one - and then
remove the code from migration methods, forward and backwards,
respectively.
-- todo: is there a 
