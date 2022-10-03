import unittest
from GEDCOM import uniqueNameAndBirthdays, checkCorrespondingEntries, listLivingMarried, listRecentBirths

from Person import Person


class TestForErrors(unittest.TestCase):

    def test_listLessThanOneIndWithSameBDayAndName_error_path(self):
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
        }
        res = uniqueNameAndBirthdays(dummy_data)
        self.assertEqual(res, 1)

    def test_listLessThanOneIndWithSameBDayAndName_happy_path(self):
        dummy_data = {
            "1": Person("1", "ASD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
            "2": Person("1", "BSD", 22, "M", "01-JAN-2001", True, "N\A", "N\A", "N\A"),
        }
        res = uniqueNameAndBirthdays(dummy_data)
        self.assertEqual(res, 0)

    def test_check_corresponding_entries(self):
        self.assertTrue(checkCorrespondingEntries())

    def test_living_and_married(self):
        self.assertEqual(listLivingMarried(), 0)

    def test_list_recent_births(self):
        self.assertEqual(listRecentBirths(), 1)


if __name__ == '__main__':
    unittest.main()
