import json

#Arbritrary Filenames for your data, edit as needed
with open("data-emoji-meirl.txt") as f:
    data = json.loads(f.read())


#Removes everything that was posted after Jan 1, 2019
data = [x for x in data if x["created_utc"] < 1546300800]

#Removes everything that doesn't start with "me" and end with "irl"
data = [x for x in data if unicode(x["title"]).lower()[:2] == "me" and \
        unicode(x["title"]).lower()[-3:] == "irl"]


#Saves Data
with open("data-emoji-meirl.txt",'w') as f:
    f.write(json.dumps(data,indent=4,sort_keys=True))
