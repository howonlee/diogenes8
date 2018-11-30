#!/usr/bin/env python3.7
from __future__ import annotations
import functools
import csv
import random
import sys
import email
import smtplib
import argparse
import datetime
import crontab
import click
from dio import *
from typing import Optional, Any, Dict, List

@click.group()
def cli():
    pass

@cli.command()
@click.argument("name", required=True)
def add(name):
    """
    Adds a new person to diogenes.
    
    Given one name twice, current behavior is replacing the salt corresponding to the name
    """
    dio_dir: DioDir = DioDir()
    new_peep: Person = Person(name=name)
    new_peep.save(dio_dir)
    click.echo("New person with name {} added".format(name))

@cli.command()
@click.argument("batch_file_name", required=True)
def batchadd(batch_file_name):
    """
    Adds a batch of peeps to diogenes.

    Takes a csv with one field only, field name is `name`
    """
    click.echo("Processing batch file...")
    dio_dir: DioDir = DioDir()
    with open(batch_file_name, "r") as batch_file:
        reader = csv.DictReader(batch_file, fieldnames=["name"])
        for row in reader:
            # if you don't do this they all have the same salt
            new_rand: str = str(random.randint(int(1e30), int(9e30)))
            new_peep: Person = Person(name=row["name"], salt=new_rand)
            new_peep.save(dio_dir)
    click.echo("Finished processing batch file...")

@cli.command()
def dryrecs():
    """
    Gives you the recommendations for today without emailing them
    """
    click.echo("Recommendations, not emailed: ")
    dio_dir: DioDir = DioDir()
    sched: ScheduleABC = DefaultSchedule()
    today: datetime.date = datetime.datetime.now().date()
    res: Optional[List[Person]] = get_recs(dio_dir, sched, today)
    next_day: datetime.date = sched.next_emailing_day(today)
    click.echo(recs_to_message(res, next_day))

@cli.command()
def recs():
    """
    Emails the destination email the recommendations for today
    """
    click.echo("Emailing recommendations to destination...")
    dio_dir: DioDir = DioDir()
    sched: ScheduleABC = DefaultSchedule()
    today: datetime.date = datetime.datetime.now().date()
    res: Optional[List[Person]] = get_recs(dio_dir, sched, today)
    next_day: datetime.date = sched.next_emailing_day(today)
    message: str = recs_to_message(res, next_day)
    settings: Optional[Settings] = dio_dir.get_settings()
    assert settings is not None, "Have to setup diogenes to get emails. Run `dio setupemail`"
    send_message(message, today, settings)
    click.echo("Recommendations emailed!")

@cli.command()
def setupemail():
    """
    Sets up the email for diogenes
    """
    dio_dir: DioDir = DioDir()
    dio_dir.set_settings_interactive()
    click.echo("Setup complete. To setup the diogenes cronjob, run `dio setupcron`")

@cli.command()
def setupcron():
    """
    Sets up the cronjob for diogenes. Run `dio setupemail` before this one.
    Sets up only up to one cronjob per user. Sets cronjob for this user.
    """
    click.echo("Note that you should have run `dio setupemail` before this, or it will error out every time")
    curr_cron = crontab.CronTab(user=True)
    if len(list(curr_cron.find_comment("diogenes8"))) > 0:
        pass # do nothing
    else:
        job = curr_cron.new(command="dio recs", comment="diogenes8")
        job.hour.on(15)
        curr_cron.write_to_user(user=True)

if __name__ == "__main__":
    cli()
