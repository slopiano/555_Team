import unittest

from GEDCOM import (birthBeforeDeath, birthBeforeMarriage, birthOutOfWedlock, checkUniqueIndividualIDs, listDeceased, noMoreThan5Births, uniqueNameAndBirthdays,
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

def checkUniqueFamilyNames(families, individuals):
    while True:
        uniqueNames = []
        for fam in families.values():
            husbandName = fam.husband_name.split(" ")
            wifeName = fam.wife_name.split(" ")
            if husbandName[0] == wifeName[0]:
                print("Cannot have two people in the same family with the same first name")
                return 0
            else:
                uniqueNames.append(husbandName[0])
                uniqueNames.append(wifeName[0])


            children = fam.children
      
            for child in children:
                childName = individuals.get(child)
                firstName = childName.name.split(" ")
                if firstName[0] not in uniqueNames:
                   uniqueNames.append(firstName[0])
                else:
                    print(f"Cannot have same name, {firstName[0]}")
                    return 1
                    break
            print("\n All names in family {} are unique".format(fam.id))
            print(uniqueNames)
            uniqueNames.clear()
        break


from Person import Person
from Family import Family


class TestForErrors(unittest.TestCase):


    def test_UniqueFamilyNames1(self):   #testing with spouses having the same first name
        dummy_data = {"1": Family("1", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Taylor Reinert", "2,7")}
        childData = { "2": Person(self, "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A")
        , "3" : Person(self, "7", "Willy McBride", 14 , "M", "20-JAN-2008", True , "N/A", "N/A")}
        res = checkUniqueFamilyNames(dummy_data, childData)
        print(res)
        self.assertEqual(res, 0)

    def test_UniqueFamilyNames2(self):  #checking when parents are same, and so are kids
        childData = { "2": Person(self, "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A")
        , "3" : Person(self, "7", "Willy McBride", 14 , "M", "20-JAN-2008", True , "N/A", "N/A")}
        dummy_data = {"1": Family("1", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Taylor Reinert", childData)}
    
        res = checkUniqueFamilyNames(dummy_data, childData)
        self.assertNotEqual(res, 1)
    
    def test_UniqueFamilyNames3(self):   #checking when parents are different names, but kids have same first names
        childData = { "1" : Person( "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A", "N/A")
        ,"2" : Person("7", "Willy McBride", 14 ,"M", "20-JAN-2008", True , "N/A", "N/A", "N/A")}

        dummy_data = {"1": Family("1", "24-JUL-1998", "N/A", "9", "Troy Boxing", "5", "Taylor Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        print(res)
        self.assertEqual(res, 1)

    def test_UniqueFamilyNames4(self):   #checking when both parents and kids have same names
        childData = { "1" : Person( "2", "Willy McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A", "N/A")
        ,"2" : Person("7", "Willy McBride", 14 ,"M", "20-JAN-2008", True , "N/A", "N/A", "N/A")}

        dummy_data = {"1": Family("1", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Taylor Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        print(res)
        self.assertEqual(res, 0)

    def test_UniqueFamilyNames5(self):   #checking when a parent and child have the same name
        childData = { "1" : Person( "2", "Worker McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A", "N/A")
        ,"2" : Person("7", "Taylor McBride", 14 ,"M", "20-JAN-2008", True , "N/A", "N/A", "N/A")}

        dummy_data = {"1": Family("1", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Kim Reinert", childData)}
        res = checkUniqueFamilyNames(dummy_data, childData)
        print(res)
        self.assertEqual(res, 1)

    def test_noMoreThan5Births(self):   #checking when a parent and child have the same name
        childData = { "1" : Person( "2", "Worker McBride", 7 , "M", "20-JAN-2015", True , "N/A", "N/A", "N/A")
        ,"2" : Person("7", "Taylor McBride", 14 ,"M", "20-JAN-2015", True , "N/A", "N/A", "N/A")}

        dummy_data = {"1": Family("1", "24-JUL-1998", "N/A", "9", "Taylor Boxing", "5", "Kim Reinert", childData)}
        res = noMoreThan5Births(childData)
        print(res)
        self.assertEqual(res, 0)






if __name__ == '__main__':
    unittest.main()
