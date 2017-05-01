class regExps():
    # Zone reg exps
    from_friendly_hand = r"name=.* id=(?P<id>\d*).*zonePos=(?P<zonePos>.*).* cardId=(?P<cardId>.*) player.*from FRIENDLY HAND ->*"
    to_friendly_hand = r"name=.* id=(?P<id>\d*).*zonePos=(?P<zonePos>.*).* cardId=(?P<cardId>.*) player.*to FRIENDLY HAND"
    change_card_position = r"name=.* id=(?P<id>\d*).*zone=HAND.*pos from (?P<pos_1>\d*) -> (?P<pos_2>\d*)"
    to_opposing_hand = r".*-> OPPOSING HAND"
    from_opposing_hand = r".*OPPOSING HAND -> .*"
    smth_to_friendly_hand = r".*to FRIENDLY HAND"
    smth_to_opposing_hand = r".*to OPPOSING HAND"
    player_name_n_id = r".*id=(?P<id>\d*).*name=(?P<name>\w*).*tag=NUM_CARDS_DRAWN_THIS_TURN.*"
    # Power reg exps
    hero_power_activations = ".*Entity=(name).*tag=HEROPOWER_ACTIVATIONS_THIS_TURN value=(?P<value>\d*)" # Dont forget to replace (name) => player_name
    died = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from FRIENDLY PLAY -> FRIENDLY GRAVEYARD"
    minionChangePosition = r"ZoneMgr.*id=(?P<id>\d*).*zone=PLAY.*zonePos (?P<from>\d*) -> (?P<to>\d*)"
    minionPlay1 = r"PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=\[name=.* id=(?P<id>\d*).*zonePos=(?P<dstPos>\d).*cardId=(?P<cardId>.*) player=.\] tag=ZONE value=PLAY"
    minionChangePosition1 = r"PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=\[name=.* id=(?P<id>\d*).*cardId=(?P<cardId>.*) player=.\] tag=ZONE_POSITION value=(?P<dstPos>\d)"
    
    minionPlay2 = r"ZoneChangeList.ProcessChanges.*TRANSITIONING card \[name=(.+) id=(?P<id>\d+) zone=.* zonePos=(?P<dstPos>\d) cardId=(?P<cardId>.*) player=.\].* to FRIENDLY PLAY"
    minionChangePosition2 = r"ZoneChangeList.ProcessChanges.*id=\d+ .* \[name=.* id=(?P<id>\d*) zone=.* zonePos=(\d) cardId=(?P<cardId>.*) player=.\] pos from \d -> (?P<dstPos>\d)"
    