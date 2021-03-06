Diogenes Mark 8
===

Diogenes is an intensely personalized scheduler for reminding you to talk to your friends. Personalized only to me, Howon Lee. Literally down to using my favorite way to refer to peeps in the plural, `peeps`. You can use it if you want, tho.

There are of course other folks who did analogous things, almost without exception more user-friendly (for example, [Monica](https://www.monicahq.com/)) but I wanted this specific thing.

Installing and Setup
---

`pip install diogenes8`

Requires python3.7. Only tested in Ubuntu, it will definitely only work in POSIX machines right now.

To enable email sending in recommendations, you also have to run

`dio setupemail`

And enter the information.

To setup the cronjob, do

`dio setupcron`

This will set it up in vixie cron, which seems to be the proper one in Ubuntu and OSX, I don't know about other distros.

Usage
---
On first usage, creates a `~/.diogenes` directory in home dir. Only a few subcommands right now. The person data only goes into a little `peep.json` file inside of a folder in `~/.diogenes` corresponding to the person. So if you need to do actual CRM things and take notes or something, there's a ... folder. Just shove it in there. Any files you'd like.

Here are the subcommands.

`dio add <name>`

Adds a new person to diogenes. Name has to be one word, so I do `snake_caps`. Addition is silently not strictly idempotent, because it replaces the person in the hash, I'm vacillating on whether that's good behavior.

`dio batchadd <file name>`

Adds peeps batchwise. --batchfile takes a csv with fields `name` _only_.

`dio recs`

Manually email the destination email which you previously set in `dio setupemail` the recommendations for today.

`dio dryrecs`

Manually give you the contents of the recommendations for today without emailing.

`dio setupemail`

Sets up the email settings for emailing. This just assumes an SMTP server already exists somewhere. To use webmail with 2fa, use an app password.

`dio setupcron`

Sets up the cronjob for automatic emailing. Uses the default vixiecron on ubuntu only: I don't know a way to do anacron without asking for root, and at that point you might as just manually setup cron by running something like:

```
sudo sh -c 'echo "#!/bin/bash -e
> sudo -H -u <your username> dio recs" >> /home/<your username>/.diogenes/diogenes.log 2>&1'
```

There's no anacron in OSX, you're supposed to use launchd for analogous functionality. I have no idea how to use launchd, so my recommendation is just use the vixiecron that comes with OSX.

Importing friends
---

I seriously recommend using pen and paper and taking an afternoon to go over your contacts list and only then making the csv, because at this point 4/5 your "friends" on Facebook are probably not actually going to be friends to a degree that you will actually be able to contact them. It was for me, a half-decade ago, so I suspect it got worse for folks.

Synchronization, Collaboration, and Backup
---

Why not just use git on the .diogenes folder? It's actually just all text all the time there.

I want to add more stuff onto this.
---

The actual place where the folks are stored, `~/.diogenes`, is a perfectly normal little bit of the filesystem. Each person is construed as a folder, so you can stick more stuff in there. Have fun. If you make something cool, do tell me.

Shouldn't you automate the actual contacting of people?
---

That's a terrible idea.

Why's it called Diogenes?
---

The most antisocial way to be social should be named after the most antisocial of the ancients.

Slack
---

I made a slack at diogenes8.slack.com. Email me if you want in.

Notes
---

The default schedule is to contact everyone 2x a year, reminding on an unpredictable but nonrandom (hash-based) schedule of days. Pretty obvious that the unpredictable schedule helps. There's a little ABC for creating your own schedule if you want.

Diogenes Mark 1 was just writing on some paper. I then lost the paper and realized it should probably be backed up.

Mark 2 was a web app which was generally a pain in the butt to janitor, as web apps do end up being. It was also based upon an entirely document-based (but Postgres) schema, meaning that there was no schema, so I got hit in the face with that, basically.

Mark 3 was a spreadsheet, which did fine but I was feeling the lack of scheduling apparatus a fair bit.

Mark 4 was a local postgres DB and small cronjob, no app. It was a surprising amount of work to execute the schema and janitor even the tiny DB (because I made the in-hindsight bad decision of putting it on RDS), and I wanted something more complicated than what a crontab could give me.

Mark 5 was a static site with JS, which turns out to be a bad idea if you're planning runtimes of months.

Mark 6 was again some paper, because I gave up. There was also a pretty big lacuna there.

Mark 7 was a SQLite local crud command line app. I then realized that I could just use fopen (the biggest SQLite competitor, as the SQLite folks would tell you).

You're looking at mark 8, the filesystem local crud command line app that I messed with the settings a bit and de-hardcoded a lot of stuff so I could publish. There were also a bunch of lacunae where I was working way too much to be a proper human being. But overall, this little long-running thing is the basis of how I quit facebook for the last half-decade or so.

The overall motivation is Granovetter's observation that weak links are most important, "The Strength of Weak Ties". But I believe the data better fits a renormalization group sort of picture of the actual use of weak ties. To the best of my knowledge, SOTA of community modelling is basically this sort of renormalization group flow picture (Kronecker graph, tensor methods), although it is pretty seldom that folks actually say renormalization group flow (Watts and Strogatz do, if I recall correctly, but I can't find a cite). Friends are a fractal phenomenon!

It remains an old contention of mine that many of the two-factor things that happen a lot in psychology are sort of doing a PCA on a fractal space and popping out the first two factors and calling it a day. But given that, you need to actually respect the illusion of a two-factor thing going on and don't put anyone in that you contact out of your own volition all the time. Weak links, basically.
