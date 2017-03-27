import time, os
import re
import json
import thread
from DataStructures import *
from MouseControls import *



def getNameByID(id): # DEBUG
    with open('cards.json') as data_file:    
        data = json.load(data_file)
    for i in range(len(data)):
        if "name" in data[i] and data[i]["id"] == id:
            return data[i]["name"]
            break
    else:
        return "NONE"
              

def sleepAndMoveToCard(card, playerHand):
    time.sleep(5)
    MoveToCard(card, playerHand)
              
#Set the filename and open the file
filename = 'C:\Program Files (x86)\Hearthstone\Logs\Power.log'
filename1 = 'C:\Program Files (x86)\Hearthstone\Logs\Zone.log'
file = open(filename,'r')
file1 = open(filename1,'r')

#Find the size of the file and move to the end
file.seek(os.stat(filename)[6])
file1.seek(os.stat(filename1)[6])

p_drawCard = r"name=(.*) id=.*to FRIENDLY HAND"
p_playCreature = r"name=(.*) id=.*FRIENDLY HAND -> FRIENDLY PLAY"
p_playSpell = r"name=(.*) id=.*from FRIENDLY HAND -> $"

p_toFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*to FRIENDLY HAND"
p_fromFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY HAND"

p_posNumberChange = r".*cardId=(.*) player=1] pos from (. -> .)"

p_turnStart = r"GameState.*tag=TURN value=(?P<number>\d*)"


p_minionPlay = r"ZoneMgr.CreateLocalChangesFromTrigger().*name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*dstZoneTag=PLAY dstPos=(?P<dstPos>\d)"
p_died = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY PLAY -> FRIENDLY GRAVEYARD"
p_minionChangePosition = r"ZoneMgr.*id=(?P<id>\d*).*zone=PLAY.*zonePos (?P<from>\d*) -> (?P<to>\d*)"

playerHand = PlayerHand()
playerBoard = PlayerBoard()

isGotCoin = False


while 1:
    where1 = file1.tell()
    line1 = file1.readline()
    where = file.tell()
    line = file.readline() + line1
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        toFriendlyHand = re.search(p_toFriendlyHand, line)
        fromFriendlyHand = re.search(p_fromFriendlyHand, line)
        turnStart = re.search(p_turnStart, line)
        minionPlay = re.search(p_minionPlay, line)
        minionChangePosition = re.search(p_minionChangePosition, line)
        died = re.search(p_died, line)
        
        if died:
            playerBoard.removeMinion(Minion(died.group("cardId"), died.group("id")))
            playerBoard.printMinionsNames()
        if minionPlay:
            playerBoard.addMinion(Minion(minionPlay.group("cardId"), minionPlay.group("id")), minionPlay.group("dstPos"))
            playerBoard.printMinionsNames()
        
        if toFriendlyHand:
            playerHand.addCard(Card(toFriendlyHand.group("cardId"), toFriendlyHand.group("id")))
            playerHand.printCardsNames()
        if fromFriendlyHand:
            playerHand.removeCard(Card(fromFriendlyHand.group("cardId"), fromFriendlyHand.group("id")))
            playerHand.printCardsNames()
            
        if (playerHand.isInHand("GAME_005")):
            isGotCoin = True
        if turnStart:
            #print "Turn start"
            if ((isGotCoin and int(turnStart.group("number")) % 2 == 0) or ((not isGotCoin) and int(turnStart.group("number")) % 2 == 1)):
                if (int(turnStart.group("number"))) / 2 >= 1:
                    pass#thread.start_new_thread(sleepAndMoveToCard, (playerHand.cardsList[0], playerHand))
                print "YOUR TURN!!! Number: " + str(int(turnStart.group("number")) / 2)# + "   //" + turnStart.group("number")