import pytest
from GEDCOM import parse, Individuals

parse('TR_Family_Tree.ged')

def test_Gregg():
    assert Individuals.get('@I12@').age != 49
    assert Individuals.get('@I12@').age == 33

def test_Tyler():
    assert Individuals.get('@I3@').age == 21
    assert Individuals.get('@I3@').age != 31

def test_Rebecca():
    assert Individuals.get('@I4@').age == 47
    assert Individuals.get('@I4@').age != 46

