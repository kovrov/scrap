"""
This module is describing high-level control flow of the game, that is
essentially logic behind "game rules".
This is typical "controller" in MVC terminology.
"""
import board
import fsm
import log

BATTLE_STARTED='BATTLE_STARTED';PLAYER_TURN='PLAYER_TURN';BATTLE_ENDED='BATTLE_ENDED' # states
SETUP='SETUP';SHOOT='SHOOT';RESTART='RESTART' # events
SEA_SIDE = 10

@log.info
def restart_battle(context):  # entry action
	for player in context['players'].itervalues():
		player['sea'] = board.SeaGrid(SEA_SIDE)
	context['current'] = context['players'].keys()[0]

@log.info
def does_all_players_set(context):  # condition
	for player in context['players'].itervalues():
		if not player['ready']:
			return False
	return True

@log.info
def is_shot_missed(context):  # condition
	current_player = context['players'][context['current']]
	if current_player['last_shot_hit']:
		return False
	else:
		return True

@log.info
def does_opponent_has_no_ships(context):  # condition
	current_player = context['players'][context['current']]
	target_sea = context['players'][current_player['opponent']]['sea']
	if target_sea.has_ships():
		return False
	else:
		return True

@log.info
def pass_turn(context):  # action
	current_player = context['players'][context['current']]
	context['current'] = current_player['opponent']

@log.info
def setup_ships(context, input):  # event input
	player, ships = input
	sea = context['players'][player]['sea']
	for pos in ships:
		sea.place_ship(pos)
	context['players'][player]['ready'] = True

@log.info
def player_shoot(context, input):  # event input
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
					{'condition':does_all_players_set, 'state':PLAYER_TURN, 'action':None},)}}},
	PLAYER_TURN: {
		'on_enter': None,
		'events': {
			SHOOT: {
				'input': player_shoot,
				'transitions': (
					{'condition':is_shot_missed, 'state':PLAYER_TURN, 'action':pass_turn},
					{'condition':does_opponent_has_no_ships, 'state':BATTLE_ENDED, 'action':None})}}},
	BATTLE_ENDED: {
		'on_enter': None,
		'events': {
			RESTART: {
				'input': None,
				'transitions': (
					{'condition':None, 'state':BATTLE_STARTED, 'action':None},)}}}}

fleet_config = (
	(1, 4),  # one huge
	(2, 3),  # two bigs
	(3, 2),  # three mediums
	(4, 1))  # four smalls

class Game:
	def __init__(self, player1, player2):
		self.context = {
			'states': states,
			'players': {
				player1: {'ready': False, 'opponent': player2},
				player2: {'ready': False, 'opponent': player1}},
			'current': None}
		self.state = fsm.set_state(self.context, BATTLE_STARTED)

# test
PLAYER1='PLAYER1'; PLAYER2='PLAYER2'


import ai
from random import randrange, choice

game = Game(PLAYER1, PLAYER2)
while game.get_state() != BATTLE_ENDED:
	state = fsm.get_state(context)
	if game.state == BATTLE_STARTED:
		log.log("# BATTLE STARTED")
		fsm.dispatch(context, SETUP,
				(PLAYER1, ai.setup_ships(SEA_SIDE, fleet_config)))
		context['players'][PLAYER1]['shots'] = range(100)
		fsm.dispatch(context, SETUP,
				(PLAYER2, ai.setup_ships(SEA_SIDE, fleet_config)))
		context['players'][PLAYER2]['shots'] = range(100)
	elif state == PLAYER_TURN:
		log.log("# PLAYER TURN")
		shot = choice(context['players'][context['current']]['shots'])
		context['players'][context['current']]['shots'].remove(shot)
		log.log("  " + context['current'] + " shots left: " + str(len(context['players'][context['current']]['shots'])))
		fsm.dispatch(context, SHOOT, (context['current'], (shot // 10, shot % 10)))
	elif state == BATTLE_ENDED:
		log.log("# BATTLE ENDED")
	else:
		raise Exception("Unknown STATE %s" % state)
