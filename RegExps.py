
class regExps():
    # Zone reg exps
    from_friendly_hand = r"name=.* id=(?P<id>\d*).*zonePos=(?P<zonePos>.*).* cardId=(?P<cardId>.*) player.*from FRIENDLY HAND ->*"
    to_friendly_hand = r"name=.* id=(?P<id>\d*).*zonePos=(?P<zonePos>.*).* cardId=(?P<cardId>.*) player.*to FRIENDLY HAND"
    change_card_position = r"name=.* id=(?P<id>\d*).*zone=HAND.*pos from (?P<pos_1>\d*) -> (?P<pos_2>\d*)"
    to_opposing_hand = r".*-> OPPOSING HAND"
    from_opposing_hand = r".*OPPOSING HAND -> .*"
    # Power reg exps
    player_name = r"TAG_CHANGE Entity=(?P<name>\w*) tag=PLAYSTATE value=PLAYING" # Hui znaet, kak poluchit' my nickname
    hero_power_activations = ".*Entity=(name).*tag=HEROPOWER_ACTIVATIONS_THIS_TURN value=(?P<value>\d*)" # Dont forget to replace (name) => player_name