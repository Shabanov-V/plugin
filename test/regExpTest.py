import re

hero_power_activations = ".*Entity=Grig0510.*tag=HEROPOWER_ACTIVATIONS_THIS_TURN value=(?P<value>\d*)"
result = re.search(hero_power_activations, "D 10:22:13.8424500 PowerTaskList.DebugPrintPower() -     TAG_CHANGE Entity=Grig0510 tag=HEROPOWER_ACTIVATIONS_THIS_TURN value=1")
if result:
    print "|"+result.group("value")+"|"