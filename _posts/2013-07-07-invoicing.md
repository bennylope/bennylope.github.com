---
published: true
title: "Invoicing clients: a guide for web developers"
layout: post
permalink: /invoicing-for-web-developers/
category: business
redirect_from: /2013/invoicing-for-web-developers/
soHelpful: true
comments: true
---

On the new Django Discussions forum someone raised [a question about time tracking](http://djangodiscussions.com/t/how-to-invoice-clients/83) which led to a discussion about invoicing. I thought I'd include here and expand on what I wrote in the hopes that maybe it would allay any confusion for other development shops and even customers who are new to development.

### The nuts-and-bolts overview

Timesheets and invoices are all managed through Harvest. Invoices are
sent out with net-15 terms and an automatic reminder is created for late

invoices through [Harvest](http://try.hrv.st/5ahy) (referral
link). Additionally we have
[Zencash](http://www.zencash.com/) integrated with Harvest so that when
an invoice is sent via email a hard copy is mailed as well. We also have
reminder postcards and thank you postcards configured to be sent out
automatically for overdue invoices and paid invoices, respectively.

Now let's break this down.

### Invoice management

The very first invoicing service we used was through the online services collection from our bank. As you would imagine it was terrible. The interface was rather poor and customers complained about the complexity of trying to pay online.

**When a customer complains that it's not easy enough to give you money, you should listen.**

We then briefly tried PayPal. Sure we could send invoices online and allow clients to pay electronically, but it just didn't fit well. We didn't want to encourage clients to pay via PayPal (and thus lose money to fees) and there were additional features we wanted, like reminders. Not to mention that something about using PayPal as our primary invoicing system just felt like it was sending the wrong message. You can use PayPal for any kind of service, but for many clients PayPal is what you use for buying and selling baubles on eBay. Not the association we want.

Of course there was always QuickBooks right in front of us. We did and still do manage the authoritative copy of our books in QuickBooks but only because we have to. This piece of software deserves its own blog post, but suffice to say using a desktop application for invoicing means all your invoices are managed in one location accessible only from that computer. We did not want one person to be a total bottle neck for invoicing.

Eventually we landed with [Blinksale](http://www.blinksale.com/) and used it quite happily for a couple years. We could send professional looking invoices with automatic client reminders and even provide a PayPal link for clients to inclined to pay that way. However once we started to outgrow Basecamp's time tracking functionality (now Basecamp classic) we had to start looking for something that better integrated time tracking and invoices, which is how we landed with Harvest.

Most of our work is not billed hourly, but enough is that we want to ensure that it's easy to get right. Coupled with my post consulting hatred of filing time sheets ("What billing code did *that* quarter hour fit into?") we wanted it to be dead easy. So time tracking can either be done via a desktop application as you work or through the Zendesk interface for customer tickets. It's then simple to run reports to ensure that we've captured hours accurately and to tie them to projects and even individual tasks (like tickets).

### Billing terms

As I noted, we bill using net-15 terms, which means the invoice must be paid within 15 days of the invoice date. I suspect that net-30 terms are closer to the norm for most firms in our line of work, but having listened to the laments of entrepreneurs suffering late and unpaid invoices, I'm happy sticking with net-15.

The thing about invoices or bills of any kind is that people, and businesses by extension, have a tendency to put them off. Sending money *out* of the business is not a high priority item. And like deadlines, Parkinson's Law applies. If a client is going to pay an invoice a week late, often they're going to pay it a week late whether it's due in 15 days of 45. 

In fact, very large businesses, like those that build big defense systems, may demand longer terms from vendors and then pay those late. We don't work with customers like that.

We do have a late fee policy but in practice we do not have to apply this. Most of our customers pay pretty promptly without carrot or stick. If a client mentions they have the invoice but are awaiting payment from their own clients or that they need a couple extra weeks because of a recent capital expenditure, that typically isn't a problem.

*If you have persistent problems with clients paying late, no invoicing system or change to your terms will alone fix things. The problem lies either in the client relationship or with the client.*

### Payment options

The importance of providing an electronic payment option is directly related to your invoicing volume and inversely related to your typical invoice value. Business customers don't mind writing a $15,000 check. Ask them to start submitting checks for $50 on a semi-regular basis and even an intern may grumble, "Why?" Handling small checks is annoying on the receiving end too.

Let me say this - I am totally willing to stop by the post office on the way back from the coffee shop to pick up checks. This is usually worth the hundreds of dollars in payment processing fees saved.

But what's most important about electronic payment is that it's available for customers who prefer to pay that way. Now when we send out invoices we offer the option for customers to pay with credit card via Stripe. I might complain that it's more costly than PayPal e-check, but I can count on one hand the number of invoices ever paid that way.

### Follow through and touch points

Since then we've added  to the mix for Zencash mailing hard copies of invoices. It sounds absurd, a firm grounded in the web mailing off *paper*. But it turns out the paper invoices are helpful for some clients, as its something they can hand to accounts payable. It's another non-intrusive touchpoint for reminding clients that they have an invoice.

![Zencash thank you card](/images/zencash-thank-you.png)

More important, or so we like to think, is the reminder and thank you cards. While it's true that one client complained about getting the thank you cards ("We know we paid you!") most appreciate it. Another client went out of her way to point out we were the only vendor they'd received a thank you note from. It's just a small post card with a tiny URL link to a feedback form.

### Line item by line item

I earlier alluded to reporting time against Zendesk tickets. This is helpful for internal tracking but it's also something we use for reporting line items on detailed maintenance invoices.

![Detailed invoice with line items](/images/invoice-detailed-line-items.png)

**But maintenance invoices are the only invoices subject to level of detail.**

This is not the blog post to discuss the difference between hourly and flat rate project pricing, but these pricing strategies are relevant to the invoice. We use both flat rate (most projects) and hourly pricing for projects, but even for hourly projects break down invoice line items only as far as the category of work (e.g. development, project management), if that to that degree.

Under a maintenance contract we need to show where work was applied by request. In a design and build project the project goal is the defined request, so this isn't necessary. More importantly, line item reporting is distracting. Even when billing by the hour you should really be selling something different than hours: your business's expertise.

Line item by line item invoices reduce your business to a shop selling hours of labor rather than expertise. Don't commoditize your business.


