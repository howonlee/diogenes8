import hypothesis as hp
import hypothesis.strategies as st
import hypothesis_fspaths as hy_fs
import dio
import pytest
import os

@st.composite
def person_str(draw, name=st.text(), email=st.text(), salt=st.text()):
    return dio.Person(
            name=draw(name),
            email=draw(email),
            salt=draw(salt))

@st.composite
def dio_dir(draw, dirname=hy_fs.fspaths()):
    return dio.DioDir(dirname=draw(dirname))

@st.composite
def sched_str(draw):
    return dio.DefaultSchedule()

@st.composite
def recs_str(draw):
    return dio.Recs(people=st.lists(person_str()))

@hp.given(peep=person_str())
def test_person_init(peep):
    # assert not null
    assert peep

@hp.given(peep=person_str())
def test_person_file_encode_involution(fs, peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_str())
def test_person_folder_encode_involution(peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_str())
def test_is_peep_dir_idempotence(peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_str())
def test_get_all_idempotence(peep):
    ##############
    ##############
    ##############
    pass

# fs from pyfakefs

@hp.given(dio_dir=dio_dir())
def test_dio_dir_creation_idempotence(fs, dio_dir):
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)

@hp.given(recs=recs_str())
def test_recs_encoding_involution(recs):
    ##############
    ##############
    ##############
    pass

@hp.given(sched=sched_str())
def test_schedule_should_email_day_idempotence(sched):
    ##############
    ##############
    ##############
    pass

@hp.given(sched=sched_str())
def test_schedule_should_contact_idempotence(sched):
    ##############
    ##############
    ##############
    pass

def test_get_recs_idempotence():
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_str())
def test_add_person_idempotence(peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_str())
def test_add_person_associativity(peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_str())
def test_remove_person_idempotence(peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_str())
def test_peep_state_machine(peep):
    ##############
    ##############
    ##############
    pass

if __name__ == "__main__":
    pass
