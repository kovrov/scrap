"""
This module is describing high-level control flow of the game, that is
essentially logic behind "game rules".
This is typical "controller" in MVC terminology.
"""
import board
import fsm

BATTLE_STARTED, PLAYER_TURN, BATTLE_ENDED = range(100, 103) # states
SETUP, SHOOT, RESTART = range(200, 203) # events
PLAYER1, PLAYER2 = range(300, 302)
SEA_SIDE = 10

def restart_battle(context):  # entry action
	print "battle restarted"
	for player in context['players'].itervalues():
		player['sea'] = board.SeaGrid(SEA_SIDE)
	context['current'] = context['players'].keys()[0]

def all_players_set(context):  # condition
	for player in context['players'].itervalues():
		if not player['ready']:
			print "not all players set!"
			return False
	print "all players set!"
	return True

def missed_shot(context):  # condition
	current_player = context['players'][context['current']]
	if current_player['last_shot_hit']:
		print "shot is hit!"
		return False
	else:
		print "shot is missed!"
		return True

def opponent_has_no_ships(context):  # condition
	current_player = context['players'][context['current']]
	target_sea = context['players'][current_player['opponent']]['sea']
	if target_sea.has_ships():
		print "opponent has ships!"
		return False
	else:
		print "opponent has no ships!"
		return True

def pass_turn(context):  # action
	print "passing turn..."
	current_player = context['players'][context['current']]
	context['current'] = current_player['opponent']

def setup_ships(context, input):  # event input
	print "setting up ships..."
	player, ships = input
	sea = context['players'][player]['sea']
	for pos in ships:
		sea.place_ship(pos)
	context['players'][player]['ready'] = True

def player_shoot(context, input):  # event input
	print "player shooting..."
	player, pos = input
	current_player = context['players'][context['current']]
	target_sea = context['players'][current_player['opponent']]['sea']
	current_player['last_shot_hit'] = target_sea.shoot_square(pos)

states = {
	BATTLE_STARTED: {
		'on_enter': restart_battle,
		'events': {
			SETUP: {
				'input': setup_ships,
				'transitions': (
					{'condition':all_players_set, 'state':PLAYER_TURN, 'action':None},)}}},
	PLAYER_TURN: {
		'on_enter': None,
		'events': {
			SHOOT: {
				'input': player_shoot,
				'transitions': (
					{'condition':missed_shot, 'state':PLAYER_TURN, 'action':pass_turn},
					{'condition':opponent_has_no_ships, 'state':BATTLE_ENDED, 'action':None})}}},
	BATTLE_ENDED: {
		'on_enter': None,
		'events': {
			RESTART: {
				'input': None,
				'transitions': (
					{'condition':None, 'state':BATTLE_STARTED, 'action':None},)}}}}

context = {
	'states': states,
	'players': {
		PLAYER1: {'ready': False, 'opponent': PLAYER2},
		PLAYER2: {'ready': False, 'opponent': PLAYER1}},
	'current': None}

# test
from random import randint

fsm.set_state(context, BATTLE_STARTED) #game = Game()
#ships = [(24,34,44,54),(37,47,57),(80,81,82),(69,79),(1,2),(85,86),(8,),(6,),(60,),(22,)]
ships = [(24,34,44,54),]
fsm.dispatch(context, SETUP, (PLAYER1, ships)) #game.setupShips(PLAYER1, ships)
fsm.dispatch(context, SETUP, (PLAYER2, ships)) #game.setupShips(PLAYER2, ships)
while fsm.get_state(context) == PLAYER_TURN: #while game.inprogress:
	fsm.dispatch(context, SHOOT, (PLAYER1, (randint(0,9),randint(0,9)))) #game.shoot(PLAYER2, (5,6))
	fsm.dispatch(context, SHOOT, (PLAYER2, (4,2)))
	fsm.dispatch(context, SHOOT, (PLAYER2, (4,3)))
	fsm.dispatch(context, SHOOT, (PLAYER2, (4,4)))
	fsm.dispatch(context, SHOOT, (PLAYER2, (4,5)))
