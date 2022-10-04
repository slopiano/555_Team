from datetime import date, timedelta
from collections import OrderedDict
from prettytable import PrettyTable
from Person import Person
from Family import Family
from constants import month_dict, FAMILY_COLUMNS, INDIVIDUAL_COLUMNS
from utils import diff_month
from datetime import datetime

# Dictionary that holds all of the individuals values.
# FORMAT: {'Individual ID' : Person object }
Individuals = {}

# Dictionary that holds all of the families values.
# FORMAT: {'Family ID' : Family object }
Families = {}

# Holds all the errors
errors = []

died30DaysAgo = []

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

    temp_age = calculate_age(temp_birthday, temp_death)
    indi = Person(temp_id, temp_name, temp_age, temp_gender,
                  temp_birthday, temp_alive, temp_death, temp_child, temp_spouse)
    Individuals[temp_id] = indi

    '''Checks if they died in the past 30 days'''
    if (temp_alive == False):
        diedPast30Days(temp_death, indi)

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

    fam = Family(temp_id, temp_married, temp_divorced, temp_husband_id,
                 temp_husband_name, temp_wife_id, temp_wife_name, temp_children)
    Families[temp_id] = fam
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


def listRecentBirths():
    print('\n Recent births')
    table = PrettyTable(INDIVIDUAL_COLUMNS)
    for person in Individuals.values():
        day, month, year = person.birthday.split()
        d1 = datetime.today()
        d2 = datetime(int(year), month_dict[month], int(day))
        if (diff_month(d1, d2) <= 1):
            table.add_row([person.id, person.name, person.gender, person.birthday,
                          person.age, person.alive, person.death, person.children, person.spouse])

    if (len(table.rows)):
        print(table)
        print(len(table.rows), "Recent births found in 30 days")
        return 0
    else:
        print("No recent births found in the past 30 days")
        return 1


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
            count+=1
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


def diedPast30Days(death, indi):
    '''Gets the date 30 days before today'''
    day_before = (date.today()-timedelta(days=30))
    curr_day = int(day_before.strftime("%d"))
    curr_month = int(day_before.strftime("%m"))
    curr_year = int(day_before.strftime("%Y"))

    '''Gets the death date'''
    death_list = death.split()
    ind_day = int(death_list[0])
    ind_month = month_dict[death_list[1]]
    ind_year = int(death_list[2])

    if (curr_year < ind_year):
        died30DaysAgo.append(indi)
    elif (curr_year == ind_year and curr_month < ind_month):
        died30DaysAgo.append(indi)
    elif (curr_year == ind_year and curr_month == ind_month and curr_day < ind_day):
        died30DaysAgo.append(indi)


def showDied30DaysAgo():
    print('\nPeople who died in the past 30 days:')
    table = PrettyTable(INDIVIDUAL_COLUMNS)
    for person in died30DaysAgo:
        table.add_row([person.id, person.name, person.gender, person.birthday,
                      person.age, person.alive, person.death, person.children, person.spouse])
    print(table)
    print(f'{len(died30DaysAgo)} recent deaths')


def uniqueNameAndBirthdays(individuals):
    myDict = {}
    for indi in individuals.values():
        if (myDict.get(indi.name)):
            if (myDict[indi.name] == indi.birthday):
                print(
                    "\n Error: More than one individual found with same name and birthday")
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
        return False


def checkUniqueFamilyNames():
    while True:
        uniqueNames = []
        for fam in Families.values():
            husbandName = fam.husband_name.split(" ")
            wifeName = fam.wife_name.split(" ")
            if husbandName[0] == wifeName[0]:
                print("Cannot have to people in the same family with the same first name")
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
        return False

deceasedList = []        

def listDeceased():
    for indi in Individuals.values():
        if indi.death != "N/A":
            deceasedList.append(indi)


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
                print((len(lets) +1) + "Births on {}".format(child.birthday))
                multipleBirths.append(child.birthday)
                lets.append(child.birthday)
          
    if len(lets) == 0:
        print("\n No multiple births")






def checkCorrespondingEntries():
    # checks for the corresponding entries in family
    indi = checkCorrespondingIndividualRecords()
    fam = checkCorrespondingFamilyRecords()
    if (indi and fam):
        print('\n Corresponding entries for person(spouse, children) family(spouse, children) exist')
        return True

    print('\n Corresponding entries for person(spouse, children) family(spouse, children) do not exist')
    return False


def listData():
    listLivingMarried()
    neverMarriedOver30()
    showDied30DaysAgo()
    listRecentBirths()
    listDeceased()
    showDeceased()


def calculateErrors():
    uniqueNameAndBirthdays(Individuals)
    checkCorrespondingEntries()


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