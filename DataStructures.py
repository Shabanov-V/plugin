import math, json


class Point:
    
    
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    


class Rect:

    """A rectangle identified by two points.

    The rectangle stores left, top, right, and bottom values.

    Coordinates are based on screen coordinates.

    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom
    """

    def __init__(self, (left, top, right, bottom)):
        """Initialize a rectangle from four ints."""
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

class Card:
    
    def __init__(self, cardId, id):
        self.cardId = cardId
        self.id = id

    def getName(self):
        with open('cards.json') as data_file:    
            data = json.load(data_file)
        for i in range(len(data)):
            if "name" in data[i] and data[i]["id"] == self.cardId:
                return data[i]["name"]
                break
        else:
            return "NONE"
        
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
        
class PlayerHand:
    def __init__(self):
        self.cardsList = []
        
    def addCard(self, card): #add card in the right position
        self.cardsList.append(card)
        
    def addCardByIds(self, cardId, id):
        self.addCard(Card(cardId, id))
        
    def addListOfCards(self, cardsList):
        for i in cardsList:
            self.addCard(i)
    
    def printCardsNames(self):
        for i in self.cardsList:
            print i.getName() + ", ",
        else:
            print
    
    def getCardIndex(self, card): #find card position in the player hand
        for i in range(len(self.cardsList)):
            if self.cardsList[i] == card:
                return i + 1
                break
        else:
            return 0
        
    def getCardByIndex(self, ind):
        self.cardsList[ind - 1]
        
    def removeCardByIndex(self, ind):
        del self.cardsList[ind - 1]
    
    def removeCard(self, card):
        self.removeCardByIndex(self.getCardIndex(card))
        
    def isInHand(self, cardId):
        for i in self.cardsList:
            if i.cardId == cardId:
                return True
        return False

class Minion:
    def __init__(self, cardId, id):
        self.cardId = cardId
        self.id = id
        
    def getName(self):
        with open('cards.json') as data_file:    
            data = json.load(data_file)
        for i in range(len(data)):
            if "name" in data[i] and data[i]["id"] == self.cardId:
                return data[i]["name"]
                break
        else:
            return "NONE"
        
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
        
class PlayerBoard:
    def __init__(self):
        self.minionsList = [0] * 8
        self.minionsCount = 0
    
    def addMinion(self, minion, dstPos):
        if dstPos == "0":
            return
        self.minionsCount += 1
        dstPos = int(dstPos)
        if (dstPos == self.minionsCount):
            self.minionsList[dstPos] = minion
        else:
            for i in range(7, dstPos, -1):
                self.minionsList[i] = self.minionsList[i - 1]
            self.minionsList[dstPos] = minion 
                
    
        
    def printMinionsNames(self):
        for i in range(len(self.minionsList)):
            if isinstance(self.minionsList[i], Minion):
                print self.minionsList[i].getName() + " " + str(i)
        else:
            print
            
    def getMinionIndex(self, minion):
        #print "Find: (" + str(minion.cardId) + ", " + str(minion.id) + ")"
        for i in range(len(self.minionsList)):
            #print "---> (" + str(self.minionsList[i].cardId) + ", " + str(self.minionsList[i].id) + ")"
            if isinstance(self.minionsList[i], Minion) and self.minionsList[i] == minion:
                return i
                break
        else:
            return 0
    
    def removeMinionByIndex(self, index):
        if index == 0:
            return
        for i in range(index, 7):
            self.minionsList[i] = self.minionsList[i + 1]
        self.minionsList[7] = 0
        
    def removeMinion(self, minion):
        self.removeMinionByIndex(self.getMinionIndex(minion))