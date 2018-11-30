from .schedule_abc import ScheduleABC
from .default_schedule import DefaultSchedule
from .dio_dir import DioDir
from .person import Person
from .settings import Settings
from .three_times_schedule import ThreeTimesSchedule
from .utils import *
from typing import Optional, List, Dict
import datetime
import email
import smtplib
import functools

def get_recs(dio_dir: DioDir, schedule: ScheduleABC, date_to_rec: datetime.date) -> Optional[List[Person]]:
    if schedule.should_email_day(date_to_rec):
        should_contact_on_day = functools.partial(
            schedule.should_contact,
            date=date_to_rec
        )
        return list(filter(should_contact_on_day, Person.get_all(dio_dir)))
    else:
        return None

def recs_to_message(res: Optional[List[Person]], next_day: datetime.date) -> str:
    if res is None:
        return "Next emailing day is : {}".format(next_day)
    elif res == []:
        return "Emailing day, but no peeps today. Add more peeps."
    else:
        return "\n".join(
            [peep.name for peep in res]
        )

def send_message(contents: str, date: datetime.date, settings: Settings) -> None:
    msg_obj: email.message.EmailMessage = email.message.EmailMessage()
    msg_obj['From'] = settings.smtp_username
    msg_obj['To'] = settings.smtp_dest_email
    msg_obj['Subject'] = "Diogenes | {}".format(str(date))
    msg_obj.set_content(contents)
    with smtplib.SMTP(settings.smtp_url, settings.smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg_obj)

