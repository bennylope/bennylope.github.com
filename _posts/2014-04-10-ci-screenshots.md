---
author: Ben
title: "Continuous Cross-browser Screenshots"
layout: post
permalink: /continuous-cross-browser-screenshots/
category: programming
redirect_from: /blog/continuous-cross-browser-screenshots/
published: true
categories: development
comments: true
canonical: https://wellfire.co/blog/continuous-cross-browser-screenshots/
teaser: >
    Trying to check changes on multiple browsers and multiple devices is hard. In
    the old days shops kept old computers lying around to test against different OS's and
    older browsers. A lot of that can be virtualized on your desktop now, but
    that's still kind of a pain in the tuchus. And adding in tablets and mobile
    phones just deepens the hole. Thankfully, there's a better way.
---

Trying to check changes on multiple browsers and multiple devices is hard. In
the old days shops kept old computers lying around to test against different OS's and
older browsers. A lot of that can be virtualized on your desktop now, but
that's still kind of a pain in the tuchus. And adding in tablets and mobile
phones doesn't make testing any easier. Thankfully, there's a better way.

### Virtualized browsers with BrowserStack

We use a service called [BrowserStack](http://www.browserstack.com/) for
cross browser testing. It's a little
slower and less convenient than running a browser directly on your computer,
but for running, say Internet Explorer on a Mac, it's a lifesaver. This is to
say nothing of multi OS and device support. We don't keep old phones around
just to test websites.

We started using live testing, allowing you to directly interact with the
website in question through the virtualized browser. But for a lot of QA work
what you really just want are screenshots to see how layouts behave in
different browsers or different dimensions. That's where we've made use of the
screenshot feature, generating screenshots for one URL across numerous browsers
at once.

![Sweet website](/images/lingcars.png)

### Shooting from the hip

That's fine and dandy but clicking on screens and filling out forms gets tedious fast.
[Screenshooter](http://github.com/bennylope/screenshooter/) is a little Ruby gem I
wrote last year that provides a convenient command line interface to
BrowserStack's screenshot API.

With a local `browsers.yaml` file and some credentials in either a user dotfile
or environment variables, you can request screenshots right from your project.

To start, you'll first want to list the available device, OS, and browser
combinations so you can build your selection.

{% highlight bash %}
screenshooter list
{% endhighlight %}

This simply prints out the direct hash of devices (this list continues quite a ways!).

{% highlight ruby %}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"3.6", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"4.0", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"5.0", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"6.0", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"7.0", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"8.0", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"9.0", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"10.0", :os_version=>"Mavericks"}
{:os=>"OS X", :browser=>"firefox", :device=>nil, :browser_version=>"11.0", :os_version=>"Mavericks"}
{% endhighlight %}

Pick the browsers you want and edit your `browsers.yaml` file to specify which
you want. We'll keep this simple and just check two versions of IE and and iOS device.

{% highlight yaml %}
url: http://www.example.com/default-url/
browsers:
    -
      browser: "Mobile Safari"
      os: ios
      os_version: "7.0"
      device: "iPhone 5S"
    -
      browser: ie
      browser_version: "10.0"
      os: Windows
      os_version: "7"
    -
      browser: ie
      browser_version: "11.0"
      os: Windows
      os_version: "7"
{% endhighlight %}

The file does need a default URL, but this can be overridden on the command line.

{% highlight bash %}
screenshooter browsers.yaml -u http://www.lingscars.com/
{% endhighlight %}

Screenshooter will request the screenshots and then return the URL for the
screenshot gallery while BrowserStack generates them.

{% highlight bash %}
[0:02]http://www.browserstack.com/screenshots/f3cd6276f3429641dd43d2cdc1eea5108b6faf3c
{% endhighlight %}

### CI: Robots in the sky

To complete the automation, we have [CircleCI](https://circleci.com/) kick off
the screenshot commands right after deployment. In this example, we have the CI service check
a few key pages on the staging site after
each deployment. The resulting screenshot URLs are then added to a file
in CircleCI's [artifacts folder](https://circleci.com/docs/build-artifacts).

The screenshot URLs text file is now available for review
against each build. Additionally in this example, we have the results
sent to a HipChat room so that the dev team can grab them more
conveniently.

Here's the deployment snippet of an example `circle.yml` file:

{% highlight yaml %}
deployment:
  staging:
    branch: master
    commands:
      - cap staging deploy
      - screenshooter shoot -u http://"${STAGING_USERNAME}":"${STAGING_PASSWORD}"@staging.example.com/ >> $CIRCLE_ARTIFACTS/screenshots.txt
      - screenshooter shoot -u http://"${STAGING_USERNAME}":"${STAGING_PASSWORD}"@staging.example.com/page1/ >> $CIRCLE_ARTIFACTS/screenshots.txt
      - screenshooter shoot -u http://"${STAGING_USERNAME}":"${STAGING_PASSWORD}"@staging.example.com/page2/ >> $CIRCLE_ARTIFACTS/screenshots.txt
      - screenshooter shoot -u http://"${STAGING_USERNAME}":"${STAGING_PASSWORD}"@staging.example.com/page3/ >> $CIRCLE_ARTIFACTS/screenshots.txt
      - >
        curl --data-urlencode room_id="${HIPCHAT_ROOM}" --data-urlencode "message_format=text"
        --data-urlencode "color=purple" --data-urlencode "from=BrowserStack"
        --data-urlencode "message=$(cat $CIRCLE_ARTIFACTS/screenshots.txt)"
        https://api.hipchat.com/v1/rooms/message?auth_token="${HIPCHAT_TOKEN}"
{% endhighlight %}

### QA's hard, let's build websites!

Not only does this save the time and hassle of going to generate the
screenshots, it ensures that they are generated for each new deployment. These
can be shared with a wider team and the client, and everyone can get back to
the business of building websites.
