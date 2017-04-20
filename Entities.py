from Interfaces import IAlterationEntity
from Classes import *
from RegExps import *
import re

class myHandCards(IAlterationEntity):
    hand_cards = []

    def __init__(self):
        self.hand_cards = []

    def debugPrintShit(self):
        print "******************"
        for item in self.hand_cards:
            print item.name

    def add_card_to_hand(self, hand_pos, card):
        self.hand_cards.insert(hand_pos, card)

    def del_card_from_hand(self, special_id):
        self.hand_cards = [card for card in self.hand_cards if card.special_id != special_id]

    def change_card_position(self, special_id, new_pos):
        temp_card = next((card for card in self.hand_cards if card.special_id == special_id), None)
        if temp_card == None:
            return
        self.hand_cards.remove(temp_card)
        self.hand_cards.insert(new_pos, temp_card)

    def checkNChange(self, logLine):
        played_card = re.search(regExps.from_friendly_hand, logLine)
        drawed_card = re.search(regExps.to_friendly_hand, logLine)
        changed_position = re.search(regExps.change_card_position, logLine)
        if played_card:
            self.del_card_from_hand(played_card.group("id"))
            self.debugPrintShit()
        if drawed_card:
            self.add_card_to_hand(int(drawed_card.group("zonePos")), Card(drawed_card.group("cardId"), drawed_card.group("id")))
            self.debugPrintShit()
        if changed_position:
            print logLine
            self.change_card_position(changed_position.group("id"), int(changed_position.group("pos_2")))