from Parser import Parser
from HSActions import HSActions
import time

parser = Parser()
actions = HSActions()


def find_card_to_play(my_hand, available_resources):
    for i in range(0, len(my_hand.hand_cards)):
        if my_hand.hand_cards[i].mana_cost <= available_resources:
            return i
    return None

def find_taunt(opp_board):
    for i in range(1, opp_board.size_minions() + 1):
        if opp_board.minions[i].taunt:
            return i
    return None


parser.start()


time.sleep(5)
actions.find_next_game()

while parser.game_state.game_state != 0:
    time.sleep(2)

time.sleep(20)
actions.confirm_mulligan()
time.sleep(6)

while parser.game_state.game_state != 4:
    if parser.game_state.game_state == 1:
        time.sleep(3)
        num_of_card = find_card_to_play(parser.my_hand, parser.my_hero.available_resources)
        while num_of_card != None:
            #print str(parser.my_hand.hand_cards[num_of_card].mana_cost) + "   " + str(parser.my_hero.available_resources)
            if parser.my_hand.hand_cards[num_of_card].type == "WEAPON":
                actions.play_weapon(parser.my_hand, num_of_card)
            if parser.my_hand.hand_cards[num_of_card].type == "SPELL":
                actions.play_spell(parser.my_hand, num_of_card + 1, 0 if parser.my_hand.hand_cards[num_of_card].target_required else None, parser.my_board, parser.opp_board)
            if parser.my_hand.hand_cards[num_of_card].type == "MINION":
                actions.play_minion(parser.my_hand, num_of_card + 1, 1, 0 if parser.my_hand.hand_cards[num_of_card].target_required else None, parser.my_board, parser.opp_board)
            time.sleep(3)
            num_of_card = find_card_to_play(parser.my_hand, parser.my_hero.available_resources)
        if parser.my_hero.available_resources >= 2:
            actions.hero_power(0, parser.opp_board)
        taunt_id = find_taunt(parser.opp_board)
        cur_opp_board_size = parser.opp_board.size_minions()
        if taunt_id == None:
            for i in range(1, parser.my_board.size_minions() + 1):
                actions.hit(i, 0, parser.my_board.size_minions(), parser.opp_board.size_minions())
        if taunt_id != None:
            for i in range(1, parser.my_board.size_minions() + 1):
                if cur_opp_board_size != parser.opp_board.size_minions():
                    break
                actions.hit(i, taunt_id, parser.my_board.size_minions(), parser.opp_board.size_minions())
        taunt_id = find_taunt(parser.opp_board)
        actions.end_turn()
    time.sleep(2)
