import hypothesis as hp
import hypothesis.strategies as st
import dio
import fixtures
import pytest

@st.composite
def person_str(draw, name=st.text(), email=st.text(), salt=st.text()):
    return dio.Person(
            name=draw(name),
            email=draw(email),
            salt=draw(salt))

@hp.given(person_str())
def test_person(s):
    assert s

### Person strategy
### Email strategy
### Settings strategy

if __name__ == "__main__":
    pass
