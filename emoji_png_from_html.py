import base64
from bs4 import BeautifulSoup
import os

#In the html files, the emojis were stored as base64 strings. This saves them as pngs

#This is either "normal" or "skintone". change as needed
emojiType = "normal"

#Opening the html file
with open("emoji-{}.html".format(emojiType),'r') as f:
    site = f.read()

#Creating the very  beautiful soup
soup = BeautifulSoup(site,"html.parser")

#Function for converting the base64 string and saving the image
def saveImage(path,data):
    imgdata = base64.b64decode(data)

    #Saving the Image
    with open(path, 'wb') as f:
        f.write(imgdata)


#Dictionary for emoji names based on their column on the site
nameDict = {
    3:"Appl",
    4:"Goog",
    5:"FB",
    6:"Wind",
    7:"Twtr",
    8:"One",
    9:"Sams",
    10:"GMail",
    11:"SB",
    12:"DCM",
    13:"KDDI"
    }


#Getting each row in the table
for tr in soup.find("table").find_all("tr"):
    tds = tr.find_all("td")

    #Some rows did not contain emojis, this factors them out
    if len(tds) == 15:

        directory = "emojis/{}/{}/".format(emojiType,tds[0].text)

        #Checking if the specific emoji's folder exists, if not it creates it
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Saves the unicode identifier
        with open(directory+"code.txt",'w') as f:
            f.write(tds[1].text)

        #Going through each element in the row, 3-13 are the emojis
        for a in range(3,14):

            #Checking if an emoji exists for that specific company
            if len(tds[a].find_all("img")) != 0:

                #Gettings the base64 string
                src = tds[a].img.get("src")[22:]

                #Saving the emoji
                saveImage(directory+nameDict[a]+".png",src)
            












