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
