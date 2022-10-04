import unittest

from GEDCOM import (checkUniqueIndividualIDs, listDeceased, uniqueNameAndBirthdays,
checkCorrespondingEntries,
listLivingMarried,
listRecentBirths,
calculate_age, 
checkUniqueFamilyIDs,
checkUniqueFamilyNames,
listDeceased,
listMulitpleBirths)

from GEDCOM import uniqueNameAndBirthdays, checkCorrespondingEntries, listLivingMarried, listRecentBirths, calculate_age, showDied30DaysAgo, neverMarriedOver30, checkSpouseAndMarriageDate


from Person import Person


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
        self.assertEqual(listRecentBirths(), 1)

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

if __name__ == '__main__':
    unittest.main()
