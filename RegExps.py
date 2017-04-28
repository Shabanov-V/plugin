
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
    minionPlay = r"ZoneMgr.CreateLocalChangesFromTrigger().*name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*dstZoneTag=PLAY dstPos=(?P<dstPos>\d)"
    died = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY PLAY -> FRIENDLY GRAVEYARD"
    minionChangePosition = r"ZoneMgr.*id=(?P<id>\d*).*zone=PLAY.*zonePos (?P<from>\d*) -> (?P<to>\d*)"
    minionPlay1 = r"PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=\[name=.* id=(?P<id>\d*).*zonePos=(?P<dstPos>\d).*cardId=(?P<cardId>.*) player=.\] tag=ZONE value=PLAY"
    minionChangePosition1 = r"PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=\[name=.* id=(?P<id>\d*).*cardId=(?P<cardId>.*) player=.\] tag=ZONE_POSITION value=(?P<dstPos>\d)"
    
    
    """PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=\[name=.* id=(?P<id>\d*).*cardId=(?P<cardId>.*) player=2\] tag=ZONE_POSITION value=(?P<dstPos>\d)"""