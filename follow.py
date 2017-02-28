import time, os
import re

#Set the filename and open the file
filename = 'C:\Program Files (x86)\Hearthstone\Logs\Zone.log'
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

p_drawCard = r"name=(.*) id=.*to FRIENDLY HAND"
p_playCreature = r"name=(.*) id=.*FRIENDLY HAND -> FRIENDLY PLAY"
p_playSpell = r"name=(.*) id=.*from FRIENDLY HAND -> $"
p_died = r"name=(.*) id=.*from FRIENDLY PLAY -> FRIENDLY GRAVEYARD"


while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        draws = re.search(p_drawCard, line)
        playCreatures = re.search(p_playCreature, line)
        playSpells = re.search(p_playSpell, line)
        dieds = re.search(p_died, line)
        if draws:
            print "Draw: " + draws.group(1) # already has newline
        if playCreatures:
            print "Play Creature: " + playCreatures.group(1)
        if playSpells:
            print "Play Spell: " + playSpells.group(1)
        if dieds:
            print "Died: " + dieds.group(1)