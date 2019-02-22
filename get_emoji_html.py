# -*- coding: utf-8 -*-
import requests

#Downloading Emojis from site that has complete lists

#getting normal emojis
page = requests.get("http://www.unicode.org/emoji/charts/full-emoji-list.html")

#Saving file
with open("emojis-normal.html",'w') as f:
    f.write(page.text.encode("utf-8"))

#Getting skintone emojis
page = requests.get("https://www.unicode.org/emoji/charts/full-emoji-modifiers.html")

#Saving file
with open("emojis-skintone.html",'w') as f:
    f.write(page.text.encode("utf-8"))
