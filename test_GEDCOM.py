import pytest
from GEDCOM import calculate_age

def test_Gregg():
    assert calculate_age('12 NOV 1972', '2 JUL 2006') == 33

def test_Tyler():
    assert calculate_age('16 AUG 2001', 'N/A') == 21

def test_Rebecca():
    assert calculate_age('21 JUL 1975', 'N/A') == 47

def test_James():
    assert calculate_age('15 DEC 1929', '29 JAN 2010') == 80

def test_Chase():
    assert calculate_age('23 JUL 2008', 'N/A') == 14