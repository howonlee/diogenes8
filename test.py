import hypothesis as hp
import hypothesis.strategies as st
import hypothesis_fspaths as hy_fs
import dio
import datetime
import pytest
import pyfakefs
import os

# fs from pyfakefs

@st.composite
def person_st(draw, name=st.text(), email=st.text(), salt=st.text()):
    return dio.Person(
            name=draw(name),
            email=draw(email),
            salt=draw(salt))

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

@hp.given(peep=person_st(), dio_dir=dio_dir_st(), dirname=hy_fs.fspaths())
def test_is_peep_dir_idempotence(fs, peep, dio_dir, dirname):
    fst_res = dio.Person.is_peep_dir(dirname)
    snd_res = dio.Person.is_peep_dir(dirname)
    assert fst_res == snd_res
    thd_res = dio.Person.is_peep_dir(peep.get_dir(dio_dir))
    fth_res = dio.Person.is_peep_dir(peep.get_dir(dio_dir))
    assert thd_res == fth_res

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_get_all_idempotence(fs, peep, dio_dir):
    peep.save(dio_dir)
    fst_res = dio.Person.get_all(dio_dir)
    snd_res = dio.Person.get_all(dio_dir)
    assert fst_res == snd_res

@hp.given(dio_dir=dio_dir_st())
def test_dio_dir_creation_idempotence(fs, dio_dir):
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)

@hp.given(sched=sched_st(), dt=st.datetimes())
def test_schedule_should_email_day_idempotence(sched, dt):
    fst_res = sched.should_email_day(dt)
    snd_res = sched.should_email_day(dt)
    assert fst_res == snd_res

@hp.given(peep=person_st(), sched=sched_st(), dt=st.datetimes())
@hp.settings(
        suppress_health_check=(hp.HealthCheck.filter_too_much,),
        max_examples=200
)
def test_schedule_should_contact_idempotence(fs, peep, sched, dt):
    hp.assume(sched.should_email_day(dt))
    fst_res = sched.should_contact(peep, dt)
    snd_res = sched.should_contact(peep, dt)
    assert fst_res == snd_res

@hp.given(sched=sched_st(), dt=st.datetimes())
def test_schedule_next_day_should_be_after_day(sched, dt):
    next_day = sched.next_emailing_day(dt)
    assert next_day >= dt

@hp.given(sched=sched_st(), dt=st.datetimes())
def test_fst_email_comparable_to_snd_email(sched, dt):
    """ imbalance should be ~ Gaussian, so this is just verifying thin-tailedness """
    days_to_schedule = sched.set_of_days_emailed(dt.year)
    fst, snd = dio.DefaultSchedule.split_emailed_set(days_to_schedule)
    assert abs(len(fst) - len(snd)) < 40

@hp.given(peep=person_st(), dio_dir=dio_dir_st(), sched=sched_st())
def test_person_contacted_exactly_twice_a_year(fs, peep, dio_dir, sched):
    peep.save(dio_dir)
    first_day = datetime.datetime(2018, 1, 1)
    num_times_contacted = 0
    for curr_day in range(365):
        curr_dt = first_day + datetime.timedelta(days=curr_day)
        if sched.should_email_day(curr_dt) and sched.should_contact(peep, curr_dt):
            num_times_contacted += 1
    assert num_times_contacted == 2

@hp.given(sched=sched_st())
def test_schedule_should_have_days_contacted(sched):
    num_days_contacted = 0
    first_day = datetime.datetime(2018, 1, 1)
    for curr_day in range(365):
        curr_dt = first_day + datetime.timedelta(days=curr_day)
        if sched.should_email_day(curr_dt):
            num_days_contacted += 1
    assert num_days_contacted > 40

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
