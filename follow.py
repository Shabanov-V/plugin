import time, os
import re
import json
from DataStructures import *

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

p_drawCard = r"name=(.*) id=.*to FRIENDLY HAND"
p_playCreature = r"name=(.*) id=.*FRIENDLY HAND -> FRIENDLY PLAY"
p_playSpell = r"name=(.*) id=.*from FRIENDLY HAND -> $"
p_died = r"name=(.*) id=.*from FRIENDLY PLAY -> FRIENDLY GRAVEYARD"

p_toFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*to FRIENDLY HAND"
p_fromFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY HAND"

p_posNumberChange = r".*cardId=(.*) player=1] pos from (. -> .)"

p_turnStart = r"GameState.*tag=TURN value=(?P<number>\d*)"

playerHand = PlayerHand()

isGotCoin = False

def f(line):
    global isGotCoin
    toFriendlyHand = re.search(p_toFriendlyHand, line)
    fromFriendlyHand = re.search(p_fromFriendlyHand, line)
    turnStart = re.search(p_turnStart, line)
    
    if (playerHand.isHaveCard("GAME_005")):
        isGotCoin = True
    if turnStart:
        if ((isGotCoin and int(turnStart.group("number")) % 2 == 0) or ((not isGotCoin) and int(turnStart.group("number")) % 2 == 1)):
            print "YOUR TURN!!! Number: " + str(int(turnStart.group("number")) / 2) + "   //" + turnStart.group("number")
    if toFriendlyHand:
        playerHand.addCard(Card(toFriendlyHand.group("cardId"), toFriendlyHand.group("id")))
        playerHand.printCardsNames()
    if fromFriendlyHand:
        playerHand.removeCard(Card(fromFriendlyHand.group("cardId"), fromFriendlyHand.group("id")))
        playerHand.printCardsNames()

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
        
        if (playerHand.isHaveCard("GAME_005")):
            isGotCoin = True
        if turnStart:
            #print "Turn start"
            if ((isGotCoin and int(turnStart.group("number")) % 2 == 0) or ((not isGotCoin) and int(turnStart.group("number")) % 2 == 1)):
                print "YOUR TURN!!! Number: " + str(int(turnStart.group("number")) / 2)# + "   //" + turnStart.group("number")
                print isGotCoin
        if toFriendlyHand:
            playerHand.addCard(Card(toFriendlyHand.group("cardId"), toFriendlyHand.group("id")))
            playerHand.printCardsNames()
        if fromFriendlyHand:
            playerHand.removeCard(Card(fromFriendlyHand.group("cardId"), fromFriendlyHand.group("id")))
            playerHand.printCardsNames()