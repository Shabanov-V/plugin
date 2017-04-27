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
    mana_cost  = None #int
    special_id = None #str
    name       = None #str
    type       = None #str
    attack     = None #int
    health     = None #int
    json_num   = None #str
    def __init__(self, cardId, specialId):
        self.special_id = specialId
        self.card_id    = cardId
        self.json_num   = json_id_by_cardId(cardId)
        self.name       = get_json_prop(cardId, "name")
        self.type       = get_json_prop(cardId, "type")
        self.attack     = get_json_prop(cardId, "attack")
        self.health     = get_json_prop(cardId, "health")
    #TODO: Add card in hand bafs
# Can I write without self.methodName or self.fieldName?

class Minion(Card):
    card_id = None #int
    special_id = None #int
    json_num = None #str
    attack = None #int
    health = None #int
    maxHealth = None #int
    isMine = None #bool
    silenced = None #bool
    windfury = None #bool
    taunt = None #bool
    divine_shield = None #bool
    frozen = None #bool
    stealth = None #bool
    position = None #int
    num_attacks_this_turn = None #int
    poisonous = None #bool
    cost = None #int
    def __init__(self, cardId, specialId, isMine):
        self.special_id = specialId
        self.card_id    = cardId
        self.json_num   = json_id_by_cardId(cardId)
        self.name       = get_json_prop(cardId, "name")
        self.type       = get_json_prop(cardId, "type")
        self.attack     = get_json_prop(cardId, "attack")
        self.health     = get_json_prop(cardId, "health")
        self.isMine     = isMine
