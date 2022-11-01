from datetime import date, timedelta, datetime
from collections import OrderedDict
from prettytable import PrettyTable
from Person import Person
from Family import Family
from constants import month_dict, FAMILY_COLUMNS, INDIVIDUAL_COLUMNS
from utils import (diff_month,
                   parseDate,
                   isDateLess,
                   thirty_day_difference, thirty_day_ahead,
                   isDateValid, isDateLessThanOrEqual, is_not_none)

# Dictionary that holds all of the individuals values.
# FORMAT: {'Individual ID' : Person object }
Individuals = {}

# Dictionary that holds all of the families values.
# FORMAT: {'Family ID' : Family object }
Families = {}

# Holds all the errors
errors = []

died30DaysAgo = []
born30DaysAgo = []
anniversariesNext30Days = []

deceasedList = []

# This is the starter of the program, it reads the entire file and adds it to the
# Inidiviuals dictionary and Families dictionary


def parse(fileName):
    f = open(fileName)
    lines = f.readlines()
    idx = 0
    while (idx < len(lines)):
        line = lines[idx]
        end = len(line)
        if (line[end-5:end-1] == 'INDI'):
            idx = readIndividual(idx, lines)
        elif (line[end-4:end-1] == 'FAM'):
            idx = readFamily(idx, lines)
        else:
            idx += 1

    # Fills in missing info for the Person and Family class
    for fam in Families.values():
        'Adding to the husband'
        if (Individuals[fam.husband_id].gender == 'F'):
            errors.append('Husband: ' + fam.husband_id + ' cannot be Female')
        Individuals[fam.husband_id].children = fam.children
        Individuals[fam.husband_id].spouse = fam.wife_id

        'Adding to the wife'
        if (Individuals[fam.wife_id].gender == 'M'):
            errors.append('Wife: ' + fam.husband_id + ' cannot be Male')
        Individuals[fam.wife_id].children = fam.children
        Individuals[fam.wife_id].spouse = fam.husband_id

        'Adding missing info into family'
        fam.wife_name = Individuals[fam.wife_id].name
        fam.husband_name = Individuals[fam.husband_id].name

# this function reads in all of the individuals data and adds them to the Person class,
# then it adds the Person to the Individuals dictionary


def readIndividual(idx, lines):
    line = lines[idx]
    tags = line.split()
    temp_name = 'N/A'
    temp_age = 0
    temp_id = tags[1]
    temp_gender = 'N/A'
    temp_birthday = 'N/A'
    temp_alive = True
    temp_death = 'N/A'
    temp_child = []
    temp_spouse = 'N/A'
    idx += 1
    line = lines[idx]
    while (idx < len(lines) and line[0] != '0'):
        line = lines[idx]
        tags = line.split()
        if (tags[1] == 'NAME'):
            temp_name = tags[2] + " " + tags[3]
        if (tags[1] == 'SEX'):
            temp_gender = tags[2]
        if (tags[1] == 'BIRT'):
            idx += 1
            line = lines[idx]
            tags = line.split()
            if (tags[1] == 'DATE'):
                temp_birthday = tags[2] + ' ' + tags[3] + ' ' + tags[4]
            else:
                idx -= 1
        if (tags[1] == 'DEAT'):
            temp_alive = False
            idx += 1
            line = lines[idx]
            tags = line.split()
            if (tags[1] == 'DATE'):
                temp_death = tags[2] + ' ' + tags[3] + ' ' + tags[4]
            else:
                idx -= 1
        idx += 1

    if isDateValid(temp_birthday) and isDateValid(temp_death):
        temp_age = calculate_age(temp_birthday, temp_death)
        indi = Person(temp_id, temp_name, temp_age, temp_gender,
                      temp_birthday, temp_alive, temp_death, temp_child, temp_spouse)
        Individuals[temp_id] = indi

        '''Checks if they died in the past 30 days'''
        if (temp_alive == False):
            diedPast30Days(temp_death, indi)

        '''Checks if born in the past 30 days'''
        bornPast30Days(temp_birthday, indi)
    else:
        print(
            f'date birthday {temp_birthday} or date of death {temp_death} is not valid')
    return idx-1

# this function reads in all of the families data and adds them to the Family class,
# then it adds the family to the Families dictionary


def readFamily(idx, lines):
    line = lines[idx]
    tags = line.split()
    temp_id = tags[1]
    temp_married = 'N/A'
    temp_divorced = 'N/A'
    temp_husband_id = 'N/A'
    temp_husband_name = 'N/A'
    temp_wife_id = 'N/A'
    temp_wife_name = 'N/A'
    temp_children = []
    idx += 1
    line = lines[idx]
    while (idx < len(lines) and line[0] != '0'):
        line = lines[idx]
        tags = line.split()
        if (tags[1] == 'MARR'):
            idx += 1
            line = lines[idx]
            tags = line.split()
            if (tags[1] == 'DATE'):
                temp_married = tags[2] + ' ' + tags[3] + ' ' + tags[4]
            else:
                idx -= 1
        if (tags[1] == 'DIV'):
            idx += 1
            line = lines[idx]
            tags = line.split()
            if (tags[1] == 'DATE'):
                temp_divorced = tags[2] + ' ' + tags[3] + ' ' + tags[4]
            else:
                idx -= 1
        if (tags[1] == 'WIFE'):
            temp_wife_id = tags[2]
        if (tags[1] == 'HUSB'):
            temp_husband_id = tags[2]
        if (tags[1] == 'CHIL'):
            temp_children.append(tags[2])
        idx += 1

    if isDateValid(temp_married) and isDateValid(temp_divorced):
        fam = Family(temp_id, temp_married, temp_divorced, temp_husband_id,
                     temp_husband_name, temp_wife_id, temp_wife_name, temp_children)

        if thirty_day_ahead(temp_married):
            anniversariesNext30Days.append(fam)

        Families[temp_id] = fam
    else:
        print(
            f'date birthday {temp_married} or date of death {temp_divorced} is not valid')
    return idx-1

# This function calculates the age of an individual from their birthday and death day


def calculate_age(birthday, death):
    today = date.today()
    if (birthday == 'N/A'):
        return 0
    birthday_list = birthday.split()
    death_list = death.split()
    if (death == 'N/A'):
        curr_day = int(today.strftime("%d"))
        curr_month = int(today.strftime("%m"))
        curr_year = int(today.strftime("%Y"))
    else:
        curr_day = int(death_list[0])
        curr_month = month_dict[death_list[1]]
        curr_year = int(death_list[2])

    ind_day = int(birthday_list[0])
    ind_month = month_dict[birthday_list[1]]
    ind_year = int(birthday_list[2])

    age = curr_year - ind_year
    if (curr_month < ind_month):
        age -= 1
    if (curr_month == ind_month and curr_day < ind_day):
        age -= 1
    return age


def listLivingMarried():
    print('\n Living and Married Individuals')
    indi_list = []
    table = PrettyTable(INDIVIDUAL_COLUMNS)
    for fam in Families.values():
        if (Individuals[fam.husband_id].alive and Individuals[fam.wife_id].alive and fam.married != 'N/A'):
            indi_list.append(Individuals[fam.husband_id].id)
            indi_list.append(Individuals[fam.wife_id].id)

    for indi in list(set(indi_list)):
        person = Individuals[indi]
        table.add_row([person.id, person.name, person.gender, person.birthday,
                      person.age, person.alive, person.death, person.children, person.spouse])

    if (len(table.rows)):
        print(table)
        return 0
    else:
        print('No Individuals found living and married')
        return 1


def birthBeforeMarriage_MarriageBeforeDivorce():
    result = 0
    for fam in Families.values():
        if (fam.married != "N/A"):
            marriageDate = parseDate(fam.married)
            wifeDeathDate = Individuals[fam.wife_id].death
            husbandDeathDate = Individuals[fam.husband_id].death
            if fam.divorced != 'N/A':
                divorceDate = parseDate(fam.divorced)
                if isDateLess(divorceDate, marriageDate):
                    print('Error: US04: Divorce should not occur before marriage')
                    result = 1
            if husbandDeathDate != 'N/A' and isDateLess(parseDate(husbandDeathDate), marriageDate):
                print('Error: US05: Marriage cannot occur after husbands death')
                result = 1
            if wifeDeathDate != 'N/A' and isDateLess(parseDate(wifeDeathDate), marriageDate):
                print('Error: US05: Marriage cannot occur after wifes death')
                result = 1
    return result


def birthBeforeMarriage():
    for fam in Families.values():
        if (fam.married != "N/A"):
            marriageDate = parseDate(fam.married)
            husbandBirthDate = parseDate(Individuals[fam.husband_id].birthday)
            wifeBirthDate = parseDate(Individuals[fam.wife_id].birthday)
            if (not (isDateLess(husbandBirthDate, marriageDate) or isDateLess(wifeBirthDate, marriageDate))):
                print('Error: US02: Birth should occur before marriage of an individual')
                return 1
    return 0


# US07: Death should be less than 150 years after birth for dead people,
# and current date should be less than 150 years after birth for all living people
def is_less_than_150_years():
    date_150_years_in_future = (datetime.today()+timedelta(weeks=365*150))
    for indi in Individuals.values():
        if (is_not_none(indi.birthday)):
            birthDate = parseDate(indi.birthday)
        if (is_not_none(indi.death)):
            deathDate = parseDate(indi.death)
        if (not (isDateLess(birthDate, date_150_years_in_future) or isDateLess(deathDate, date_150_years_in_future))):
            print('Error: US07: Less then 150 years old')
            return 1


def validate_life_events():
    # US01: Dates (birth, marriage, divorce, death) should not be after the current date
    today = datetime.today()
    for fam in Families.values():
        if (is_not_none(fam.married)):
            marriageDate = parseDate(fam.married)
        if (is_not_none(fam.divorced)):
            divorcedDate = parseDate(fam.divorced)
        if (not (isDateLessThanOrEqual(marriageDate, today) or isDateLessThanOrEqual(divorcedDate, today))):
            print(
                'Error: US01: Dates (birth, marriage, divorce, death) should not be after the current date')
            return 1

    for indi in Individuals.values():
        if (is_not_none(indi.birthday)):
            birthDate = parseDate(indi.birthday)
        if (is_not_none(indi.death)):
            deathDate = parseDate(indi.death)
        if (not (isDateLessThanOrEqual(birthDate, today) or isDateLessThanOrEqual(deathDate, today))):
            print(
                'Error: US01: Dates (birth, marriage, divorce, death) should not be after the current date')
            return 1
    return 0


def birthBeforeDeath():
    for dec in deceasedList:
        birthDate = parseDate(dec.birthday)
        deathDate = parseDate(dec.death)
        if (not isDateLess(birthDate, deathDate)):
            print('Error: US03: Birth should occur before death of an individual')
            return 1
    return 0

# Shows the data in a pretty table of the individuals and the families


def showData():
    ordered_ind = OrderedDict(sorted(Individuals.items()))
    ordered_fam = OrderedDict(sorted(Families.items()))
    x = PrettyTable(INDIVIDUAL_COLUMNS)
    y = PrettyTable(FAMILY_COLUMNS)
    for ind in ordered_ind.values():
        x.add_row([ind.id, ind.name, ind.gender, ind.birthday,
                  ind.age, ind.alive, ind.death, ind.children, ind.spouse])
    for fam in ordered_fam.values():
        y.add_row([fam.id, fam.married, fam.divorced, fam.husband_id,
                  fam.husband_name, fam.wife_id, fam.wife_name, fam.children])

    print("Individuals")
    print(x)
    print("\n")
    print("Families")
    print(y)


def checkSpouseAndMarriageDate():
    spouseMarriageSet = set()
    count = 0
    for fam in Families.values():
        sm = fam.married + fam.husband_name + fam.wife_name
        if sm in spouseMarriageSet:
            print(
                fam.id + ' is being deleted as they have the same wife name, husband name, and mariage date')
            del Families[fam.id]
            count += 1
        else:
            spouseMarriageSet.add(sm)
    return count


def neverMarriedOver30():
    print('\nIndividuals over 30 who have never been married:')
    table = PrettyTable(INDIVIDUAL_COLUMNS)
    for person in Individuals.values():
        if (person.age > 30 and person.spouse == 'N/A'):
            table.add_row([person.id, person.name, person.gender, person.birthday,
                          person.age, person.alive, person.death, person.children, person.spouse])
    print(table)
    print(f'{len(table.rows)} individuals over 30 and were never married')
    return len(table.rows)


def bornPast30Days(birthday, indi):
    '''Shows people born in the past 30 days'''
    if thirty_day_difference(birthday):
        born30DaysAgo.append(indi)


def diedPast30Days(death, indi):
    '''Shows people who died in the past 30 days'''
    if thirty_day_difference(death):
        died30DaysAgo.append(indi)


def showBorn30DaysAgo():
    print('\nPeople who were born in the past 30 days:')
    table = PrettyTable(INDIVIDUAL_COLUMNS)
    for person in born30DaysAgo:
        table.add_row([person.id, person.name, person.gender, person.birthday,
                      person.age, person.alive, person.death, person.children, person.spouse])
    print(table)
    print(f'{len(died30DaysAgo)} recent deaths')
    return len(born30DaysAgo)


def showDied30DaysAgo():
    print('\nPeople who died in the past 30 days:')
    table = PrettyTable(INDIVIDUAL_COLUMNS)
    for person in died30DaysAgo:
        table.add_row([person.id, person.name, person.gender, person.birthday,
                      person.age, person.alive, person.death, person.children, person.spouse])
    print(table)
    print(f'{len(died30DaysAgo)} recent deaths')
    return len(died30DaysAgo)


def showUpcomingAnniversaries():
    print('\nPeople with anniversaries coming up in the next 30 days:')
    table = PrettyTable(FAMILY_COLUMNS)
    for fam in anniversariesNext30Days:
        if (Individuals[fam.husband_id].alive and Individuals[fam.wife_id].alive and fam.married != 'N/A'):
            table.add_row([fam.id, fam.married, fam.divorced, fam.husband_id,
                           fam.husband_name, fam.wife_id, fam.wife_name, fam.children])
    print(table)
    print(f'{len(anniversariesNext30Days)} upcoming anniversaries')
    return len(anniversariesNext30Days)


def uniqueNameAndBirthdays(individuals):
    if (not (len(individuals))):
        print("No Individuals found")
        return 1

    myDict = {}
    for indi in individuals.values():
        if (myDict.get(indi.name)):
            if (myDict[indi.name] == indi.birthday):
                print(
                    "\n Error: US23: More than one individual found with same name and birthday")
                return 1
        else:
            myDict[indi.name] = indi.birthday
    print("\n No individual found with same name and birthday")
    return 0


def checkCorrespondingIndividualRecords():
    indi_spouse_len = 0
    fam_children_len = 0

    total_indi_spousal_length = len(list(filter(lambda indi: indi.spouse !=
                                                "N/A", Individuals.values())))

    total_indi_children_len = sum(
        map(lambda indi: len(indi.children),  Individuals.values()), 0)

    for indi in Individuals.values():
        for fam in Families.values():
            if (indi.spouse != 'N/A'):
                if (indi.gender == "M"):
                    if (indi.id == fam.husband_id and indi.spouse == fam.wife_id):
                        indi_spouse_len += 1
                elif (indi.gender == "F"):
                    if (indi.id == fam.wife_id and indi.spouse == fam.husband_id):
                        indi_spouse_len += 1

            if (len(indi.children)):
                for indi_child in indi.children:
                    if (indi_child in fam.children):
                        fam_children_len += 1

    return indi_spouse_len == total_indi_spousal_length and fam_children_len == total_indi_children_len


def checkCorrespondingFamilyRecords():
    for fam in Families.values():
        if (not (Individuals[fam.husband_id] and Individuals[fam.wife_id])):
            return False
        else:
            if (len(fam.children)):
                for fam_child in fam.children:
                    if (not (Individuals[fam_child])):
                        return False

    return True


def checkUniqueIndividualIDs():
    uniqueIDs = []
    while True:
        for person in Individuals.values():
            if person.id not in uniqueIDs:
                uniqueIDs.append(person.id)
            else:
                print("\n" + person.id + " is not unique")
                return False
        print("\n All indivuals IDs are unique")
        return False


def checkUniqueFamilyIDs():
    uniqueIDs = []
    while True:
        for fam in Families.values():
            if fam.id not in uniqueIDs:
                uniqueIDs.append(fam.id)
            else:
                print("\n" + fam.id + " is not unique")
                return False
        print("\n All families IDs are unique")
        break


def checkUniqueFamilyNames():
    while True:
        uniqueNames = []
        for fam in Families.values():
            husbandName = fam.husband_name.split(" ")
            wifeName = fam.wife_name.split(" ")
            if husbandName[0] == wifeName[0]:
                print(
                    "Cannot have to people in the same family with the same first name")
                return False
            else:
                uniqueNames.append(husbandName[0])
                uniqueNames.append(wifeName[0])

            children = fam.children

            for child in children:
                childName = Individuals.get(child).name
                firstName = childName.split(" ")
                if firstName[0] not in uniqueNames:
                    uniqueNames.append(firstName[0])
                else:
                    print(f"Cannot have same name, {firstName[0]}")
                    return False
            print("\n All names in family {} are unique".format(fam.id))
            print(uniqueNames)
            uniqueNames.clear()
        break


def listDeceased():
    for indi in Individuals.values():
        if indi.death != "N/A":
            deceasedList.append(indi)
    showDeceased()


def showDeceased():
    print('\n Deceased Individuals')
    table = PrettyTable(INDIVIDUAL_COLUMNS)
    for person in deceasedList:
        table.add_row([person.id, person.name, person.gender, person.birthday,
                      person.age, person.alive, person.death, person.children, person.spouse])
    print(table)
    print(f'{len(deceasedList)} deaths')


def listMulitpleBirths():
    for fam in Families.values():
        multipleBirths = []
        lets = []
        for children in fam.children:
            child = Individuals.get(children)
            if child.birthday not in multipleBirths:
                multipleBirths.append(child.birthday)
            elif child.birthday in multipleBirths:
                print((len(lets) - 1) + "Births on {}".format(child.birthday))
                multipleBirths.append(child.birthday)
                lets.append(child.birthday)
        return lets

    if len(lets) == 0:
        print("\n No multiple births")

def noMoreThan5Births(self):
    if self.listMultipleBirths() >= 5:
        print("Cannot have more than 5 siblings born on the same day")



def birthOutOfWedlock():
    count = 0
    for fam in Families.values():
        husbandDead = Individuals[fam.husband_id].death
        wifeDead = Individuals[fam.wife_id].death
        if (fam.married != "N/A" and fam.divorced != "N/A"):  # if family is married and divorced
            marriageDate = parseDate(fam.married)
            for children in fam.children:
                child = Individuals.get(children)
                childBirthDate = parseDate(child.birthday)
                if isDateLess(childBirthDate, marriageDate):
                    print(f"{child.name} Born out of wedlock")
                    count += 1
        # if fam is married and not divorced
        if (fam.married != "N/A" and fam.divorced == "N/A" and husbandDead == "N/A" and wifeDead == "N/A"):
            marriageDate = parseDate(fam.married)
            for children in fam.children:
                child = Individuals.get(children)
                childBirthDate = parseDate(child.birthday)
                if diff_month(childBirthDate, marriageDate) >= 9:
                    print(f"{child.name} Born out of wedlock")
                    count += 1
        if (fam.married == "N/A" and fam.divorced == "N/A"):  # if fam is not married or divorced
            for children in fam.children:
                child = Individuals.get(children)
                childBirthDate = parseDate(child.birthday)
                print(f"{child.name} Born out of wedlock")
                count += 1
    return count


def siblingMarriage():
    count = 0
    for fam in Families.values():
        childList = []
        for children in fam.children:
            child = Individuals.get(children)
            childList.append(child)
            for each in childList:
                if each.spouse in children:
                    print(f"Cannot have siblings marry")
                    count += 1
    return count


def checkCorrespondingEntries():
    # checks for the corresponding entries in family
    indi = checkCorrespondingIndividualRecords()
    fam = checkCorrespondingFamilyRecords()
    if (indi and fam):
        print('\n Corresponding entries for person(spouse, children) family(spouse, children) exist')
        return True

    print('\n Error: US26: Corresponding entries for person(spouse, children) family(spouse, children) do not exist')
    return False


def listData():
    listLivingMarried()
    neverMarriedOver30()
    showDied30DaysAgo()
    showBorn30DaysAgo()
    listDeceased()
    showUpcomingAnniversaries()


def calculateErrors():
    uniqueNameAndBirthdays(Individuals)
    checkCorrespondingEntries()
    birthBeforeDeath()
    birthBeforeMarriage()
    birthBeforeMarriage_MarriageBeforeDivorce()
    birthOutOfWedlock()
    siblingMarriage()
    validate_life_events()
    is_less_than_150_years()


# Driver code
parse('My-Family-TR.ged')
showData()
listData()
calculateErrors()
checkSpouseAndMarriageDate()
checkUniqueIndividualIDs()
checkUniqueFamilyIDs()
checkUniqueFamilyNames()
listMulitpleBirths()
