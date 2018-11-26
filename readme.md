Diogenes Mark 8
===

Diogenes is an intensely personalized command line only CRM for friends. Personalized only to me, Howon Lee. Literally down to using my favorite way to refer to peeps in the plural, `peeps`.

Installing and Setup
---

Overall goal is to create pip installable dealio. Not yet, tho.

Set email url, password with envvars

You have to set:

```
DIO_SMTP_URL
DIO_SMTP_PORT
DIO_SMTP_USERNAME
DIO_SMTP_PASSWORD
DIO_DEST_EMAIL
```

Use an app password for the `DIO_SMTP_PASSWORD`

What I use for daemonization is supervisord. Cat the conf file to /etc/supervisor/conf.d/recommenderd.conf

Usage
---
On first usage, creates a `~/.diogenes` directory in home dir. Only a few subcommands right now.

```
dio.py add --name <name> --email <email>
```

Adds a new person to diogenes. This ends up being a folder in `~/.diogenes` and a little peep.json file. The rest of the folder is yours to futz around with. Addition is silently not strictly idempotent, because it replaces the person in the hash, I'm vacillating on whether that's good behavior.

```
dio.py batchadd --batchfile <file name>
```

Adds peeps batchwise. --batchfile takes a csv with fields `name` and `email` _only_. This ends up being a bunch of folders in `~/.diogenes` and a bunch of little peep.json files. The rest of the folders are yours to futz around with. Addition is silently not strictly idempotent, because it replaces the person in the hash, I'm vacillating on whether that's good behavior.

```
dio.py recs
```

Manually give the recommendations for today, without emailing. Will give you the contents of what the daemon will email you, but just use the daemon.

Importing friends
---

I seriously recommend using pen and paper and taking an afternoon to go over your contacts list, because at this point 4/5 your "friends" on Facebook are probably not actually going to be friends to a degree that you will actually be able to contact them.

Shouldn't you automate the actual contacting of people?
---

No.

Notes
---

Default schedule is to contact everyone 2x a year, reminding on an unpredictable but nonrandom (hash-based) schedule of days. There's a little ABC for creating your own schedule if you want.

Diogenes mark 1 was some paper

mark 2 was a web app (that I took down, because it was getting annoying)

mark 3 was a spreadsheet

mark 4 was a local postgres DB

mark 5 was a static site with JS that I took down

mark 6 was some paper

mark 7 was a SQLite local crud command line app, threw that away

You're looking at mark 8, the filesystem local crud command line app that I messed with envvars a bit and de-hardcoded a lot of stuff so I could publish

Motivation is Granovetter's observation that weak links are most important, "The Strength of Weak Ties". But I believe the data better fits a renormalization group sort of picture of the actual use of weak ties. To the best of my knowledge, SOTA of community modelling is basically this sort of renormalization group flow picture (Kronecker graph, tensor methods), although it is pretty seldom that folks actually say renormalization group flow (Watts and Strogatz do, if I recall correctly, but I can't find a cite). Friends are a fractal phenomenon!

It remains an old contention of mine that many of the two-factor things that happen a lot in psychology are sort of doing a PCA on a fractal space and popping out the first two factors and calling it a day. But given that, you need to actually respect the illusion of a two-factor thing going on and don't put anyone in that you contact out of your own volition all the time. Weak links, basically.
