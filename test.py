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
file = open(filename,'r')

#Find the size of the file and move to the end
file.seek(os.stat(filename)[6])

p_minionPlay = r"ZoneChangeList.ProcessChanges.*name=(?P<name>[^\]]*) id=(?P<id>\d*) zone=PLAY.* cardId=(?P<cardId>.*) player=2.*dstPos=(?P<dstPos>\d)"
p_transitCard = r"TRANSITIONING.*name=(?P<name>[^\]]*) id=(?P<id>\d*).*cardId=(?P<cardId>.*) player=.* to FRIENDLY PLAY"


p_died = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY PLAY -> FRIENDLY GRAVEYARD"
p_minionChangePosition = r"ZoneChangeList.ProcessChanges().*local=.*name=(?P<name>[^\]]*) id=(?P<id>\d*) zone=.*zonePos=(?P<zonePos>\d*) cardId=(?P<cardId>.*) player=.* pos from \d -> \d"


p_changeTag = r"TAG_CHANGE Entity=((.name=(?P<name>[^\]]*) id=(?P<id>\d*).*cardId=(?P<cardId>.*) player=.*)|((?P<label>[a-zA-Z]+))) tag=(?P<tagName>.*) value=(?P<value>.*)"

p_playCard = r"PowerTaskList.DebugPrintPower.. - BLOCK_START BlockType=POWER Entity=.name=(?P<name>.{1,30}) id=(?P<id>\d*) zone=(?P<zone>.{1,10}) zonePos=(?P<zonePos>.) cardId=(?P<cardId>.{1,20}) player=1.*"
p_blockEnd = r".*BLOCK_END.*"

transitCards = []

playerBoard = PlayerBoard()

print

Tags = collections.defaultdict(dict)

root = Tk()
ed = Entry(root)
ed.pack()
ed1 = Entry(root)
ed1.pack()
bt = Button(root)
bt.pack()
bt["text"] = "Ok"
lb = Label(root)
lb["text"] = "None"
lb.pack()
bt2 = Button(root)
bt2.pack()
bt2["text"] = "Print all tags"

bt1 = Button(root)
bt1.pack()
bt1["text"] = "Print minions"
def printer(event):
     lb["text"] = Tags[ed.get()][ed1.get()]

def printMinions(event):
    playerBoard.printMinionsNames()

def printAllTags(event):
    for key, value in Tags[ed.get()].iteritems():
        print key + ": " + value
bt.bind("<Button-1>", printer)
bt1.bind("<Button-1>", printMinions)
bt2.bind("<Button-1>", printAllTags)

thread = Thread(target = root.mainloop, args = ())
thread.start()

f = "0"

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        changeTag = re.search(p_changeTag, line)
        playCard = re.search(p_playCard, line)
        blockEnd = re.search(p_blockEnd, line)
           
        if (playCard): 
            Tags[playCard.group("id")]["cardId"] = playCard.group("cardId")
            Tags[playCard.group("id")]["zone"] = playCard.group("zone")
            Tags[playCard.group("id")]["zonePos"] = playCard.group("zonePos")
            if (playCard.group("zonePos") != "0"):
                playerBoard.addMinion(Minion(playCard.group("cardId"), playCard.group("id")), playCard.group("zonePos"))
            #print playCard.group("name") + " " + playCard.group("id") + ": " + playCard.group("zone") + " " + playCard.group("zonePos")
       
        
        if (changeTag):
            if (changeTag.group("id")):
                Tags[(changeTag.group("id"))][changeTag.group("tagName")] = changeTag.group("value")
                if (changeTag.group("tagName") == "ZONE" and changeTag.group("value") == "GRAVEYARD"):
                    playerBoard.removeMinion(Minion(changeTag.group("cardId"), changeTag.group("id")))
            #if (changeTag.group("tagName") == "ZONE_POSITION"):
                #print changeTag.group("name") + " " + changeTag.group("id") + ": " + changeTag.group("tagName") + " = " + changeTag.group("value")
            else:
                Tags[(changeTag.group("label"))][changeTag.group("tagName")] = changeTag.group("value")
                #print changeTag.group("label") + ": " + changeTag.group("tagName") + " = " + Tags[(changeTag.group("label"))][changeTag.group("tagName")]
                
            