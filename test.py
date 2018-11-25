import hypothesis as hp
import hypothesis.strategies as st
import hypothesis_fspaths as hy_fs
import dio
import fixtures
import pytest
import os

@st.composite def person_str(draw, name=st.text(), email=st.text(), salt=st.text()):
    return dio.Person(
            name=draw(name),
            email=draw(email),
            salt=draw(salt))

@st.composite
def dio_dir(draw, dirname=hy_fs.fspaths()):
    return dio.DioDir(dirname=draw(dirname))

@hp.given(person_str())
def test_person_init(peep):
    # assert not null
    assert peep

def test_person_file_encode_involution(peep):
    ##############
    ##############
    ##############
    pass

def test_person_folder_encode_involution(peep):
    ##############
    ##############
    ##############
    pass

def test_is_peep_dir_idempotence(peep):
    ##############
    ##############
    ##############
    pass

def test_get_all_idempotence(peep):
    ##############
    ##############
    ##############
    pass

# fs from pyfakefs

@hp.given(dio_dir=dio_dir())
def test_filesystem_creation(fs, dio_dir):
    """ tests idempotence of fs creation """
    dir_obj = dio.DioDir(dirname=dio_dir)
    dir_obj.create_if_not_exists()
    assert os.path.exists(dir_obj.dirname)
    dir_obj.create_if_not_exists()
    assert os.path.exists(dir_obj.dirname)

def test_recs_encoding_involution(recs):
    ##############
    ##############
    ##############
    pass

def test_add_person_idempotence(peep):
    ##############
    ##############
    ##############
    pass

def test_get_recs_idempotence():
    ##############
    ##############
    ##############
    pass

if __name__ == "__main__":
    pass
