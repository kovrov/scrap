

BATTLE_STARTED, PLAYER_TURN, BATTLE_ENDED = xrange(3)
SETUP, SHOOT, RESTART = xrange(3)
PLAYER1, PLAYER2 = xrange(2)
SEA_SIDE = 10

def restart_battle(context):
	print "restart_battle"
	context['current'] = PLAYER1
	context['winner'] = None
	context['players'][PLAYER1]['sea'] = [' '] * (SEA_SIDE**2)
	context['players'][PLAYER2]['sea'] = [' '] * (SEA_SIDE**2)

def player_setup(context, player, ships):
	pass

def player_shoot(context, player, shot):
	pass

def new_game(context):
	pass

def all_players_set(context):
	pass

def shot_missed(context, player, shot):
	pass

def pass_turn(context):
	pass

def opponent_has_no_ships(context): 
	pass

def setup_ships(context):
	print "setup_ships"

def process_shot(context):
	pass

def player_lose(context):
	pass

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
				'input': process_shot,
				'transitions': (
					{'condition':shot_missed, 'state':PLAYER_TURN, 'action':pass_turn},
					{'condition':opponent_has_no_ships, 'state':BATTLE_ENDED, 'action':None})},
			RESTART: {
				'input': None,
				'transitions': (
					{'condition':None, 'state':BATTLE_STARTED, 'action':player_lose},)}}},
	BATTLE_ENDED: {
		'on_enter': None,
		'events': {
			RESTART: {
				'input': None,
				'transitions': (
					{'condition':None, 'state':BATTLE_STARTED, 'action':None},)}}}
}

def fsm_set_state(context, state):
	states[state]['on_enter'](context)
	context['state'] = state

def fsm_dispatch(context, event, input):
	states[context['state']]['events'][event](input)

context = {
		'players': { PLAYER1:{}, PLAYER2:{} },
		'current': None,
		'winner':  None}

fsm_set_state(context, BATTLE_STARTED) #game = Game()
ships = [(24,34,44,54),(37,47,57),(80,81,82),(69,79),(1,2),(85,86),(8,),(6,),(60,),(22,)]
fsm_dispatch(context, SETUP, (PLAYER1, ships)) #game.setupShips(PLAYER1, ships)
fsm_dispatch(context, SETUP, (PLAYER2, ships)) #game.setupShips(PLAYER2, ships)
#while fsm_get_state(context) == PLAYER_TURN: #while game.inprogress:
fsm_dispatch(context, SHOOT, (PLAYER1, (7,8))) #game.shoot(PLAYER1, (7,8))
fsm_dispatch(context, SHOOT, (PLAYER2, (5,6))) #game.shoot(PLAYER2, (5,6))
