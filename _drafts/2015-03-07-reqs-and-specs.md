---
title: "Requirements and specifications: confusing the why, the how, and the what"
permalink: /requirements-and-specifications/
layout: post
published: true
date: 2015-03-07 18:14:44
teaser: >
    They tried turning specifications into user stories. You'll never
    guess how much money they spent cleaning it up.
---


What are the differences between specifications and requirements? 

It's a question that comes up implicitly in a lot of projects where
clients come to you or come to us with this preconceived notion of what
the application is going to look like, what the site is going to look
like perhaps. It's going to do this it's going to do that. So and so
wants it to look like this. They really like the feature from this app
or this site and so it's gotta do this. Well of course there may be a
much more structured approach where we've got some wireframes already
and we've got some designs that should make it easier for you to put the
proposal together. 

When we put together a project plan and you start developing, there are
two ways to do it: there are specs and requirements. Requirements are
the 'what's necessary' question. What do you need to do? Specifications
are the 'how.' How are you going to do that? 

![Horse and cart, Johann Adam Klein](/images/horse-and-cart.jpg)

### Driving

Figure out where you want to go. Then how are you going to get there
(the road). Then how you might change direction as needed. Don't specify
the lane you'll drive now. Actually figure out why you want to go there.

### Conversations with Jesus

So here's a good example: You're talking to someone who is a great
carpenter and you want to have this custom bookshelf built, and you're
like 'I know exactly what I want,' so you give him specs. It's got to be
this tall and this wide and it's got to have this many shelves. So the
carpenter spends a couple of weeks and you get this bookshelf back and
it's beautiful and amazing.

The only trouble is that it doesn't fit exactly. It's almost a little
too tight. And you know what? It doesn't account for the number of books
you have because you gave them the specs. If you had said here are the
requirements - it needs to fit in this space and I like to be able to
get books that I read frequently easily. I've got a whole bunch of
really big books - they're really big art books and then just a whole
bunch of paperbacks. Now the carpenter has requirements. So he might
take those specs and he's going to generate specs based on the
requirements. So the difference here is that you're taking an expert,
someone who knows the problem space and can formulate better solutions. 

### Bring forth the requirements!

So requirements are really a software development parlance. A user store
is an example of a requirement. It's really just a way of formulating a
requirement. Whether or not you do agile scrum or whatever the next
methodology of the moment is going to be, a user store is still a great
way of expressing what needs to be done, and from a user's standpoint it
says something like this type of user - you know an admin user - can get
a report and see who the most active users have been this past month.
And specs says this report is going to have this header here and it's
going to do this, it's going to pull this query.

What happens frequently when you the specs without getting the
requirements, you're not really targeting the actual problem. So specs
need to be developed with everyone on board. In a smaller team, it's
probably going to be you make sure the developers who are doing this are
the ones who are actually involved and the specs are probably...they're
going to...if it's purely backend or they're developing the stuff, it's
going to be they develop as well. If you don't do it with their input,
then now you're creating these arbitrary constraints that may not help
you solve your requirements. 

So going back, this carpenter example is a prime example of how this
works. You bring the requirements and you….Now, if you don't...there's
two (    ) you might have specs: 1) it's not a very complex job; it's
very simple. You know what? You've got a WordPress site and it's going
to be a blog and you might start spec-ing stuff out here. You're a
designer and it's a known issue: it's a blog. That's what WordPress
does. It's a blogging engine, so you're not worried about well I need to
be able to add a blog post. This is already a given. Now you're spec-ing
it out. Or, if you have a team of engineers, then you need someone else
to actual implement it. And that could be another engineering team, it
could be architects specifying the stuff, but that's how it's going to
work. Or you know maybe it's an API and you're spec-ing out the API and
then someone else is going to build it out.

The issue is that when you start spec-ing first is that it's a much more
rigid process. You can start out with specs and that's a prototype and
it's a loose specification and you can build to it and then you can very
quickly and you can stop and say great, now let's check this out. Does
this work? Does this do what we want it to do? How does it feel? Ok,
let's fix this, let's redo it maybe.

### Specified requirements and prototypes

But that presupposes two things: One - That it's a very loose
specification, again a prototype. It's very important that everyone has
bought into this idea and that everyone is sold on it. They really got
to be bought into it. They really got to understand this throughout the
project. There is still a risk that a prototype will anchor people's
expectations, so you do have to be careful with that even when the
entire team is bought in. The other presumption is that you have to
requirements separately articulated.  

Again, it doesn't have to be like a spreadsheet with your requirements
analysis or it doesn't have to be every single use story broken down and
estimated already, but at the very least you've got to have this stuff
explained and written down and articulated. Otherwise, the specs...what
are they doing? You're giving the how for the what that haven't been
answered yet. 
Can you imagine if you designed a car without knowing what you need to
do? It's great. You're going to build this...I want it to look this
way...I want it to look very pretty. The body has to have this kind of
angle and do this and this and it needs to be here, and then you find
out it was supposed to be an off-road vehicle and the specs are going to
define something that wasn't really appropriate or you knew something
else about it.

Now, you say ‘well, what if we specified how fast it needs to be able to
go and it's cornering ability, specifying that it needs to be able to go
through this kind of turn at this speed?' Great, you are specifying
requirements. Say what? I thought you just said specs and requirements
are different? Yes. These are very specific requirements that are still
requirements. They form the problem space around which the solution will
be built. They don't provide parameters around the solution itself. That
could be a little tricky, but requirements form the problem space for
which we could create the solution, so specific specified requirements
are just very precise parameters.

Now, the difference is when you have the...it's like taking this little
game that toddlers play where you put the different shaped pegs in the
different shaped holes. These specified requirements are just very
precisely cut holes. They still don't explain exactly how the block will
fit in. You say ‘well, if we already know the shape of the hole,
shouldn't the block fit in?' Well, if we were just dealing with blocks,
the answer is yes - very likely - but other shapes can fit in there too,
and if the requirement turns out to be that there are different holes
and that the blocks will have to fit in different holes, then perhaps
sizing it exactly with the exact same shape as the initial hole might be
really bad.

![Wooden blocks. Photo by Flickr user rosipaw https://www.flickr.com/photos/rosipaw/4643095630/](/images/wooden-blocks.jpg)

That's a little bit of a bad example because we don't assume a problem
space that we have is going to be so big, but it does get to the point
that we don't know ahead of time. So, you  just define what you need to,
and the requirements and the specs, which the entire team works on, you
get input from everyone. You're assuming you need to get information
from every party here, that they're experts, and if they aren't experts,
well that's a much bigger problem. If these are people you don't trust
to get that type of information from, then this is a much bigger
problem. So, that's a bit about specs and requirements differences, and
I hope that when you look at your next project, you start with
requirements.

