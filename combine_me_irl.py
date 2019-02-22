import json

#Combines my three separate me_irl files into a single file now that they are compressed


#Loading the data
#These are the filenames I designated for each file, change as needed.
with open('me_irl-startto2017-months-counted.txt') as f:
    source1 = json.loads(f.read())

with open('me_irl-2017to2018-months-counted.txt') as f:
    source2 = json.loads(f.read())

with open('me_irl-2018to2019-months-counted.txt') as f:
    source3 = json.loads(f.read())

#Master Dictionary 
master = {}

#Adding all three sources to master 
for a in source1:
    master[a] = source1[a]

for a in source2:
    master[a] = source2[a]

for a in source3:
    master[a] = source3[a]

#Save as new file
with open("me_irl-months-counted.txt",'w') as f:
    f.write(json.dumps(master, indent=4,sort_keys=True))
