import json

with open('cards.json') as data_file:
    cards = json.load(data_file)


def json_id_by_cardId(cardId):
    for i in range(0, len(cards)):
        if cards[i]["id"] == cardId:
            return i
    return 0


class Card():
    card_id = str # JSON id
    json_num = int
    special_id = int
    attack = int
    health = int
    mana_cost = int
    type = str
    name = str
# Can I write without self.methodName or self.fieldName?
    def __init__(self, cardId, specialId):
        self.special_id = specialId
        self.card_id = cardId
        self.json_num = json_id_by_cardId(cardId)
        self.name = cards[self.json_num]["name"]
        if cards[self.json_num]["type"] == "MINION":
            self.type = "MINION"
            self.attack = cards[self.json_num]["attack"]
            self.health = cards[self.json_num]["health"]
        else:
            self.attack = None
            self.health = None
            self.type = cards[self.json_num]["type"]




class Minion():
    card_id = int
    isMine = bool
    attack = int
    health = int
    maxHealt = int
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

