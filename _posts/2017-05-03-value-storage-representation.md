---
title: "Data Representation "
permalink: /numeric-values-and-representation/
layout: post
category: programming
published: true
date: 2017-05-03 13:22:53
teaser: >
    When numeric representation formats differ from calculation
    formats, choosing the latter for storage simplifies maintenance and
    debugging.
---

How should you store the value of 5%? Or $10 in expenses?

These seemingly trivial little questions can cause development pain and allow errors to seep
into a program.

### Money

Let's start with money.

Monetary values are represented in all kinds of ways. One million dollars might
be represented as "$1M" or "1,000,000 USD" or "$1,000,000.00" Smaller numbers
can likewise be represented in different ways, and as these three examples show
its not just the currency symbols that affect this.

Hopefully your first thought is to store a number. Storing "$1M" might be
acceptable if you need some additional cached value, but the source of truth
should be a number. This makes different representation simple as well as allows
calculations.

But you probably already had a numeric format in mind.

That leaves floats and integers, right? Floats allow you to store data past the
decimal point and integers can be used for both whole number amounts and numbers
with fractional values by padding the stored amount, e.g. multiplying by 100. So
which is the better choice?

The punchline is neither. Use a decimal instance.

Float values are subject to unexpected rounding and imprecise results, which is
not acceptable for most financial calculations or representations. And while the
padded integer trick works, it requires not only that you enforce a specific
level of precision (using a coefficient of 100 you won't be able to represent
half cents) but that you always remember the conversion.

For Python users, use `decimal.Decimal`.

### Percentages

Surely percentages are simpler. 99.9% should be stored as `Decimal(99.9)`!

Not so fast! A percentage is a decimal value, a fraction of 100. Chances are
*pretty good* that if you're storing percentage values you're making some kind
of calculation with them. In this case you'll be transforming these values
everytime you make that calculation.

Instead, store the underlying value, that is `Decimal(0.999)`.

Yep, you're going to have to transform this when you represent it or store user
input. The difference between this conversion and the one mentioned with money
is that the former padded integer conversion involves converting to an
*unexpected format* whereas encountering a percetage value as a decimal is
expected. So you remove the unexpected conversion from all calculations and
add in understandable conversion to and from the user.

Store as a decimal, using the actual *percentage value*.

### Sign

This one has to be silly obvious. You store a number with whatever sign it has
in the calculation. Right?

Here there isn't a right or wrong answer, rather you should consider the
calculations you'll perform with the numbers (if any). For instance, it might
make sense to store an *expense* as a *negative number*. This would allow you to
simply sum expesnes and income values, for example, and get the result.
Of course computationally it's trivial to negate these if they're stored as
positive values. The question is, again, what is expected? If you find yourself
frequently or always negating a value for either calculations or
representations, it might make more sense to store with that sign.

### The commmon thread

In each case we're presented with a choice: modify the value for calculations or
for representation. For instance, if you need to use a threshold percentage
value, storing this as a percentage value, `0.78` instead of `78` means there's
fewer opportunities for confusion and hence errors when updating calculations.
This *does* mean that the value a user inputs and the value presented to a user
might need to be transformed. And this might even be more work. However the risk
to code maintenance and correctness is greater.

A rule of thumb I use is how much sense would it make seeing this value in a
database and then performing calculations in SQL with it. Are you dividing
numbers by some arbitrary coefficient to get something sensible to add? That's a
sign you probably have a representation format where you want a storage format.

