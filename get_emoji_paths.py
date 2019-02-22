import json
import os
from PIL import Image

#Creats a file that can be accessed to create a link between the unicode
#identifier and it's relative path.
#Creates path to apple emojis only

#Initializing Dictionaries
paths = {}
newUnicodeStrings = {}


#there are 1719 different emojis in the normal folder
for a in range(1,1720):
    
    try:
        #Getting unicode identifier, formatted U+XXXXX
        with open("emojis/normal/{}/code.txt".format(a),'r') as f:
            code = f.read()

        #Changing the formatting
        new =  "".join([  "\U"+ ("0" * (8 - len(x[2:]))) + x[2:] for x in code.split(" ")])
        new = str(new)
        
        path = "emojis/normal/{}/Appl.png".format(a)

        #If there is no apple emoji, it does not get added to the list
        if os.path.isfile(path):
            paths[new] = path

        
    except:
        pass



#there are 1300 different emojis in the skintone folder
for a in range(1,1301):
    
    try:
        #Getting unicode identifier, formatted U+XXXXX
        with open("emojis/skintone/{}/code.txt".format(a),'r') as f:
            code = f.read()

        #Changing the formatting
        new =  "".join([  "\U"+ ("0" * (8 - len(x[2:]))) + x[2:] for x in code.split(" ")])
        new = str(new)
        
        path = "emojis/skintone/{}/Appl.png".format(a)

        #If there is no apple emoji, it does not get added to the list
        if os.path.isfile(path):
            paths[new] = path

        
    except:
        #This fails if an apple emoji does not exist
        pass




#Iterating Through every escaped unicode
for a in paths:

    #Decoding it and re-encoding it allows for the graphing script to actually use the paths
    newUnicodeStrings[unicode(a).decode("unicode-escape").encode("unicode-escape")] = paths[a]







#Saving the file
with open("paths.txt",'w') as f:
    f.write(json.dumps(newUnicodeStrings,indent=4,sort_keys=True))




