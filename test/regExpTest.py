import re

change_pos = r"id=(?P<id>\d*).*pos from (?P<pos_1>\d*) -> (?P<pos_2>\d*)"
result = re.search(change_pos, "D 14:31:30.6715887 ZoneChangeList.ProcessChanges() - id=2 local=False [name=Pyroblast id=35 zone=HAND zonePos=1 cardId=EX1_279 player=2] pos from 0 -> 1")
print result.group("pos_2")