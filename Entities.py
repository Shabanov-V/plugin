from Interfaces import IAlterationEntity
from Classes import *
from RegExps import *
import re


class playersInfo(IAlterationEntity):
    # Needs Zone
    my_id = int
    my_name = "Grig0510"
    opp_id = int
    opp_name = str

    __flag__ = bool

    def __init__(self):
        self.__flag__ = False
        self.my_name = ""
        self.opp_name = ""

    def debug_print_shit(self):
        print "My name: " + self.my_name
        print "Opponent name: " + self.opp_name

    def check_n_change(self, logLine):
        print
        # Flag == True => waiting for my name, otherwise opposing
        # I tried :c


class myHeroPower(IAlterationEntity):
    # Needs Power
    is_available = bool

    def debug_print_shit(self):
        print str(self.is_available)

    def __init__(self):
        self.is_available = True
        self.my_name = ""

    def check_n_change(self, logLine):
        num_of_activations_this_turn = re.search(regExps.hero_power_activations.replace("(name)", playersInfo.my_name), logLine)
        if num_of_activations_this_turn:
            self.is_available = True if int(num_of_activations_this_turn.group("value")) == 0 else False
            self.debug_print_shit()


class opponentHandCards(IAlterationEntity):
    # Needs only Zone
    num_of_cards = int

    def __init__(self):
        self.num_of_cards = 0

    def debug_print_shit(self):
        print self.num_of_cards

    def check_n_change(self, logLine):
        to_hand = re.search(regExps.to_opposing_hand, logLine)
        from_hand = re.search(regExps.from_opposing_hand, logLine)
        if to_hand:
            self.num_of_cards += 1
            self.debug_print_shit()
        if from_hand:
            self.num_of_cards -= 1
            self.debug_print_shit()


class myHandCards(IAlterationEntity):
    # Needs only Zone
    hand_cards = []

    def __init__(self):
        self.hand_cards = []

    def debug_print_shit(self):
        print "******************"
        print '\n'.join(str(item.name) for item in self.hand_cards)

    def add_card_to_hand(self, card):
        self.hand_cards.append(card)

    def del_card_from_hand(self, special_id):
        self.hand_cards = [card for card in self.hand_cards if card.special_id != special_id]

    def change_card_position(self, special_id, new_pos):
        temp_card = next((card for card in self.hand_cards if card.special_id == special_id), None)
        if temp_card == None:
            return
        self.hand_cards.remove(temp_card)
        self.hand_cards.insert(new_pos, temp_card) # -1

    def check_n_change(self, logLine):
        played_card = re.search(regExps.from_friendly_hand, logLine)
        drawed_card = re.search(regExps.to_friendly_hand, logLine)
        changed_position = re.search(regExps.change_card_position, logLine)
        if played_card:
            self.del_card_from_hand(played_card.group("id"))
            self.debug_print_shit()
        if drawed_card:
            self.add_card_to_hand(Card(drawed_card.group("cardId"), drawed_card.group("id")))
            self.debug_print_shit()
        if changed_position:
            self.change_card_position(changed_position.group("id"), int(changed_position.group("pos_2")))