print("Hello World")

Dict = {
    "INDI",
    "NAME",
    "SEX",
    "BIRT",
    "DEAT",
    "FAMC",
    "FAMS",
    "FAM",
    "MARR",
    "HUSB",
    "WIFE",
    "CHIL",
    "DIV",
    "DATE",
    "HEAD",
    "TRLR",
    "NOTE"
    }

with open('export-BloodTree.ged') as f:
    for pos, line in enumerate(f.readlines()):
        print("--> " + line[0:len(line)-1])
        """Initializes some base variables"""
        start=2;
        end=2;
        valid="N"
        arguments = ""
        tag = ""
        level = line[0:1]

        if(line[2:3] == "@" or line[2:3] == "¿"):
            end = len(line)
            start = end-1
            while(line[start] != " "):
                start = start-1;
            tag = line[start+1:end-1]
            arguments = line[2:start]
            if(tag in Dict):
                valid = "Y"
        else:
            """Checks the first tag to see if it's in our set"""
            while(end<len(line) and line[end] != " "):
                end+=1

            """Saves the tag and arguments and changes valid to Y if it is in set"""    
            if(end+1<len(line)):
                arguments = line[end+1:len(line)-1]
            if(end == len(line)):
                end-=1
            tag = line[start:end]
            if(tag in Dict):
                valid = "Y"
        print("<-- " + level + "|" + tag + "|" + valid + "|" + arguments + "\n")
        pos+=5
        
        
