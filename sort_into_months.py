import json
import emoji
from datetime import datetime

#Arbritrary Filename, edit as needed
with open("data-emoji-meirl.txt") as f:
    data = json.loads(f.read())

#Removing "me" and "irl" from titles, leaving only middle characters
for a in range(len(data)):
    data[a]["title"] = unicode(data[a]["title"])[2:-3]

#Initializing variable
months = {}

#Iterating Through Each Title
for a in data:

    #Converting title's unix time to YYYY-MM
    month = str(datetime.utcfromtimestamp(a["created_utc"]).strftime('%Y-%m'))

    #If the month is not in the dictionary, create it then add the title
    #If it's in the dictionary, just add the title
    if month not in months:
        months[month] = []
        months[month].append(a['title'])
    else:
        months[month].append(a['title'])

#Arbritrary Filename
with open("meirl-months.txt",'w') as f:
    f.write(json.dumps(months,indent=4,sort_keys=True))

