---
title: Waking Sleeping Beauty
permalink: /waking-sleeping-beauty/
layout: post
published: true
date: 2015-05-20
teaser: >
    The Sleeping Beauty problem is a probability puzzle, or
    maybe an epistilmogy puzzle. Creating a defensible
    position depends on building an accurate model of the problem,
    and minor twists to the model have significant consequences
    for our assessment.
---

Enjoying some cookies with my wife and a colleague of hers a few weeks back, I was presented with a puzzle that he had taught in a class on puzzles and paradoxes called the Sleeping Beauty problem. The Sleeping Beauty problem is a probability problem, or perhaps an epistemology problem (are they much different?), and it stuck with me for a few days after our discussion. At first it seemed terribly obvious to me, and I spent a while trying to think about either why the answer might be otherwise or how to better motivate my intuition. I did this right up until I found the perfect example for justifying my response, which turned out to be the key to understanding why it was likely wrong.

### The problem

The problem as my wife's colleague Eric formulated it, is roughly as follows (any errors in setup are almost certainly my own).

You are to be a subject in a two-track, one-week experiment. At the start of both tracks on Sunday evening participants are put to sleep with a heavy sedative. Participants in the first track will be awoken every day and interviewed. After this interview they will be a given a two drug cocktail that induces perfect short-term amnesia and puts them back to sleep. There is no way for you to remember being woken up at any later point. This procedure will carry on Monday through Friday, and participants are finally awoken on Saturday.

Participants in the second track will be woken up for an interview and given the same two drug cocktail, but they will be woken up only once during the week, and left to sleep the remaining days.

The track in which you are placed is decided by a fair coin toss. Heads you end up in the first track to be woken up every day, tails you end up in the second track to be woken up only once. And of course you will not be told how the coin landed.

With this in mind, if you find yourself woken up for an interview, what is your belief about the likelihood that the coin landed heads up and you are in the first track versus the coin landing tails and finding yourself in the second track?

If this is the first time you've encountered this little puzzle feel free to take some time to think about it before reading on.

### My intuitive response

Even with the preface that there is wide disagreement about how to answer this problem, and by impressively smart people, my intuitive response was near instant. The coin almost certainly landed heads up, landing you in the first track. How anyone could think otherwise was beyond me.

The coin toss, I reasoned, is irrelevant, as it doesn't bound the problem space. In the combined possibilities of being woken up, of which there are six days, five of these are found in the first track. This seems like a pretty strong Bayesian prior. And on average you'd make a mint wagering on track A every time you're awoken.

### Intuition pumping

As it were my wife wasn't buying it. It still went against her intuition. She sympathized with the argument about the wager, but wasn't won over - it's not a repeated game, after all. Right, right, but we're talking about your priors here, and 5/6 awakenings take place in the first track. Surely we have 83% confidence that the coin landed heads!

The surest way to get someone to see your point of view in a problem like this is to find an analog problem that frames it slightly differently without violating the problem structure. This is not trivial, it turns out.

Every example I tried making up, all having to do with visiting space aliens for some reason, violated at least one aspect of the problem. Aliens drop you in an ocean somewhere, what's your belief that it's the Pacific and not the Mediterranean? (Putting aside any other knowledge you might have about the bodies of water, the stars, of that the latter is not an ocean). That's a nice way of showing how your priors influence your decision, but it's not an analog.

What else could represent this kind of decision? What about the classic marble problem? You have two bags, each with five marbles. One has five black marbles. The second has one black marble and four white marbles. If a marble is selected from a bag - which bag is not known to you - and the marble is black, what is the likelihood that the marble was selected from the first bag? 

That's simple, there's a 5/6 likelihood that it was from the first bag. 

### There are no white marbles

Even with this new understanding, I knew there must be some other perspective - after all, impressively smart and credentialed people disagree about this. So when I had the opportunity I ambushed Jonathan, our resident statistician at 804RVA, with the problem.

He thought about it for a little while and said that it was an interesting little puzzle. I explained my intuitive response to the problem and, why yes, you do have some pretty strong priors! And I shared the marble problem and how what a nice analog it is. Those are obvious priors, with the two bags.

But then he thought about it for a little while longer, looked at me and shook his head. "No, there are no white marbles."

Aside from being irked that my intuitive response was so off, this was a fascinating little insight. Little like the blasting cap on a load of TNT.

When you're picking out marbles from the bags, the question isn't whether you pick a marble out or not, it's which kind of marble you pick out. There's a sampling, picking a marble out of a bag, and an outcome, either a black marble or a white marble. In the Sleeping Beauty problem, there is no distinction between the sampling and the outcome. 

Given that you have a white marble, what is the probability that it was selected from the second bag? 100%. But you can never draw a day on which you're not woken up - it's not sampled, it's a non-event. There's a 100% chance of the event happening on any given day vs a 20% chance of the event happening on any given day. *But* given that you will only be woken up when the event occurs, it's 100% likely that you will be awake for the event on either track. If both bags have only black marbles, it's irrelevant how many are in one versus the other - your knowledge is still limited to the 50% probability of the coin toss.

To better illustrate this position, let's change the Sleeping Beauty problem up a little bit. The scenario is basically the same, including the two tracks, the fair coin toss, the amnesia inducing medicine. The difference is that in the second track you're only interviewed once but you're woken up every day. Okay, you're interviewed insofar as you're asked, what do you think the likelihood is that you'll be interviewed today? Then you're either interviewed or not, given the amnesia inducing drug, and put back to sleep.

The *event* of being interviewed only happens 1 out 5 times, but the sampling happens every day. This is equivalent to pulling the marbles out of a bag with 4 white marbles and 1 black marble. On any given day that you are woken up the likelihood that you will be interviewed is 1/5 in track two. In the original formulation of the problem, the likelihood that you would be interviewed upon waking up was 1/1.

### Probability is tricky

What is interesting is that quite often it's not the math that's tricky, but getting the model right. There's a lot of literature about how human intuition gets the models wrong, and it's not just in undergraduate problem sets. 

Nobody seems to be arguing about how to multiply 50% by 20% in the Sleeping Beauty problem, but about which of these numbers is relevant in any way. It's figuring out which of the "filters" matter, and in what order, rather than arithmetic that's the most difficult part.

### Elephants and funny perspectives

The second take away from this problem is what a difference a 'minor' insight can reveal. When we think we recognize a problem it's easy to take that preexisting template and apply it to the problem in front of us. It is difficult to mentally remove a problem template once its been applied.

The blind monk presented with only the elephant's leg mistakes it for a tree, and understandably so, because without seeing the whole, without seeing the connection, that is the closest similarity. There's also the case in which we see the shadow of a horse but without looking more closely mistake a zebra for a horse. Or see a great storefront and mistake just a panel for an entire building.

If it weren't for Jonathan's insight, I'd probably still be thinking about those bags with black _and_ white marbles.
