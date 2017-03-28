import time, os
import re
import json
import thread
import collections
from DataStructures import *
from MouseControls import *
from Tkinter import *
from threading import *


def getNameByID(id): # DEBUG
    with open('cards.json') as data_file:    
        data = json.load(data_file)
    for i in range(len(data)):
        if "name" in data[i] and data[i]["id"] == id:
            return data[i]["name"]
            break
    else:
        return "NONE"

#Set the filename and open the file
filename = 'C:\Program Files (x86)\Hearthstone\Logs\Power.log'
filename1 = 'C:\Program Files (x86)\Hearthstone\Logs\Zone.log'
file = open(filename,'r')
file1 = open(filename1,'r')

#Find the size of the file and move to the end
file.seek(os.stat(filename)[6])
file1.seek(os.stat(filename1)[6])


p_changeTag = r"TAG_CHANGE Entity=((.name=(?P<name>[^\]]*) id=(?P<id>\d*).*cardId=(?P<cardId>.*) player=.*)|((?P<label>[a-zA-Z]+))) tag=(?P<tagName>.*) value=(?P<value>.*)"

p_playCard = r"PowerTaskList.DebugPrintPower.. - BLOCK_START BlockType=POWER Entity=.name=(?P<name>.{1,30}) id=(?P<id>\d*) zone=(?P<zone>.{1,10}) zonePos=(?P<zonePos>.) cardId=(?P<cardId>.{1,20}) player=1.*"
p_blockEnd = r".*BLOCK_END.*"


p_toFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*to FRIENDLY HAND"
p_fromFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY HAND"


p_showEntity = r".*SHOW_ENTITY - Updating Entity=((?P<id>\d*)|.*id=(?P<id1>\d*)).*CardID=(?P<cardId>.{1,20})"
p_setTag = r"         tag=(?P<tagName>.*) value=(?P<value>.*)"


shownEntity = Card(None, None)

transitCards = []

playerHand = PlayerHand()
playerBoard = PlayerBoard()

print

Tags = collections.defaultdict(dict)

root = Tk()
ed = Entry(root)
ed.pack()
bt2 = Button(root)
bt2.pack()
bt2["text"] = "Print all tags"

bt1 = Button(root)
bt1.pack()
bt1["text"] = "Print minions"


bt3 = Button(root)
bt3.pack()
bt3["text"] = "Print all hand cards"

def printMinions(event):
    playerBoard.printMinionsNames()

def printAllTags(event):
    for key, value in Tags[ed.get()].iteritems():
        print key + ": " + value
        

def printHandCards(event):
    playerHand.printCardsNames()
        
bt1.bind("<Button-1>", printMinions)
bt2.bind("<Button-1>", printAllTags)
bt3.bind("<Button-1>", printHandCards)


thread = Thread(target = root.mainloop, args = ())
thread.start()

f = "0"
mulligan = "2"

while 1:
    
    where1 = file1.tell()
    line1 = file1.readline()
    where = file.tell()
    line = file.readline() + line1
    
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        changeTag = re.search(p_changeTag, line)
        playCard = re.search(p_playCard, line)
        blockEnd = re.search(p_blockEnd, line)
        toFriendlyHand = re.search(p_toFriendlyHand, line)
        fromFriendlyHand = re.search(p_fromFriendlyHand, line)
        showEntity = re.search(p_showEntity, line)
        setTag = re.search(p_setTag, line)
        
        #print line
        
        if (showEntity):
            if (showEntity.group("id")):
                shownEntity = Card(showEntity.group("cardId"), showEntity.group("id"))
                #playerHand.addCard(shownEntity)
            else:
                shownEntity = Card(showEntity.group("cardId"), showEntity.group("id1"))
                """if (mulligan == "0"):
                    playerHand.addCard(shownEntity)
                else:
                    playerHand.mulliganAdd(shownEntity)"""
                    
                
            #print shownEntity.getName() + " " + shownEntity.id
        
        if (setTag and shownEntity != Card(None, None)):
            Tags[shownEntity.id][setTag.group("tagName")] = setTag.group("value")
        
        
        if (playCard): 
            Tags[playCard.group("id")]["cardId"] = playCard.group("cardId")
            Tags[playCard.group("id")]["zone"] = playCard.group("zone")
            Tags[playCard.group("id")]["zonePos"] = playCard.group("zonePos")
            if (playCard.group("zonePos") != "0"):
                playerBoard.addMinion(Minion(playCard.group("cardId"), playCard.group("id")), playCard.group("zonePos"))
            #print playCard.group("name") + " " + playCard.group("id") + ": " + playCard.group("zone") + " " + playCard.group("zonePos")
        
            #playerHand.printCardsNames()
       
        
        if (changeTag):
            if (changeTag.group("id")):
                Tags[(changeTag.group("id"))][changeTag.group("tagName")] = changeTag.group("value")
                
                minionIndex = playerBoard.getMinionIndex(Minion(changeTag.group("cardId"), changeTag.group("id")))
                
                if (changeTag.group("tagName") == "ATK" and isinstance(playerBoard.minionsList[minionIndex], Minion)):
                    playerBoard.minionsList[minionIndex].attack = int(changeTag.group("value"))
                
                if (changeTag.group("tagName") == "DAMAGE" and isinstance(playerBoard.minionsList[minionIndex], Minion)):
                    playerBoard.minionsList[minionIndex].health = playerBoard.minionsList[minionIndex].getHealth() - int(changeTag.group("value"))
                
                """if (changeTag.group("tagName") == "ZONE" and changeTag.group("value") == "DECK"):
                    if (mulligan == "0"):
                        playerHand.removeCard(Card(changeTag.group("cardId"), changeTag.group("id")))
                    else:
                        playerHand.mulliganCard(Card(changeTag.group("cardId"), changeTag.group("id")))"""
                        
                    
                if (changeTag.group("tagName") == "ZONE" and changeTag.group("value") == "GRAVEYARD"):
                    playerBoard.removeMinion(Minion(changeTag.group("cardId"), changeTag.group("id")))
            #if (changeTag.group("tagName") == "ZONE_POSITION"):
                #print changeTag.group("name") + " " + changeTag.group("id") + ": " + changeTag.group("tagName") + " = " + changeTag.group("value")
            else:
                Tags[(changeTag.group("label"))][changeTag.group("tagName")] = changeTag.group("value")
                
                if (changeTag.group("tagName") == "MULLIGAN_STATE" and changeTag.group("value") == "DONE"):
                    mulligan = str(max(0, int(mulligan) - 1))
                    print mulligan
                #print changeTag.group("label") + ": " + changeTag.group("tagName") + " = " + Tags[(changeTag.group("label"))][changeTag.group("tagName")]
                
        if fromFriendlyHand:
            if mulligan == "0":
                playerHand.removeCard(Card(fromFriendlyHand.group("cardId"), fromFriendlyHand.group("id")))
            else:
                playerHand.mulliganCard(Card(fromFriendlyHand.group("cardId"), fromFriendlyHand.group("id")))
            #print "- " + Card(fromFriendlyHand.group("cardId"), fromFriendlyHand.group("id")).getName()
                
        if toFriendlyHand:
            if (mulligan == "0"):
                playerHand.addCard(Card(toFriendlyHand.group("cardId"), toFriendlyHand.group("id")))
            else:
                playerHand.addCard(Card(toFriendlyHand.group("cardId"), toFriendlyHand.group("id")))
            #print "+ " + Card(toFriendlyHand.group("cardId"), toFriendlyHand.group("id")).getName()
            
            
                
            