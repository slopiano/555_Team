# Holds all the info a family should have
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
