import hypothesis as hp
import hypothesis.strategies as st
import hypothesis_fspaths as hy_fs
import dio
import utils
import datetime
import pytest
import pyfakefs
import os

# fs from pyfakefs

@st.composite
def person_st(draw, name=st.text(), salt=st.integers(min_value=1e30, max_value=9e30)):
    return dio.Person(
            name=draw(name),
            salt=str(draw(salt)))

@st.composite
def settings_st(draw, username=st.text(), password=st.text(), dest_email=st.text(), url=st.text(), port=st.integers(min_value=0)):
    return dio.Settings(
        smtp_username=draw(username),
        smtp_password=draw(password),
        smtp_dest_email=draw(dest_email),
        smtp_url=draw(url),
        smtp_port=draw(port))

@st.composite
def dio_dir_st(draw, dirname=hy_fs.fspaths()):
    return dio.DioDir(dirname=draw(dirname))

@st.composite
def sched_st(draw):
    return dio.DefaultSchedule()

@hp.given(peep=person_st())
def test_person_init(peep):
    # assert not null
    assert peep

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_person_file_encode_involution(fs, peep, dio_dir):
    dio_dir.create_if_not_exists()
    peep.save(dio_dir)
    dirname = peep.get_dir(dio_dir)
    filename = dio.Person.get_filename(dirname)
    new_peep = dio.Person.from_file(filename)
    assert peep == new_peep

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_person_folder_encode_involution(fs, peep, dio_dir):
    dio_dir.create_if_not_exists()
    peep.save(dio_dir)
    dirname = peep.get_dir(dio_dir)
    new_peep = dio.Person.from_dir(dirname)
    assert peep == new_peep

@hp.given(settings=settings_st(), dio_dir=dio_dir_st())
def test_settings_encode_involution(fs, settings, dio_dir):
    dio_dir.create_if_not_exists()
    settings.to_file(dio_dir.get_settings_filename())
    new_settings = dio.Settings.from_file(dio_dir.get_settings_filename())
    assert settings == new_settings

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_get_all_idempotence(fs, peep, dio_dir):
    peep.save(dio_dir)
    fst_res = dio.Person.get_all(dio_dir)
    snd_res = dio.Person.get_all(dio_dir)
    assert len(fst_res) > 0
    assert fst_res == snd_res

@hp.given(dio_dir=dio_dir_st())
def test_dio_dir_creation_idempotence(fs, dio_dir):
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)

@hp.given(sched=sched_st(), date=st.dates())
def test_schedule_should_email_day_idempotence(sched, date):
    fst_res = sched.should_email_day(date)
    snd_res = sched.should_email_day(date)
    assert fst_res == snd_res

@hp.given(peep=person_st(), sched=sched_st(), date=st.dates())
@hp.settings(
        suppress_health_check=(hp.HealthCheck.filter_too_much,),
        max_examples=200
)
def test_schedule_should_contact_idempotence(fs, peep, sched, date):
    hp.assume(sched.should_email_day(date))
    fst_res = sched.should_contact(peep, date)
    snd_res = sched.should_contact(peep, date)
    assert fst_res == snd_res

@hp.given(sched=sched_st(), date=st.dates())
def test_schedule_next_day_should_be_after_day(sched, date):
    next_day = sched.next_emailing_day(date)
    assert next_day >= date

@hp.given(sched=sched_st(), date=st.dates())
def test_fst_email_comparable_to_snd_email(sched, date):
    """ imbalance should be ~ Gaussian, so this is just verifying thin-tailedness """
    days_to_schedule = sched.set_of_days_emailed(date.year)
    fst, snd = dio.DefaultSchedule.split_emailed_set(days_to_schedule)
    assert abs(len(fst) - len(snd)) < 80

@hp.given(peep=person_st(), dio_dir=dio_dir_st(), sched=sched_st())
def test_person_contacted_exactly_twice_a_year(fs, peep, dio_dir, sched):
    peep.save(dio_dir)
    num_times_contacted = 0
    for curr_day in utils.days_in_year(2018):
        if sched.should_email_day(curr_day) and sched.should_contact(peep, curr_day):
            num_times_contacted += 1
    assert num_times_contacted == 2

@hp.given(sched=sched_st())
def test_schedule_should_have_days_contacted(sched):
    num_days_contacted = 0
    for curr_day in utils.days_in_year(2018):
        if sched.should_email_day(curr_day):
            num_days_contacted += 1
    assert num_days_contacted > 40

@hp.given(
        peeps=st.lists(person_st(), max_size=100, unique=True),
        dio_dir=dio_dir_st(),
        sched=sched_st(),
        date=st.dates())
def test_schedule_should_not_have_days_with_huge_boluses(fs, peeps, dio_dir, sched, date):
    """ going through a whole year takes too long... """
    for peep in peeps:
        peep.save(dio_dir)
    curr_recs = dio.get_recs(dio_dir, sched, date)
    if curr_recs is not None:
        assert len(curr_recs) < 10

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_add_person_idempotence(fs, peep, dio_dir):
    dio_dir.create_if_not_exists()
    peep.save(dio_dir)
    peep.save(dio_dir)
    dirname = peep.get_dir(dio_dir)
    new_peep = dio.Person.from_dir(dirname)
    assert peep == new_peep

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_remove_person_non_idempotence(fs, peep, dio_dir):
    dio_dir.create_if_not_exists()
    peep.save(dio_dir)
    peep.delete(dio_dir)
    with pytest.raises(Exception) as exc:
        peep.delete(dio_dir)
        assert "delete" in str(exc.value)

if __name__ == "__main__":
    raise Exception("use pytest")
