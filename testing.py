import unittest

from GEDCOM import (Individuals, birthBeforeDeath, birthBeforeMarriage, birthOutOfWedlock, checkUniqueIndividualIDs, listDeceased, noMoreThan5Births, uniqueNameAndBirthdays,
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
listMulitpleBirths)

from utils import thirty_day_difference, diff_month, isDateLess

from Person import Person

#code for tetsting

        

from Person import Person
from Family import Family



class TestForErrors(unittest.TestCase):
    
    def test_UniqueFamilyNames0(self):  
        childData = { "2": Person(self, "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A")
        , "3" : Person(self, "7", "William McBride", 14 , "M", "20-JAN-2008", True , "N/A", "N/A")}
        dummy_data = {"1": Family("1", "24-JUL-1998", "N/A", "9", "Ty Boxing", "5", "Taylor Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        self.assertEqual(res, True)

    def test_UniqueFamilyNames1(self):   #testing with spouses having the same first name
        childData = { "2": Person(self, "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A")
        , "3" : Person(self, "7", "Willy McBride", 14 , "M", "20-JAN-2008", True , "N/A", "N/A")}
        dummy_data = {"2": Family("2", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Taylor Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        self.assertEqual(res, False)

    def test_UniqueFamilyNames2(self):  #checking when parents are same, and so are kids
        childData = { "2": Person(self, "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A")
        , "3" : Person(self, "7", "Willy McBride", 14 , "M", "20-JAN-2008", True , "N/A", "N/A")}
        dummy_data = {"3": Family("3", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Taylor Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data,childData)
        self.assertEqual(res, False)
    
    def test_UniqueFamilyNames3(self):   #checking when parents are different names, but kids have same first names
        childData = { "1" : Person( "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A", "N/A")
        ,"2" : Person("7", "Willy McBride", 14 ,"M", "20-JAN-2008", True , "N/A", "N/A", "N/A")}
        dummy_data = {"4": Family("4", "24-JUL-1998", "N/A", "9", "Troy Boxing", "5", "Taylor Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        self.assertEqual(res, False)

    def test_UniqueFamilyNames4(self):   #checking when both parents and kids have same names
        childData = { "1" : Person( "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A", "N/A")
        ,"2" : Person("7", "Willy McBride", 14 ,"M", "20-JAN-2008", True , "N/A", "N/A", "N/A")}
        dummy_data = {"5": Family("5", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Taylor Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        self.assertEqual(res, False)

    def test_UniqueFamilyNames5(self):   #checking when a parent and child have the same name
        childData = { "1" : Person( "2", "Worker McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A", "N/A")
        ,"2" : Person("7", "Taylor McBride", 14 ,"M", "20-JAN-2008", True , "N/A", "N/A", "N/A")}
        dummy_data = {"6": Family("6", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Kim Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        self.assertEqual(res, False)







if __name__ == '__main__':
    unittest.main()
