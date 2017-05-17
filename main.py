from Entities import *
import os, time
from Tkinter import *
from threading import *

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
my_board = board(0)
op_board = board(1)
game_state = gameState()
my_hero = myHero(players_info)

root = Tk()

bt1 = Button(root)
bt1.pack()
bt1["text"] = "Print player hand"


bt2 = Button(root)
bt2.pack()
bt2["text"] = "Print opp board"

bt3 = Button(root)
bt3.pack()
bt3["text"] = "Print player board"

bt4 = Button(root)
bt4.pack()
bt4["text"] = "Numbers"

def printOppBoard(event):
    op_board.debug_print_shit()

def printPlayerBoard(event):
    my_board.debug_print_shit()
        
def printPlayerHand(event):
    my_hand.debug_print_shit()
    
def printPlayersNumbers(event):
    print str(my_board.playerNumb) + " " + str(op_board.playerNumb)
    
        
bt1.bind("<Button-1>", printPlayerHand)
bt2.bind("<Button-1>", printOppBoard)
bt3.bind("<Button-1>", printPlayerBoard)
bt4.bind("<Button-1>", printPlayersNumbers)


thread = Thread(target = root.mainloop, args = ())
thread.start()

while True:
    where_power = power.tell()
    where_zone = zone.tell()
    log_line = zone.readline() + power.readline()
    if not log_line:
        time.sleep(1)
    else:
       game_state.check_n_change(log_line)
       my_board.check_n_change(log_line)
       op_board.check_n_change(log_line)
       my_hand.check_n_change(log_line)
       #print log_line