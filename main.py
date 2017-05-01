from Entities import *
import os, time

zone_filename = 'C:\Program Files (x86)\Hearthstone\Logs\Zone.log'
zone = open(zone_filename,'r')
zone.seek(os.stat(zone_filename)[6])

power_filename = 'C:\Program Files (x86)\Hearthstone\Logs\Power.log'
power = open(power_filename, 'r')
power.seek(os.stat(power_filename)[6])

my_hand = myHandCards()
opp_hand = opponentHandCards()
players_info = playersInfo()
my_hero_power = myHeroPower(players_info)
opp_hero_power = opponentHeroPower(players_info)

while True:
    where_power = power.tell()
    where_zone = zone.tell()
    log_line = power.readline() + zone.readline()
    if not log_line:
        time.sleep(1)
    else:
       players_info.check_n_change(log_line)
       my_hero_power.check_n_change(log_line)
       opp_hero_power.check_n_change(log_line)