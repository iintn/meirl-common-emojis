import json
import requests
from datetime import datetime
import emoji

#Initializing Variables
titles = []
times = []

#Variable to decide whether or not to continue getting more scripts
shouldGoOn = True

#Choose Between "meirl" and "me_irl"
sub = "meirl"

#If Script was canceled for some reason and you wanted to pick up from where you left off.
try:
 with open("data.txt","r") as f:
  prev = json.loads(f.read())

 prevTime = int(prev[-1]["created_utc"])+1
except:
 prevTime=1



while shouldGoOn:
 #Pushshift's api url
 url = 'https://api.pushshift.io/reddit/search/submission/?size=500&subreddit={}&after={}&fields=created_utc,title'.format(sub,prevTime)

 data = json.loads(requests.get(url).text)["data"]

 for a in data:
  titles.append(a)

 prevTime=int(data[-1]['created_utc'])+1

 #Printing the time, formatted
 print ( datetime.utcfromtimestamp( prevTime ).strftime( '%Y-%m-%d %H:%M:%S' ) ),prevTime

 if len(data)!=500:
  shouldGoOn=False
 #When To Stop The Script, note: A memory error was caused with the amount of me_irl titles.
 #I split it into 3 separate files with the unix times depicted at the end of the file.
 if prevTime > 1546300800:
  shouldGoOn = False



#Arbritrary File Name,
with open('data-emoji-{}.txt'.format(sub),'w') as f:
 f.write(json.dumps(titles,sort_keys=True,indent=4).encode("UTF-8"))



##UNIX TIMES
#1546300800 - 2019 Jan 1 00:00:00
#1514764800 - 2018 Jan 1 00:00:00
#1483228800 - 2017 Jan 1 00:00:00

















