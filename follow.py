import time, os
import re
import json
from DataStructures import *

def getNameByID(id):
    with open('cards.json') as data_file:    
        data = json.load(data_file)
    for i in range(len(data)):
        if "name" in data[i] and data[i]["id"] == id:
            return data[i]["name"]
            break
    else:
        return "NONE"
              

#Set the filename and open the file
filename = 'C:\Program Files (x86)\Hearthstone\Logs\Zone.log'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

p_drawCard = r"name=(.*) id=.*to FRIENDLY HAND"
p_playCreature = r"name=(.*) id=.*FRIENDLY HAND -> FRIENDLY PLAY"
p_playSpell = r"name=(.*) id=.*from FRIENDLY HAND -> $"
p_died = r"name=(.*) id=.*from FRIENDLY PLAY -> FRIENDLY GRAVEYARD"

p_toFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*to FRIENDLY HAND"
p_fromFriendlyHand = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY HAND"

p_posNumberChange = r".*cardId=(.*) player=1] pos from (. -> .)"

playerHand = PlayerHand()

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        draws = re.search(p_drawCard, line)
        playCreatures = re.search(p_playCreature, line)
        playSpells = re.search(p_playSpell, line)
        dieds = re.search(p_died, line)
        toFriendlyHand = re.search(p_toFriendlyHand, line)
        fromFriendlyHand = re.search(p_fromFriendlyHand, line)
        posNumberChange = re.search(p_posNumberChange, line)
        if toFriendlyHand:
            playerHand.addCard(Card(toFriendlyHand.group("cardId"), toFriendlyHand.group("id")))
            print "+" + getNameByID(toFriendlyHand.group("cardId"))
            playerHand.printCardsNames()
        if fromFriendlyHand:
            playerHand.removeCard(Card(fromFriendlyHand.group("cardId"), fromFriendlyHand.group("id")))
            print "-" + getNameByID(fromFriendlyHand.group("cardId"))
            playerHand.printCardsNames()