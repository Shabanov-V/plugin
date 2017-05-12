import json

with open('cards.json') as data_file:
    cards = json.load(data_file)


def json_id_by_cardId(cardId):
    for i in range(0, len(cards)):
        if cards[i]["id"] == cardId:
            return i
    return 0

def get_json_prop(cardId, prop):
    t = json_id_by_cardId(cardId)
    if prop in cards[t]:
        return cards[t][prop]
    else:
        return None
    
class Card():
    card_id = str
    mana_cost  = int
    special_id = int
    name       = str
    type       = str
    attack     = int
    health     = int
    json_num   = str
    def __init__(self, cardId, specialId):
        self.special_id = specialId
        self.card_id    = cardId
        self.json_num   = json_id_by_cardId(cardId)
        self.name       = get_json_prop(cardId, "name")
        self.type       = get_json_prop(cardId, "type")
        self.attack     = get_json_prop(cardId, "attack")
        self.health     = get_json_prop(cardId, "health")
        self.mana_cost  = get_json_prop(cardId, "cost")

class Minion(Card):
    name = str
    card_id = int
    special_id = int
    json_num = str
    attack = int
    health = int
    maxHealth = int
    isMine = bool
    silenced = bool
    windfury = bool
    taunt = bool
    divine_shield = bool
    frozen = bool
    stealth = bool
    position = int
    num_attacks_this_turn = int
    poisonous = bool
    cost = int

    def __init__(self, cardId, specialId):
        self.type       = get_json_prop(cardId, "type")
        if (self.type == "MINION"):
            self.special_id = specialId
            self.card_id    = cardId
            self.json_num   = json_id_by_cardId(cardId)
            self.name       = get_json_prop(cardId, "name")
            self.attack     = get_json_prop(cardId, "attack")
            self.health     = get_json_prop(cardId, "health")
