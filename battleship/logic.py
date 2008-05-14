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
	return current_player['last_shot'] == 'miss'

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
	current_player['last_shot'] = target_sea.shoot_square(pos)

states = {
	BATTLE_STARTED: fsm.State(
		on_enter = restart_battle,
		events = {
			SETUP: fsm.Event(
				input = setup_ships,
				transitions = (
					fsm.Transition(condition=does_all_players_set, state=PLAYER_TURN),))}),
	PLAYER_TURN: fsm.State(
		events = {
			SHOOT: fsm.Event(
				input = player_shoot,
				transitions = (
					fsm.Transition(condition=is_shot_missed, state=PLAYER_TURN, action=pass_turn),
					fsm.Transition(condition=does_opponent_has_no_ships, state=BATTLE_ENDED)))}),
	BATTLE_ENDED: fsm.State(
		events = {
			RESTART: fsm.Event(
				transitions = (
					fsm.Transition(state=BATTLE_STARTED),))})}

fleet_config = (
	(1, 4),  # one battleship
	(2, 3),  # two cruisers
	(3, 2),  # three destroyers
	(4, 1))  # four boats
# from wikipedia article
fleet_config_2a = (
	(1, 5),  # one carrier
	(1, 4),  # one battleship
	(2, 3),  # two cruiser
	(1, 2))  # one destroyer
# from wikipedia pix
fleet_config_2b = (
	(1, 5),  # one carier
	(1, 4),  # one battleship
	(1, 3),  # one cruiser
	(2, 2),  # two destroyers
	(2, 1))  # two boats

# Just a "nice" client helper
class Game:
	def __init__(self, player1, player2):
		self.context = {
			'players': {
				player1: {'ready': False, 'opponent': player2},
				player2: {'ready': False, 'opponent': player1}},
			'current': None}
		self.state_machine = fsm.Transducer(states, BATTLE_STARTED, self.context)

	def get_state(self):
		return self.state_machine.get_state()

	def setup(self, player, ships):
		self.state_machine.dispatch(SETUP, (player, ships))

	def shot(self, player, shot):
		assert self.context['current'] == player
		self.state_machine.dispatch(SHOOT, (player, shot))
		return self.context['players'][player]['last_shot']

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

# test
import ai
from random import randrange, choice

PLAYER1='PLAYER1'; PLAYER2='PLAYER2'
game = Game(PLAYER1, PLAYER2)
players = {}
shots_made = {}
while True:
	state = game.get_state()
	if state == BATTLE_STARTED:
		game.setup(PLAYER1, ai.setup_ships(SEA_SIDE, fleet_config))
		game.setup(PLAYER2, ai.setup_ships(SEA_SIDE, fleet_config))
		players[PLAYER1] = ai.ComputerPlayer(SEA_SIDE, fleet_config)
		players[PLAYER2] = ai.ComputerPlayer(SEA_SIDE, fleet_config)
		shots_made[PLAYER1] = shots_made[PLAYER2] = 0
	elif state == PLAYER_TURN:
		current_player_id = game.current_player()
		current_player = players[current_player_id]
		shot = current_player.shot()
		res = game.shot(current_player_id, shot)
		shots_made[current_player_id] += 1
		game.print_sea()
		print current_player_id, res, shot
		current_player.track(shot, res)
	elif state == BATTLE_ENDED:
		print "# BATTLE ENDED"
		print game.current_player(), "win, shots made:", shots_made[game.current_player()]
		break
	else:
		raise Exception("Unknown STATE %s" % state)
