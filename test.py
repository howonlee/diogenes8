import hypothesis as hp
import hypothesis.strategies as st
import hypothesis_fspaths as hy_fs
import dio
import pytest
import pyfakefs
import os

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
    peep.create(dio_dir)
    dirname = peep.get_dir(dio_dir)
    filename = dio.Person.get_filename(dirname)
    new_peep = dio.Person.from_file(filename)
    assert peep == new_peep

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_person_folder_encode_involution(fs, peep, dio_dir):
    dio_dir.create_if_not_exists()
    peep.create(dio_dir)
    dirname = peep.get_dir(dio_dir)
    new_peep = dio.Person.from_dir(dirname)
    assert peep == new_peep

@hp.given(peep=person_st())
def test_is_peep_dir_idempotence(peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_st())
def test_get_all_idempotence(peep):
    ##############
    ##############
    ##############
    pass

# fs from pyfakefs

@hp.given(dio_dir=dio_dir_st())
def test_dio_dir_creation_idempotence(fs, dio_dir):
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)
    dio_dir.create_if_not_exists()
    assert os.path.exists(dio_dir.dirname)

@hp.given(sched=sched_st())
def test_schedule_should_email_day_idempotence(sched):
    ##############
    ##############
    ##############
    pass

@hp.given(sched=sched_st())
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

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_add_person_idempotence(fs, peep, dio_dir):
    dio_dir.create_if_not_exists()
    peep.create(dio_dir)
    peep.create(dio_dir)
    dirname = peep.get_dir(dio_dir)
    new_peep = dio.Person.from_dir(dirname)
    assert peep == new_peep

@hp.given(peep=person_st(), dio_dir=dio_dir_st())
def test_remove_person_idempotence(fs, peep, dio_dir):
    dio_dir.create_if_not_exists()
    peep.create(dio_dir)
    peep.remove(dio_dir)
    with pytest.raises(Exception) as exc:
        peep.remove(dio_dir)
        assert "remove" in str(exc.value)

@hp.given(peep=person_st())
def test_add_person_associativity(peep):
    ##############
    ##############
    ##############
    pass

@hp.given(peep=person_st())
def test_peep_state_machine(peep):
    ##############
    ##############
    ##############
    pass

if __name__ == "__main__":
    pass
