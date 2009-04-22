"""
This module is describing high-level control flow of the game, that is
essentially logic behind "game rules".
This is typical "controller" in MVC terminology.
"""
import board
import fsm

BATTLE_STARTED='BATTLE_STARTED'; PLAYER_TURN='PLAYER_TURN'; BATTLE_ENDED='BATTLE_ENDED' # states
SETUP='SETUP'; SHOOT='SHOOT'; RESTART='RESTART' # events
SEA_SIDE = 10

# A "facade" around particular gamelogic implementation
class Game:
	"""
	Usage like this:

	game = logic.Game("player one", "player two")
	while True:
		state = game.get_state()
		if state == logic.BATTLE_STARTED:
			ships_for_player_one = ...
			game.setup("player one", ships_for_player_one)
			ships_for_player_two = ...
			game.setup("player two", ships_for_player_two)
		elif state == logic.PLAYER_TURN:
			current_player_id = game.current_player()
			the_shot = ...
			shot_result = game.shot(current_player_id, the_shot)
		elif state == logic.BATTLE_ENDED:
			break
	"""
	config = (
		(1, 4),  # one battleship
		(2, 3),  # two cruisers
		(3, 2),  # three destroyers
		(4, 1))  # four boats

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

	def shoot(self, player, shot):
		assert self.context['current'] == player
		self.state_machine.dispatch(SHOOT, (player, shot))
		return self.context['players'][player]['last_shot']

	def current_player(self):
		return self.context['current']

	def opponent_ships(self, player):
		opponent = self.context['players'][player]['opponent']
		return self.context['players'][opponent]['sea'].ships

	def player_shots(self, player):
		opponent = self.context['players'][player]['opponent']
		return self.context['players'][opponent]['sea'].shots

# Rule defenitions and support

def restart_battle(context):  # entry action
	for player in context['players'].itervalues():
		player['sea'] = None
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
	if len(target_sea.active_ships) == 0:
		return True
	else:
		return False

def pass_turn(context):  # action
	current_player = context['players'][context['current']]
	context['current'] = current_player['opponent']

def setup_ships(context, input):  # event input
	player, ships = input
	context['players'][player]['sea'] = board.SeaGrid(SEA_SIDE, ships)
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
