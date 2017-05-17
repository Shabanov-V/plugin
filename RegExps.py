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
    waiting_4_friendly_deck = "START waiting for zone FRIENDLY DECK"
    waiting_4_opposing_deck = "START waiting for zone OPPOSING DECK"
    main_action_start = "name=GameEntity\] tag=NEXT_STEP value=MAIN_ACTION"
    end_of_mulligan = "tag=MULLIGAN_STATE value=WAITING"
    # Power reg exps
    tag_change = r".*TAG_CHANGE Entity=\[name=(?P<name>(\w*\s*)*) id=(?P<id>\d*).*zonePos=(?P<zonePos>\d*) cardId=(?P<cardId>\w*) player=(?P<player>\d*)\] tag=(?P<tag>\w*) value=(?P<value>\d*).*"
    hero_power_activations = ".*Entity=(name).*tag=HEROPOWER_ACTIVATIONS_THIS_TURN value=(?P<value>\d*)" # Dont forget to replace (name) => player_name
    died = r"name=.* id=(?P<id>\d*).* cardId=(?P<cardId>.*) player.*from .*PLAY -> .*GRAVEYARD"
    minionChangePosition = r"ZoneMgr.*id=(?P<id>\d*).*zone=PLAY.*zonePos (?P<from>\d*) -> (?P<to>\d*)"
    minionPlay1 = r"PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=\[name=.* id=(?P<id>\d*).*zonePos=(?P<dstPos>\d).*cardId=(?P<cardId>.*) player=.\] tag=ZONE value=PLAY"
    minionChangePosition1 = r"PowerTaskList.DebugPrintPower.*TAG_CHANGE Entity=\[name=.* id=(?P<id>\d*).*cardId=(?P<cardId>.*) player=.\] tag=ZONE_POSITION value=(?P<dstPos>\d)"
    friendly_minion_play2 = r"ZoneChangeList.ProcessChanges.*TRANSITIONING card \[name=(.+) id=(?P<id>\d+) zone=.* zonePos=(?P<dstPos>\d) cardId=(?P<cardId>.*) player=.\].* to FRIENDLY PLAY"
    minion_change_position2 = r"ZoneChangeList.ProcessChanges.*id=\d+ .* \[name=.* id=(?P<id>\d*) zone=.* zonePos=(\d) cardId=(?P<cardId>.*) player=(?P<player>.)\] pos from \d -> (?P<dstPos>\d)"
    opposite_minion_play = r"ZoneChangeList.ProcessChanges.*TRANSITIONING card \[name=(.+) id=(?P<id>\d+) zone=.* zonePos=(?P<dstPos>\d) cardId=(?P<cardId>.*) player=.\].* to OPPOSING PLAY"
    who_is_who1 = r"player=(?P<player_numb>.)].*FRIENDLY"
    who_is_who2 = r"player=(?P<player_numb>.)].*OPPOSING"
    
    minion_tag_changed = r"\[type=TAG_CHANGE entity=\[id=(?P<id>\d+) cardId=(?P<cardId>.*) name=(.+)\] tag=(?P<tag>.*) value=(?P<value>.*)\] c"
    
    """\[type=TAG_CHANGE entity=\[id=(\d+) cardId=(.*) name=(.*)\] tag=(.*) value=(.*)\] c"""
    
    """ ZoneChangeList.ProcessChanges.*TRANSITIONING card \[name=(.+) id=(\d+) zone=.* zonePos=(\d) cardId=(.*) player=.\].* to FRIENDLY PLAY """
    """ ZoneChangeList.ProcessChanges.*id=\d+ .* \[name=.* id=(\d*) zone=.* zonePos=(\d) cardId=(.*) player=(.)\] pos from \d -> (\d) """
    """ name=.* id=(\d*).* cardId=(.*) player.*from .*PLAY -> .*GRAVEYARD """