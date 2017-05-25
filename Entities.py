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
    my_player_num = int
    opposing_player_num = int
    __waiting_for_opp_name__ = bool

    def __init__(self):
        self.__waiting_for_opp_name__ = False
        self.my_name = ""
        self.opp_name = ""

    def debug_print_shit(self):
        print "My name: " + self.my_name
        print "Opponent name: " + self.opp_name
        print "My num: " + str(self.my_player_num)
        print "Opp num: " + str(self.opposing_player_num)

    def check_n_change(self, logLine):
        to_friendly_hand = re.search(regExps.smth_to_friendly_hand, logLine)
        to_opposing_hand = re.search(regExps.smth_to_opposing_hand, logLine)
        player_name_n_id = re.search(regExps.player_name_n_id, logLine)
        my_player_num = re.search(regExps.who_is_who1, logLine)
        opp_player_num = re.search(regExps.who_is_who2, logLine)
        if to_friendly_hand:
            self.__waiting_for_opp_name__ = False
        if to_opposing_hand:
            self.__waiting_for_opp_name__ = True
        if player_name_n_id and self.__waiting_for_opp_name__:
            self.opp_id = player_name_n_id.group("id")
        if player_name_n_id and not(self.__waiting_for_opp_name__):
            self.my_id = player_name_n_id.group("id")
            self.my_name = player_name_n_id.group("name")
        if my_player_num:
            self.my_player_num = my_player_num.group("player_numb")
        if opp_player_num:
            self.opposing_player_num = opp_player_num.group("player_numb")


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
        #print '\n'.join(str(item.name) + " " + str(item.attack) + "\\" + str(item.health) + " manacost: " + str(item.mana_cost) for item in self.hand_cards)
        rows = [[str(item.name), str(item.attack), "\\" , str(item.health) , " manacost: " , str(item.mana_cost)] for item in self.hand_cards]  
        widths = [max(map(len, col)) for col in zip(*rows)]
        for row in rows:
            print "  ".join((val.ljust(width) for val, width in zip(row, widths)))
        #print '\n'.join("{: >20} {: >2} {: >0} {: >2} {: >0} {: >2}".format(*[str(item.name), str(item.attack), "\\" , str(item.health) , " manacost: " , str(item.mana_cost)])  for item in self.hand_cards)
        
    def add_card_to_hand(self, card):
        self.hand_cards.append(card)

    def del_card_from_hand(self, special_id):
        self.hand_cards = [card for card in self.hand_cards if card.special_id != special_id]

    def change_card_position(self, special_id, new_pos):
        temp_card = next((card for card in self.hand_cards if card.special_id == special_id), None)
        if temp_card == None:
            return
        self.hand_cards.remove(temp_card)
        self.hand_cards.insert(new_pos - 1, temp_card) # -1
        #print temp_card.name + " " + str(new_pos)

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
            #self.debug_print_shit()
        if drawed_card:
            self.add_card_to_hand(Card(drawed_card.group("cardId"), int(drawed_card.group("id"))))
            #self.debug_print_shit()
        if changed_position:
            self.change_card_position(int(changed_position.group("id")), int(changed_position.group("pos_2")))
        if tag_change:
            self.tag_change(tag_change.group("tag"), tag_change.group("value"), int(tag_change.group("id")))
            
            
class board(IAlterationEntity):
    minions = [Minion(None, None)] * 10
    playerNumb = 0
    isOpponent = 0
    
    def __init__(self, t):
        self.minions = [Minion(None, None)] * 10
        self.isOpponent = t
    
    def size_minions(self):
        i = 0
        for j in self.minions:
            if (j.name != None):
                i += 1
        return i
        
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
        rows = [[str(self.minions[i].name), str(self.minions[i].special_id), str(self.minions[i].attack), "/", str(self.minions[i].health), str(self.minions[i].exhausted), str(self.minions[i].frozen)] for i in range(len(self.minions))]  
        widths = [max(map(len, col)) for col in zip(*rows)]
        for row in rows:
            print "  ".join((val.ljust(width) for val, width in zip(row, widths)))
    
    def change_position(self, special_id, dstPos):
        ti = self.get_minion_index_by_id(special_id)
        if ti == None:
            return
        t = self.minions[ti]
        if t == None:
            return
        self.removeMinionByIndex(ti)
        self.addMinion(t, dstPos)
    
    def change_minion_tag(self, special_id, tag, value):
        ti = self.get_minion_index_by_id(special_id)
        if ti == None:
            return
        t = self.minions[ti]
        if (tag == "TAUNT"):
            self.minions[ti].add_mechanic(tag)
            self.minions[ti].update_mechanics()
        if (tag == "ZONE" and value == "SETASIDE"):
            self.removeMinionByIndex(ti)
        if (tag == "EXHAUSTED"):
            self.minions[ti].exhausted = value
        if (tag == "ATK"):
            self.minions[ti].attack = value
        if (tag == "DAMAGE"):
            self.minions[ti].health = self.minions[ti].maxHealth - int(value)
        if (tag == "FROZEN"):
            self.minions[ti].frozen = value
    
    def check_n_change(self, logLine):
        friendlyMinionPlay = re.search(regExps.friendly_minion_play2, logLine)
        minionChangePosition = re.search(regExps.minion_change_position2, logLine)
        oppositeMinionPlay = re.search(regExps.opposite_minion_play, logLine)
        died = re.search(regExps.died, logLine)
        whoIsWho1 = re.search(regExps.who_is_who1, logLine)
        whoIsWho2 = re.search(regExps.who_is_who2, logLine)
        MiniontagChanged1 = re.search(regExps.minion_tag_changed1, logLine)
        MiniontagChanged2 = re.search(regExps.minion_tag_changed2, logLine)
        if MiniontagChanged1:
            self.change_minion_tag(MiniontagChanged1.group("id"), MiniontagChanged1.group("tag"), MiniontagChanged1.group("value"))
        if MiniontagChanged2:
            self.change_minion_tag(MiniontagChanged2.group("id"), MiniontagChanged2.group("tag"), MiniontagChanged2.group("value"))
            
        if whoIsWho1 and self.isOpponent == 0:
            self.playerNumb = int(whoIsWho1.group("player_numb"))
        if whoIsWho2 and self.isOpponent == 1:
            self.playerNumb = int(whoIsWho2.group("player_numb"))
        if died:
            self.removeMinion(Minion(died.group("cardId"), (died.group("id"))))
            #print "111: " + died.group("cardId") + " " + died.group("id")
            #self.debug_print_shit()
        if friendlyMinionPlay and self.isOpponent == 0:
            self.addMinion(Minion(friendlyMinionPlay.group("cardId"), friendlyMinionPlay.group("id")), friendlyMinionPlay.group("dstPos"))
            #print "lol"
            #self.debug_print_shit()
        if oppositeMinionPlay and self.isOpponent == 1:
            self.addMinion(Minion(oppositeMinionPlay.group("cardId"), oppositeMinionPlay.group("id")), oppositeMinionPlay.group("dstPos"))
            #print "omg"
            #self.debug_print_shit()
        if minionChangePosition and self.playerNumb == int(minionChangePosition.group("player")):
            self.change_position(minionChangePosition.group("id"), int(minionChangePosition.group("dstPos")))
            #print "wtf"
            #self.debug_print_shit()

class gameState(IAlterationEntity):
    __scha_budet__ = bool
    gameState = int
    mulligan_ended = bool
    # 0 - Mulligan
    # 1 - Your turn
    # 2 - Opponent turn
    # 3 - Discovering

    def __init__(self):
        self.game_state = 0
        self.__waiting_4_deck__ = False
        self.mulligan_ended = False

    def debug_print_shit(self):
        print "gamestate: " + str(self.game_state)

    def check_n_change(self, logLine):
        mulligan = re.search(regExps.end_of_mulligan, logLine)
        main_action_start = re.search(regExps.main_action_start, logLine)
        if mulligan:
            self.mulligan_ended = True
            return
        if main_action_start:
            self.__waiting_4_deck__ = True
            return
        my_turn = re.search(regExps.waiting_4_friendly_deck, logLine)
        opp_turn = re.search(regExps.waiting_4_opposing_deck, logLine)
        if my_turn and self.mulligan_ended:
            self.game_state = 1
            self.__waiting_4_deck__ = False
            #self.debug_print_shit()
        if opp_turn and self.mulligan_ended:
            self.game_state = 2
            self.__waiting_4_deck__ = False
            #self.debug_print_shit()

class myHero(IAlterationEntity):
    players_info = playersInfo
    hp = int
    armor = int
    mana_crystals = int
    available_resources = int
    __temp_resources__ = int
    __resources_used__ = int
    __prepare_damage__ = bool

    def __init__(self, players_info):
        self.hp = 30
        self.players_info = players_info
        self.__temp_resources__ = 0
        self.__prepare_damage__ = False

    def debug_print_shit(self):
        print "HP: " + str(self.hp) + " Mana: " + str(self.available_resources)

    def change_resource(self, tag_name, entity, value):
        if entity == self.players_info.my_name:
            if tag_name == "TEMP_RESOURCES":
                self.__temp_resources__ = value
                self.available_resources = self.mana_crystals + value - self.__resources_used__
                self.debug_print_shit()
            if tag_name == "RESOURCES":
                self.mana_crystals = value
                self.available_resources = value
                self.debug_print_shit()
            if tag_name == "RESOURCES_USED":
                self.__resources_used__ = value
                self.available_resources = self.mana_crystals + self.__temp_resources__ - value
                self.debug_print_shit()

    def check_n_change(self, logLine):
        resources_changed = re.search(regExps.resources_tag_change, logLine)
        damage_changed = re.search(regExps.hero_damaged_tag.replace("(player_num)", str(self.players_info.my_player_num)), logLine)
        if damage_changed:
            self.hp = 30 - int(damage_changed.group("value"))
            self.debug_print_shit()
        if resources_changed and resources_changed.group("value") != "":
            self.change_resource(resources_changed.group("tag"), resources_changed.group("name"), int(resources_changed.group("value")))
            self.debug_print_shit()