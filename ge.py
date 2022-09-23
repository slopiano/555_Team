from datetime import date
from collections import OrderedDict
from prettytable import PrettyTable

Individuals = {}
Families = {}

listers = []
month_dict = {
        'JAN' : 1,
        'FEB' : 2,
        'MAR' : 3,
        'APR' : 4,
        'MAY' : 5,
        'JUN' : 6,
        'JUL' : 7,
        'AUG' : 8,
        'SEP' : 9,
        'OCT' : 10,
        'NOV' : 11,
        'DEC' : 12
    }

f=open('export-BloodTree.ged')

line=f.readlines()

#Holds all the info a person should have
class Person:
    def __init__(self, ID, name, age, gender, birthday, alive, death, children, spouse):
        self.name = name
        self.age = age
        self.id = ID
        self.gender = gender
        self.birthday = birthday
        self.alive = alive
        self.death = death
        self.children = children
        self.spouse = spouse

#Holds all the info a family should have
class Family:
    def __init__(self, ID, married, divorced, husband_id, husband_name, wife_id, wife_name, children):
        self.id = ID
        self.married = married
        self.divorced = divorced
        self.husband_id = husband_id
        self.husand_name = husband_name
        self.wife_id = wife_id
        self.wife_name = wife_name
        self.children = children

# This is the starter of the program, it reads the entire file and adds it to the
# Inidiviuals dictionary and Families dictionary
def parse():
    f = open('export-BloodTree.ged')
    lines = f.readlines()
    idx = 0
    while(idx < len(lines)):
        line = lines[idx]
        end = len(line)
        if(line[end-5:end-1] == 'INDI'):
            idx = readIndividual(idx, lines)
        elif(line[end-4:end-1] == 'FAM'):
            idx = readFamily(idx, lines)
        else:
            idx+=1

    #Fills in missing info for the Person and Family class
    for fam in Families.values():
        'Adding to the husband'
        Individuals[fam.husband_id].children = fam.children
        Individuals[fam.husband_id].spouse = fam.wife_id

        'Adding to the wife'
        Individuals[fam.wife_id].children = fam.children
        Individuals[fam.wife_id].spouse = fam.husband_id

        'Adding missing info into family'
        fam.wife_name = Individuals[fam.wife_id].name
        fam.husband_name = Individuals[fam.husband_id].name

    showData()

# this function reads in all of the individuals data and adds them to the Person class,
# then it adds the Person to the Individuals dictionary
def readIndividual(idx, lines):
    line = lines[idx]
    temp_name = 'N/A'
    temp_age = 'N/A'
    temp_id = line[2:len(line)-6]
    temp_gender = 'N/A'
    temp_birthday = 'N/A'
    temp_alive = True
    temp_death = 'N/A'
    temp_child = []
    temp_spouse = []
    idx+=1
    line = lines[idx]
    while(idx < len(lines) and line[0] != '0'):
        line = lines[idx]
        if(len(line) > 6 and line[2:6] == 'NAME'):
            temp_name = line[7:len(line)]
        if(len(line) > 5 and line[2:5] == 'SEX'):
            temp_gender = line[6:7]
        if(len(line) > 6 and line[2:6] == 'BIRT'):
            idx+=1
            line = lines[idx]
            if(len(line) > 6 and line[2:6] == 'DATE'):
                temp_birthday = line[7:len(line)]
            else:
                idx-=1
        if(len(line) > 6 and line[2:6] == 'DEAT'):
            temp_alive = False
            idx+=1
            line = lines[idx]
            if(len(line) > 6 and line[2:6] == 'DATE'):
                temp_death = line[7:len(line)]
            else:
                idx-=1
        idx+=1
        
    temp_age = calculate_age(temp_birthday, temp_death)
    indi = Person(temp_id, temp_name, temp_age, temp_gender, temp_birthday, temp_alive, temp_death, temp_child, temp_spouse)
    Individuals[temp_id] = indi
    return idx-1

# this function reads in all of the families data and adds them to the Family class,
# then it adds the family to the Families dictionary
def readFamily(idx, lines):
    line = lines[idx]
    temp_id = line[2:len(line)-5]
    temp_married = 'N/A'
    temp_divorced = 'N/A'
    temp_husband_id = 'N/A'
    temp_husband_name = 'N/A'
    temp_wife_id = 'N/A'
    temp_wife_name = 'N/A'
    temp_children = []
    idx+=1
    line = lines[idx]
    while(idx < len(lines) and line[0] != '0'):
        line = lines[idx]
        tags = line.split()
        if(tags[1] == 'MARR'):
            idx+=1
            line = lines[idx]
            tags = line.split()
            if(tags[1] == 'DATE'):
                temp_married = tags[2] + ' ' + tags[3] + ' ' + tags[4]
            else:
                idx-=1
        if(tags[1] == 'DIV'):
            idx+=1
            line = lines[idx]
            tags = line.split()
            if(tags[1] == 'DATE'):
                temp_divorced = tags[2] + ' ' + tags[3] + ' ' + tags[4]
            else:
                idx-=1
        if(tags[1] == 'WIFE'):
            temp_wife_id = tags[2]
        if(tags[1] == 'HUSB'):
            temp_husband_id = tags[2]
        if(tags[1] == 'CHIL'):
            temp_children.append(tags[2])
        idx+=1

    fam = Family(temp_id, temp_married, temp_divorced, temp_husband_id, temp_husband_name, temp_wife_id, temp_wife_name, temp_children)
    Families[temp_id] = fam
    return idx-1

# This function calculates the age of an individual from their birthday and death day
def calculate_age(birthday, death):
    today = date.today()
    if(birthday == 'N/A'):
        return 0
    birthday_list = birthday.split()
    death_list = death.split()
    if(death == 'N/A'):
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
    if(curr_month < ind_month):
        age-=1
    if(curr_month == ind_month and curr_day < ind_day):
        age-=1
    return age
        
        
def showData():
    ordered_ind = OrderedDict(sorted(Individuals.items()))
    ordered_fam = OrderedDict(sorted(Families.items()))
    x = PrettyTable()
    y = PrettyTable()
    x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    y.field_names = ["ID", "Married", "Divorced", "Huasband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    for ind in ordered_ind.values():
        x.add_row([ind.id, ind.name, ind.gender, ind.birthday, ind.age, ind.alive, ind.death, ind.children, ind.spouse])
    for fam in ordered_fam.values():
        y.add_row([fam.id, fam.married, fam.divorced, fam.husband_id, fam.husband_name, fam.wife_id, fam.wife_name, fam.children])       

    print("Individuals")
    print(x)
    print("\n")
    print("Families")
    print(y)







        
    
