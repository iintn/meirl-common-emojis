from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import random
import json
import emoji

#Loading Data
data = {}

with open("meirl.txt",'r') as f:
    meirl = json.loads(f.read())

with open("me_irl.txt",'r') as f:
    me_irl = json.loads(f.read())

with open("paths.txt")as f:
    paths = json.loads(f.read())


#Combining Datasets
for date in me_irl:
    data[date] = {}
    data[date]["me_irl"] = me_irl[date]
    data[date]["meirl"] = meirl.get(date,[])

#Placing the dates in order
dataList = sorted([x for x in data])



sfData = {
    "":{
        "me_irl":{},
        "meirl":{}
        }
    }
for date in meirl:
    for title in meirl[date]:
        if title not in sfData[""]["meirl"]:
            sfData[""]['meirl'][title] = meirl[date][title]
        else:
            sfData[""]['meirl'][title] += meirl[date][title]
        
for date in me_irl:
    for title in me_irl[date]:
        if title not in sfData[""]["me_irl"]:
            sfData[""]['me_irl'][title] = me_irl[date][title]
        else:
            sfData[""]['me_irl'][title] += me_irl[date][title]
        

data = sfData
dataList = [""]


#Colors
backgroundColor = (245, 245, 245)
barColor = (169, 169, 169)
textColor = (0,0,0)

#Rectangle Sizing
rectHeight = 112

rectSpacing = int(rectHeight / 2.5)

maxNumBars = 15
maxRectWidth = (maxNumBars*rectHeight + (maxNumBars-1)*rectSpacing) / 2.25


barsImgSize = maxNumBars*rectHeight + (maxNumBars-1)*rectSpacing
barsImgSize = (int(barsImgSize*1.4),barsImgSize)


frameCounter = 1

#For Each Month..
for date in dataList:

    #Initializing Bars Image
    barsImg = Image.new("RGBA",barsImgSize, backgroundColor)
    draw = ImageDraw.Draw(barsImg)

    #Creating Full Image
    full = Image.new("RGBA",(int(barsImg.size[0] * 1.0),int(barsImg.size[1] * 1.4)),(245, 245, 245))
    drawfull = ImageDraw.Draw(full)
    pasteCoords = ((full.size[0] - barsImg.size[0]) / 2,int((full.size[1] - barsImg.size[1] )* .75))
    

    #Drawing Middle Line
    midBarWidth = 12
    draw.rectangle(((barsImg.size[0]/2-midBarWidth/2,0),(barsImg.size[0]/2+midBarWidth/2,barsImg.size[1])), fill = textColor)

    #Drawing Bars

    
    current = data[date]
    
    #Removing Specific Characters From counts, comment this section out to include them
    '''
    try:
        del current["me_irl"][""]
    except:
        pass
    try:
        del current["me_irl"][" "]
    except:
        pass
    try:
        del current["me_irl"]["_"]
    except:
        pass
    '''

    #me_irl (right) side

    #Getting The Total For The Month
    countSum = float(0)
    for a in current["me_irl"]:
        countSum += current["me_irl"][a]

    #Calculating Percents and Putting Them Into Separate Dictionary
    percents = {}
    for a in current["me_irl"]:
        percents[a] = float("{0:.2f}".format(current["me_irl"][a] / countSum * 100))


    #Ordering Values Greatest to Smallest
    ordered = sorted([x for x in percents], key=lambda x:percents[x],reverse=True)




    #Cutting Off Extra Values
    ordered = ordered[:maxNumBars]

    #print ordered


    #Starting Cooordinates
    prevTL = (300+midBarWidth/2 +barsImg.size[0]/2,0 -(rectSpacing+rectHeight))
    prevBR = (300+barsImg.size[0]/2  , rectHeight -(rectSpacing+rectHeight))

    #Initializing Font
    font = ImageFont.truetype("Helvetica.ttf", size=rectHeight/2)
    font = ImageFont.truetype("Symbola.ttf", size=rectHeight/2)

    #Going Through Each Value
    for val in ordered:

        #The New Coordinates
        topLeft = (prevTL[0],prevTL[1]+rectSpacing+rectHeight)
        bottomRight = (prevTL[0] + (percents[val] / 100 * maxRectWidth),prevBR[1]+rectSpacing+rectHeight)


       ##################remove later #print topLeft, bottomRight
        #Reassigning Old Coordinates
        prevTL = topLeft
        prevBR = bottomRight
        
        #Drawing The Bar
        draw.rectangle((topLeft,bottomRight),fill = barColor)

        #Writing The Percentages
        text = str(percents[val])+"%"
        textsize= draw.textsize(text,font)

        draw.text((barsImg.size[0]/2 +20,topLeft[1]+(textsize[1]+rectHeight)/8 ),text,fill=textColor,font=font)

        
        #Placing Emojis/Other Text
           
        val = val.replace(":",';')
        #Changing unicode escape text into emoji shortcode
        emojized =  emoji.demojize(unicode(val).encode("unicode-escape"))
        emojized = emoji.demojize(val)
        
        #Starting coordinates
        xDistance = bottomRight[0] +100
        yDistance = (topLeft[1]+(textsize[1]+rectHeight)/8)

        #Splitting on : (this denoates shortcodes)
        for a in emojized.split(":"):

            #Back into unicode escape characters
            c =  emoji.emojize(":"+a+":").encode("unicode-escape")

            #Checking if emoji file exists
            result =  paths.get(c)

            #There was no emoji
            if not result:

                #Removing ":" on either side of the string
                word = c[1:-1]

                #Easier Visualization of what the character actually is
                if word == "" and len(emojized) ==0 :
                    word = "[None]"
                elif word == " " and len(emojized) ==1 :
                    word = "[Space]"

                word = word.decode("unicode-escape")
                
                #Writing Text 
                draw.text((xDistance,yDistance),word,fill=textColor,font=font)
                #Increasing coordinate for next bit of text
                xDistance+=draw.textsize(word,font)[0]
            #There was an emoji
            else:
                #Loading Emoji Picture
                emoji2paste = Image.open(result)
                emjPix = emoji2paste.load()

                #Changing Empty pixels to background color
                for x in range(emoji2paste.size[0]):
                    for y in range(emoji2paste.size[1]):
                        if emjPix[x,y][3] <= 15:
                            emjPix[x,y] = backgroundColor
                #Putting the emoji onto the image
                barsImg.paste(emoji2paste,(int(xDistance),int(yDistance)))
                #Increasing coordinate for next bit of text
                xDistance+=72



        
            
    




    #meirl (left) side

    #Removing Specific Characters From counts, comment this section out to include them
    '''
    try:
        del current["meirl"][""]
    except:
        pass
    try:
        del current["meirl"][" "]
    except:
        pass
    try:
        del current["meirl"]["_"]
    except:
        pass
    '''

    #Getting The Total For The Month
    countSum = float(0)
    for a in current["meirl"]:
        countSum += current["meirl"][a]

    #Calculating Percents and Putting Them Into Separate Dictionary
    percents = {}
    for a in current["meirl"]:
        percents[a] = float("{0:.2f}".format(current["meirl"][a] / countSum * 100))


    #Ordering Values Greatest to Smallest
    ordered = sorted([x for x in percents], key=lambda x:percents[x],reverse=True)

    #Cutting Off Extra Values
    ordered = ordered[:maxNumBars]



    #Starting Cooordinates
    prevTR = (barsImg.size[0]/2-midBarWidth/2 -300,0 -(rectSpacing+rectHeight))
    prevBL = (barsImg.size[0]/2  -300, rectHeight -(rectSpacing+rectHeight))

    #Initializing Font
    font = ImageFont.truetype("Helvetica.ttf", size=rectHeight/2)
    font = ImageFont.truetype("Symbola.ttf", size=rectHeight/2)
    
    #Going Through Each Value
    for val in ordered:

        #The New Coordinates
        topRight = (prevTR[0],prevTR[1]+rectSpacing+rectHeight)
        bottomLeft = (prevTR[0] - (percents[val] / 100 * maxRectWidth),prevBL[1]+rectSpacing+rectHeight)

        #################remove laterprint topRight,bottomLeft
        
        #Reassigning Old Coordinates
        prevTR = topRight
        prevBL = bottomLeft
        
        
        #Drawing The Bar
        draw.rectangle((topRight,bottomLeft),fill = barColor)

        #Writing The Percentages
        text = str(percents[val])+"%"
        textsize= draw.textsize(text,font)

        draw.text((barsImg.size[0]/2-textsize[0] - 20,topRight[1]+(textsize[1]+rectHeight)/8 ),text,fill=textColor,font=font)


        #Placing Emojis/Other Text
        
           
        val = val.replace(":",';')
        #Changing unicode escape text into emoji shortcode
        emojized =  emoji.demojize(unicode('"'+val+'"').encode("unicode-escape"))
        emojized = emoji.demojize(val)
        
        #Starting coordinates
        xDistance = bottomLeft[0] -100
        yDistance = topRight[1]+(textsize[1]+rectHeight)/8 

        #Splitting on : (this denoates shortcodes)
        for a in emojized.split(":"):

            #Back into unicode escape characters
            c =  emoji.emojize(":"+a+":").encode("unicode-escape")

            #Checking if emoji file exists
            result =  paths.get(c)

            #There was no emoji
            if not result:

                #Removing ":" on either side of the string
                word = c[1:-1]

                #Easier Visualization of what the character actually is 
                if word == "" and len(emojized) ==0 :
                    word = "[None]"
                elif word == " " and len(emojized) ==1 :
                    word = "[Space]"
                
                word = word.decode("unicode-escape")
                
                
                textsize = draw.textsize(word,font)

                
                
                #Writing Text 
                draw.text((xDistance-textsize[0],yDistance),word,fill=textColor,font=font)
                #Increasing coordinate for next bit of text
                xDistance-=draw.textsize(word,font)[0]
            #There was an emoji
            else:
                #Loading Emoji Picture
                emoji2paste = Image.open(result)
                emjPix = emoji2paste.load()

                #Changing Empty pixels to background color
                for x in range(emoji2paste.size[0]):
                    for y in range(emoji2paste.size[1]):
                        if emjPix[x,y][3] <= 15:
                            emjPix[x,y] = backgroundColor
                #Putting the emoji onto the image
                barsImg.paste(emoji2paste,(int(xDistance)-72,int(yDistance)))
                #Increasing coordinate for next bit of text
                xDistance-=72







    #On to Full Image

    #Pasting Bars
    pasteCoords = ((full.size[0] - barsImg.size[0]) / 2,int((full.size[1] - barsImg.size[1] )* .75))
    pasteCoords = (0,int((full.size[1] - barsImg.size[1] )* .75))
    full.paste(barsImg,pasteCoords)


    #Writing Title
    font = ImageFont.truetype("Helvetica.ttf", size=148)
    text = "The Most Common Middle Characters"

    textsize= draw.textsize(text,font)

    drawfull.text(((full.size[0]-textsize[0])/2, barsImg.size[1]/32),text,fill=textColor,font=font)
    text = "in MeIrl Titles"
    textsize= draw.textsize(text,font)
    drawfull.text(((full.size[0]-textsize[0])/2, barsImg.size[1]/10),text,fill=textColor,font=font)


    #Writing Date
    font.size = 148
    text = "2018-02"
    text = date

    textsize= draw.textsize(text,font)
    drawfull.text(((full.size[0]-textsize[0])/2, pasteCoords[1] - full.size[1] / 16),text,fill=textColor,font=font)

    #Writing Subreddit Labels

    text = "r/meirl"
    textsize= draw.textsize(text,font)
    drawfull.text(((full.size[0]-textsize[0])/4, pasteCoords[1] - full.size[1] / 16),text,fill=textColor,font=font)

    text = "r/me_irl"
    textsize= draw.textsize(text,font)
    drawfull.text(((full.size[0]- textsize[0]) *3/4 , pasteCoords[1] - full.size[1] / 16),text,fill=textColor,font=font)

    #Saving Frame
    #full.show()
    full.save("overall.png".format(frameCounter))

    #Logging Progress
    print ("Done Frame:",frameCounter)
    frameCounter+=1

    
