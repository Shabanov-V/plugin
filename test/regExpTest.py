import re

tag_change = r".*TAG_CHANGE Entity=\[name=(?P<name>(\w*\s*)*) id=(?P<id>\d*).*zonePos=(?P<zonePos>\d*) cardId=(?P<cardId>\w*) player=(?P<player>\d*)\] tag=(?P<tag>\w*) value=(?P<value>\d*).*"
result = re.search(tag_change, "D 14:31:41.0539657 GameState.DebugPrintPower() -     TAG_CHANGE Entity=[name=Kabal Crystal Runner id=14 zone=HAND zonePos=8 cardId=CFM_760 player=1] tag=TAG_LAST_KNOWN_COST_IN_HAND value=4")

if result:
    print "|"+result.group("name")+"| " + result.group("tag")+" "+result.group("value")
else:
    print "fuck u"