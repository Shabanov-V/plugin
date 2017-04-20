
class regExps():
    from_friendly_hand = r"name=.* id=(?P<id>\d*).*zonePos=(?P<zonePos>.*).* cardId=(?P<cardId>.*) player.*from FRIENDLY HAND ->*"
    to_friendly_hand = r"name=.* id=(?P<id>\d*).*zonePos=(?P<zonePos>.*).* cardId=(?P<cardId>.*) player.*to FRIENDLY HAND"
    change_card_position = r"name=.* id=(?P<id>\d*).*zone=HAND.*pos from (?P<pos_1>\d*) -> (?P<pos_2>\d*)"