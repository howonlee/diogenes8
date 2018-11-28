Diogenes Mark 8
===

Diogenes is an intensely personalized command-line-only CRM for friends. Personalized only to me, Howon Lee. Literally down to using my favorite way to refer to peeps in the plural, `peeps`.

There are of course other folks who did analogous things, almost without exception more user-friendly (for example, [Monica](https://www.monicahq.com/)) but I wanted this specific thing.

Installing and Setup
---

Overall goal is to create pip installable dealio. Not yet, tho. Currently, I'm just cloning the git repo and running the python scripts. There is also a trivial daemon.

Set email url, password with envvars. Tested on Ubuntu only right now.

You have to set:

```
DIO_SMTP_URL
DIO_SMTP_PORT
DIO_SMTP_USERNAME
DIO_SMTP_PASSWORD
DIO_DEST_EMAIL
```

Use an app password for the `DIO_SMTP_PASSWORD`

Also need to put these into the supervisord configs if daemonizing.


Usage
---
On first usage, creates a `~/.diogenes` directory in home dir. Only a few subcommands right now. The person data only goes into a little `peep.json` file inside of a folder in `~/.diogenes` corresponding to the person. So if you need to do actual CRM things and take notes or something, there's a ... folder. Just shove it in there. Any files you'd like.

What I use for daemonization is supervisord. Conf file included is a valid jinja2 template. Fill the members of template out and cat the conf file to `/etc/supervisor/conf.d/recommenderd.conf`.

Here are the subcommands.

```
dio.py add --name <name>
```

Adds a new person to diogenes. Addition is silently not strictly idempotent, because it replaces the person in the hash, I'm vacillating on whether that's good behavior.

```
dio.py batchadd --batchfile <file name>
```

Adds peeps batchwise. --batchfile takes a csv with fields `name` _only_.

```
dio.py recs
```

Manually give the recommendations for today, without emailing. Will give you the contents of what the daemon will email you, but just use the daemon.

Importing friends
---

I seriously recommend using pen and paper and taking an afternoon to go over your contacts list, because at this point 4/5 your "friends" on Facebook are probably not actually going to be friends to a degree that you will actually be able to contact them.

Synchronization and Backup
---

Why not just use git on the .diogenes folder? It's actually just all text all the time there.

I want to add more stuff onto this.
---

The actual place where the folks are stored, `~/.diogenes`, is a perfectly normal little bit of the filesystem. Each person is construed as a folder, so you can stick more stuff in there. Have fun.

Shouldn't you automate the actual contacting of people?
---

That's a terrible idea.

Notes
---

The default schedule is to contact everyone 2x a year, reminding on an unpredictable but nonrandom (hash-based) schedule of days. Pretty obvious that the unpredictable schedule helps. There's a little ABC for creating your own schedule if you want.

Diogenes Mark 1 was just writing on some paper. I then lost the paper and realized it should probably be backed up.

Mark 2 was a web app which was generally a pain in the butt to janitor, as web apps do end up being. It was also based upon an entirely document-based (but Postgres) schema, meaning that there was no schema, so I got hit in the face with that, basically.

Mark 3 was a spreadsheet, which did fine but I was feeling the lack of scheduling apparatus a fair bit.

Mark 4 was a local postgres DB and small cronjob, no app. It was a surprising amount of work to execute the schema and janitor even the tiny DB (because I made the in-hindsight bad decision of putting it on RDS), and I wanted something more complicated than what a crontab could give me.

Mark 5 was a static site with JS, which turns out to be a bad idea if you're planning runtimes of months.

Mark 6 was again some paper, because I gave up. There was also a pretty big lacuna there.

Mark 7 was a SQLite local crud command line app. I then realized that I could just use fopen (the biggest SQLite competitor, as those devs would tell you).

You're looking at mark 8, the filesystem local crud command line app that I messed with envvars a bit and de-hardcoded a lot of stuff so I could publish. There were also a bunch of lacunae where I was working way too much to be a proper human being. But overall, this little long-running thing is the basis of how I quit facebook for the last half-decade or so.

The overall motivation is Granovetter's observation that weak links are most important, "The Strength of Weak Ties". But I believe the data better fits a renormalization group sort of picture of the actual use of weak ties. To the best of my knowledge, SOTA of community modelling is basically this sort of renormalization group flow picture (Kronecker graph, tensor methods), although it is pretty seldom that folks actually say renormalization group flow (Watts and Strogatz do, if I recall correctly, but I can't find a cite). Friends are a fractal phenomenon!

It remains an old contention of mine that many of the two-factor things that happen a lot in psychology are sort of doing a PCA on a fractal space and popping out the first two factors and calling it a day. But given that, you need to actually respect the illusion of a two-factor thing going on and don't put anyone in that you contact out of your own volition all the time. Weak links, basically.
