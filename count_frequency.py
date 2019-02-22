import json
from collections import Counter

#Arbritrary Filename, edit as needed
filename = "meirl-months{}.txt"

#Load data
with open(filename.format("")) as f:
    data = json.loads(f.read())

#Initializing Variable
count = {}

#For each month in the dataset, get frequency of each middle character
for a in data:
    count[a] = dict(Counter(data[a]))



#Save the data to a new file.
with open(filename.format("-counted"),'w') as f:
    f.write(json.dumps(count,indent=4,sort_keys=True))
