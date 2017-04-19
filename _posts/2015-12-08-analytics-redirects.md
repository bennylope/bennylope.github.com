---
title: "When the numbers don't make sense: Google Analytics tracking issues"
permalink: /google-analytics-tracking-mismatches/
category: programming
layout: post
published: true
date: 2015-12-08
teaser: >
    A couple of analytics head scratchers and simple solutions.
---

While most of my work with my clients is related to building or fixing
software, I often find myself helping them solve other related business
problems. Frequently enough this includes data analysis, and with
marketing teams that means Google Analtyics.

Here are a few that have come up recently that you may have struggled
with, too.

## Why does this page have weird referrals?

The client's problem was that in a marketing system with numerous
microsites for their own customers, they were seeing lots of referrals
to customer X's microsite that were ostensibly from customer Y's
independently hosted website. There were no links on customer Y's
website to customer X's microsite, so where was this data showing up?

The answer comes from two facts:

- The microsites are hosted on a directory-like marketing platform, so
  you can navigate throughout the site to other customer microsites (based
  on geography or business type)
- Referrals are related to a session and not a specific page visit

The second is the key here. People were visiting customer Y's website,
clicking through to customer Y's microsite, and then navigating to
another customer X's microsite. Their referral path started with
customer Y's website, so that will show up as the referral for visits on
other pages.

## How do we track LinkedIn ad campaign variants?

Several URLs are being shared using ad variations, there's no clear way
to track what traffic on a shared URL is coming from the ad itself.
Using redirects doesn't help because the redirect is not tracked as a
referrer. Further, it's a small hassle to set up.

### Google campaign tracking

The solution is to provide links with Google campaign parameters
(provided by the Google URL builder tool). By tracking the (1)
overarching campaign, (2) ad source (e.g. LinkedIn), and (3) specific ad
variant in the utm\_ parameters (utm\_campagin, utm\_source, etc) the
traffic to a given landing page can be broken down by unique source.

### Viewing the data

The best way to view this data is by looking at the Landing Pages (under
Behavior and then Site Content), choosing a landing page, and then
modifying the dimensions. You can use a primary and secondary dimension,
so once you're looking at the data for a specific landing page you can
select "Campaign" as the primary dimension and "Ad Content" as the
secondary dimension, for example. Ad Content will show the value of
utm\_content which is where ad variants would be named.

You can't make Ad related dimensions the primary dimension, however, so
you'll need to start with Campaign or Source.

A short aside about using landing pages vs. "all pages": the campaign
parameters for someone's browser session on the site are persistent. So
if I click on an ad with campaign "fall2015" that will attributed to my
landing page and also each additional page I click on. This is why using
the landing page to identify clicks from ads is important. I could click
on an ad and navigate to another page that is the target of a different
ad. If you look at 'All Pages' you'll see my ad content tracked for that
other page, even though its targeted by a different ad. Google Analytics
is noting that a visitor on this page came to the site from the first ad
campaign, regardless of how they got to the page. Using Landing Pages
should isolate this to just site entry.
