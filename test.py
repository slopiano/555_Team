import unittest

from GEDCOM import (allMalesinFamilyLastName, birthBeforeDeath, birthBeforeMarriage, birthOutOfWedlock, checkUniqueIndividualIDs, listDeceased, siblingMarriage, uniqueNameAndBirthdays,
                    checkCorrespondingEntries,
                    listLivingMarried,
                    showBorn30DaysAgo,
                    showDied30DaysAgo,
                    calculate_age,
                    checkUniqueFamilyIDs,
                    checkUniqueFamilyNames,
                    listDeceased,
                    neverMarriedOver30,
                    checkSpouseAndMarriageDate,
                    is_less_than_150_years,
                    validate_life_events,
                    listMulitpleBirths,
                    birthBeforeDeathOfParents,
                    divorceBeforeDeathOfSpouse,
                    noMoreThan5Births)

from utils import thirty_day_difference, diff_month, is_not_none

from Person import Person
from Family import Family


class TestForErrors(unittest.TestCase):

    def test_listLessThanOneIndWithSameBDayAndName_0(self):
        # test with empty data
        dummy_data = {}
        res = uniqueNameAndBirthdays(dummy_data)
        self.assertEqual(res, 1)

    def test_listLessThanOneIndWithSameBDayAndName_1(self):
        # test with same names and same birthdays
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
        }
        res = uniqueNameAndBirthdays(dummy_data)
        self.assertEqual(res, 1)

    def test_listLessThanOneIndWithSameBDayAndName_2(self):
        # test with different names and same birthdays
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "BSD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
        }
        res = uniqueNameAndBirthdays(dummy_data)
        self.assertEqual(res, 0)

    def test_listLessThanOneIndWithSameBDayAndName_3(self):
        # test with different names and different birthdays
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "BSD", 22, "M", "01-FEB-2001", True, "N\A", "N\A", "N\A"),
        }
        res = uniqueNameAndBirthdays(dummy_data)
        self.assertEqual(res, 0)

    def test_listLessThanOneIndWithSameBDayAndName_4(self):
        # test with same names and different birthdays
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "ASD", 22, "M", "01-FEB-2001", True, "N\A", "N\A", "N\A"),
        }
        res = uniqueNameAndBirthdays(dummy_data)
        self.assertEqual(res, 0)

    def test_check_corresponding_entries(self):
        self.assertTrue(checkCorrespondingEntries())

    def test_living_and_married(self):
        self.assertEqual(listLivingMarried(), 0)

    def test_list_recent_births(self):
        self.assertEqual(showBorn30DaysAgo(), 0)

    def test_calculate_age(self):
        self.assertEqual(calculate_age('12 NOV 1972', '2 JUL 2006'), 33)
        self.assertEqual(calculate_age('16 AUG 2001', 'N/A'), 21)
        self.assertEqual(calculate_age('21 JUL 1975', 'N/A'), 47)
        self.assertEqual(calculate_age('15 DEC 1929', '29 JAN 2010'), 80)
        self.assertEqual(calculate_age('23 JUL 2008', 'N/A'), 14)

    def test_checkUniqueIndivIDs(self):
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "BSD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
        }
        self.assertFalse(checkUniqueIndividualIDs())

    def test_checkUniqueFamilyIDs(self):
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "BSD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
        }
        self.assertFalse(checkUniqueFamilyIDs())

    def test_showDied30DaysAgo(self):
        self.assertEqual(showDied30DaysAgo(), 0)

    def test_neverMarriedOver30(self):
        self.assertEqual(neverMarriedOver30(), 0)

    def test_checkSpouseAndMarriageDate(self):
        self.assertEqual(checkSpouseAndMarriageDate(), 0)

    def test_thirtyDayDifference(self):
        self.assertEqual(thirty_day_difference('10 OCT 2022'), False)
        self.assertEqual(thirty_day_difference('30 SEP 2022'), False)
        self.assertEqual(thirty_day_difference('9 SEP 2022'), False)

    def test_birthBeforeMarriage(self):
        self.assertEqual(birthBeforeMarriage(), 0)

    def test_birthsOutOfWedlock(self):
        self.assertEqual(birthOutOfWedlock(), 2)

    def test_SiblingMarriages(self):
        self.assertEqual(siblingMarriage(), 0)
    
    def test_marriageBefore14(self):
        self.assertEqual(marriageBefore14(), 0)
        indi = Person('@I234@', 'oiudhgf', 12, 'M',
                        '15 JUL 2010', True, 'N/A', [], 'N/A')
        Individuals['@I234@'] = indi
        indi = Person('@I235@', 'oiudhggf', 22, 'M',
                        '30 JUL 2000', True, 'N/A', [], 'N/A')
        Individuals['@I235@'] = indi
        fam = Family('@F235@', '24 NOV 2022', 'N/A', '@I234@',
                    'oiudhgf', '@I235@', 'oiudhggf', [])
        Families['@F235@'] = fam
        self.assertEqual(marriageBefore14(), 1)

    def test_Less_than_150_years(self):
        self.assertEqual(is_less_than_150_years(), 0)

    def test_Less_than_150_years(self):
        self.assertEqual(validate_life_events(), 0)

    def test_is_not_none(self):
        self.assertEqual(is_not_none("N/A"), False)

    def maleLastNames(self):
        self.assertEqual(allMalesinFamilyLastName(), 0)

    def test_is_not_none(self):
        self.assertEqual(is_not_none("Not_N/A"), True)

    def test_birthBeforeDeathOfParents(self):
        self.assertEqual(birthBeforeDeathOfParents(), 0)

    def test_divorceBeforeDeathOfSpouse(self):
        self.assertEqual(divorceBeforeDeathOfSpouse(), 0)


if __name__ == '__main__':
    unittest.main()
