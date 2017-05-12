from Interfaces import IAlterationEntity
from Classes import *
from RegExps import *
import re


class playersInfo(IAlterationEntity):
    # Needs Zone
    my_id = int
    my_name = str
    opp_id = int
    opp_name = str

    __waiting_for_opp_name__ = bool

    def __init__(self):
        self.__waiting_for_opp_name__ = False
        self.my_name = ""
        self.opp_name = ""

    def debug_print_shit(self):
        print "My name: " + self.my_name
        print "Opponent name: " + self.opp_name

    def check_n_change(self, logLine):
        to_friendly_hand = re.search(regExps.smth_to_friendly_hand, logLine)
        to_opposing_hand = re.search(regExps.smth_to_opposing_hand, logLine)
        player_name_n_id = re.search(regExps.player_name_n_id, logLine)
        if to_friendly_hand:
            self.__waiting_for_opp_name__ = False
        if to_opposing_hand:
            self.__waiting_for_opp_name__ = True
        if player_name_n_id and self.__waiting_for_opp_name__:
            self.opp_id = player_name_n_id.group("id")
            self.opp_name = player_name_n_id.group("name")
            self.debug_print_shit()
        if player_name_n_id and not(self.__waiting_for_opp_name__):
            self.my_id = player_name_n_id.group("id")
            self.my_name = player_name_n_id.group("name")


class myHeroPower(IAlterationEntity):
    # Needs Power
    is_available = bool
    players_info = playersInfo

    def debug_print_shit(self):
        print "my heropower " + str(self.is_available)

    def __init__(self, players_info):
        self.is_available = True
        self.players_info = players_info

    def check_n_change(self, logLine):
        num_of_activations_this_turn = re.search(regExps.hero_power_activations.replace("(name)", self.players_info.my_name), logLine)
        if num_of_activations_this_turn:
            self.is_available = True if int(num_of_activations_this_turn.group("value")) == 0 else False
            self.debug_print_shit()


class opponentHeroPower(IAlterationEntity):
    # Needs Power
    is_available = bool
    players_info = playersInfo

    def debug_print_shit(self):
        print "opponent heropower " + str(self.is_available)

    def __init__(self, players_info):
        self.is_available = True
        self.players_info = players_info

    def check_n_change(self, logLine):
        num_of_activations_this_turn = re.search(regExps.hero_power_activations.replace("(name)", self.players_info.opp_name), logLine)
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
        print '\n'.join(str(item.name) + " " + str(item.attack) + "\\" + str(item.health) + " manacost: " + str(item.mana_cost) for item in self.hand_cards)

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

    def tag_change(self, tag_name, value, special_id):
        card_pos = None
        for i in range(0, len(self.hand_cards)):
            if self.hand_cards[i].special_id == special_id:
                card_pos = i
        if card_pos == None:
            return
        if tag_name == "ATK":
            self.hand_cards[card_pos].attack = int(value)
        if tag_name == "HEALTH":
            self.hand_cards[card_pos].health = int(value)
        if tag_name == "TAG_LAST_KNOWN_COST_IN_HAND":
            self.hand_cards[card_pos].mana_cost = int(value)

    def check_n_change(self, logLine):
        played_card = re.search(regExps.from_friendly_hand, logLine)
        drawed_card = re.search(regExps.to_friendly_hand, logLine)
        changed_position = re.search(regExps.change_card_position, logLine)
        tag_change = re.search(regExps.tag_change, logLine)
        if played_card:
            self.del_card_from_hand(int(played_card.group("id")))
            self.debug_print_shit()
        if drawed_card:
            self.add_card_to_hand(Card(drawed_card.group("cardId"), int(drawed_card.group("id"))))
            self.debug_print_shit()
        if changed_position:
            self.change_card_position(changed_position.group("id"), int(changed_position.group("pos_2")))
        if tag_change:
            self.tag_change(tag_change.group("tag"), tag_change.group("value"), int(tag_change.group("id")))
            
            
class board(IAlterationEntity):
    minions = [Minion(None, None)] * 10
    def __init__(self):
        self.minions = [Minion(None, None)] * 10
        
    def addMinion(self, minion, dstPos):
        if minion.type != "MINION":
            return
        dstPos = int(dstPos)
        if dstPos == len(self.minions) or dstPos == 0:
            self.minions[dstPos] = minion
        else:
            for i in range(7, dstPos, -1):
                self.minions[i] = self.minions[i - 1]
            self.minions[dstPos] = minion 
                
    
    def get_minion_index_by_id(self, special_id):
        for i in range(len(self.minions)):
            if isinstance(self.minions[i], Minion) and self.minions[i].special_id == special_id:
                return i
                break
        else:
            return None
    
    def getMinionIndex(self, minion):
        return self.get_minion_index_by_id(minion.special_id)
    
    def removeMinionByIndex(self, index):
        if index == None:
            return
        if index == 0:
            self.minions[index] = Minion(None, None)
            return
        for i in range(index, 7):
            self.minions[i] = self.minions[i + 1]
        self.minions[7] = Minion(None, None)
        
    def removeMinion(self, minion):
        self.removeMinionByIndex(self.getMinionIndex(minion))
        
    def debug_print_shit(self):
        print "******************"
        
        for i in range(len(self.minions)):
            if isinstance(self.minions[i], Minion):
                print str(self.minions[i].name) + " " + str(self.minions[i].special_id)
    
    def change_position(self, special_id, dstPos):
        ti = self.get_minion_index_by_id(special_id)
        if ti == None:
            return
        t = self.minions[ti]
        if t == None:
            return
        self.removeMinionByIndex(ti)
        self.addMinion(t, dstPos)
    
    def check_n_change(self, logLine):
        minionPlay = re.search(regExps.minionPlay2, logLine)
        minionChangePosition = re.search(regExps.minionChangePosition1, logLine)
        died = re.search(regExps.died, logLine)
        if died:
            self.removeMinion(Minion(died.group("cardId"), int(died.group("id"))))
            self.debug_print_shit()
        if minionPlay:
            self.addMinion(Minion(minionPlay.group("cardId"), minionPlay.group("id")), minionPlay.group("dstPos"))
            print "lol"
            self.debug_print_shit()
        if minionChangePosition:
            self.change_position(minionChangePosition.group("id"), int(minionChangePosition.group("dstPos")))
            print "lol"
            self.debug_print_shit()