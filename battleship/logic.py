"""
This module is describing high-level control flow of the game, that is
essentially logic behind "game rules".
This is typical "controller" in MVC terminology.
"""
import board
import fsm

BATTLE_STARTED='BATTLE_STARTED';PLAYER_TURN='PLAYER_TURN';BATTLE_ENDED='BATTLE_ENDED' # states
SETUP='SETUP';SHOOT='SHOOT';RESTART='RESTART' # events
SEA_SIDE = 10

def restart_battle(context):  # entry action
	for player in context['players'].itervalues():
		player['sea'] = board.SeaGrid(SEA_SIDE)
	context['current'] = context['players'].keys()[0]

def does_all_players_set(context):  # condition
	for player in context['players'].itervalues():
		if not player['ready']:
			return False
	return True

def is_shot_missed(context):  # condition
	current_player = context['players'][context['current']]
	if current_player['last_shot_hit']:
		return False
	else:
		return True

def does_opponent_has_no_ships(context):  # condition
	current_player = context['players'][context['current']]
	target_sea = context['players'][current_player['opponent']]['sea']
	if target_sea.has_ships():
		return False
	else:
		return True

def pass_turn(context):  # action
	current_player = context['players'][context['current']]
	context['current'] = current_player['opponent']

def setup_ships(context, input):  # event input
	player, ships = input
	sea = context['players'][player]['sea']
	for pos in ships:
		sea.place_ship(pos)
	context['players'][player]['ready'] = True

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
		fsm.set_state(self.context, BATTLE_STARTED)

	def get_state(self):
		return fsm.get_state(self.context)

	def setup(self, player, ships):
		fsm.dispatch(self.context, SETUP, (player, ships))

	def shot(self, player, shot):
		fsm.dispatch(self.context, SHOOT, (self.context['current'], shot))

	def current_player(self):
		return self.context['current']

	def print_sea(self):
		p1, p2 = self.context['players'].keys()
		print p1, "              ", p2
		for i in xrange(SEA_SIDE):
			for j in xrange(SEA_SIDE):
				print self.context['players'][p1]['sea'].grid[i * SEA_SIDE + j],
			print "  ",
			for j in xrange(SEA_SIDE):
				print self.context['players'][p2]['sea'].grid[i * SEA_SIDE + j],
			print
		print

# test
import ai
from random import randrange, choice

PLAYER1='PLAYER1'; PLAYER2='PLAYER2'
players = {}
shots_made = {}
game = Game(PLAYER1, PLAYER2)
while True:
	state = game.get_state()
	if state == BATTLE_STARTED:
		game.setup(PLAYER1, ai.setup_ships(SEA_SIDE, fleet_config))
		game.setup(PLAYER2, ai.setup_ships(SEA_SIDE, fleet_config))
		players[PLAYER1] = ai.ComputerPlayer(SEA_SIDE, fleet_config)
		players[PLAYER2] = ai.ComputerPlayer(SEA_SIDE, fleet_config)
		shots_made[PLAYER1] = shots_made[PLAYER2] = 0
	elif state == PLAYER_TURN:
		current_player = players[game.current_player()]
		game.shot(game.current_player(), current_player.shot())
		shots_made[game.current_player()] += 1
		game.print_sea()
	elif state == BATTLE_ENDED:
		print "# BATTLE ENDED"
		print (game.current_player() + " shots made: " + str(shots_made[game.current_player()]))
		break
	else:
		raise Exception("Unknown STATE %s" % state)
