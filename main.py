from Entities import *
import os, time

zone_filename = 'C:\Program Files (x86)\Hearthstone\Logs\Zone.log'
zone = open(zone_filename,'r')
zone.seek(os.stat(zone_filename)[6])

my_hand = myHandCards()


while True:
    where_zone = zone.tell()
    log_line = zone.readline()
    if not log_line:
        time.sleep(1)
    else:
        my_hand.checkNChange(log_line)