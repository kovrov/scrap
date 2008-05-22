# test
import logic
import ai
import array

def print_sea(game, player_id, last_shot, res):
	rows = 10
	side = rows*2+1
	grid = array.array('c', ' '*(rows*side))
	for x, y in game.player_shots(player_id):
		grid[y * side + x*2+1] = '.'
	for ship in game.opponent_ships(player_id):
		for s in ship:
			grid[s.y * side + s.x*2+1] = ' ' if s.active else 'x'
	x, y = last_shot
	grid[y * side + x*2] = '['
	grid[y * side + x*2+2] = ']'
	padding = ' ' * 40 + '|' if player_id == PLAYER1 else ''
	for i in xrange(rows):
		print padding, grid[i*side:(i+1)*side].tostring()
	print padding, player_id, res, last_shot, '\n'


PLAYER1='PLAYER1'; PLAYER2='PLAYER2'
game = logic.Game(PLAYER1, PLAYER2)
players = {}
shots_made = {}
while True:
	state = game.get_state()
	if state == logic.BATTLE_STARTED:
		game.setup(PLAYER1, ai.setup_ships(logic.SEA_SIDE, game.config))
		game.setup(PLAYER2, ai.setup_ships(logic.SEA_SIDE, game.config))
		players[PLAYER1] = ai.ComputerPlayer(logic.SEA_SIDE, game.config)
		players[PLAYER2] = ai.ComputerPlayer(logic.SEA_SIDE, game.config)
		shots_made[PLAYER1] = shots_made[PLAYER2] = 0
	elif state == logic.PLAYER_TURN:
		current_player_id = game.current_player()
		current_player = players[current_player_id]
		shot = current_player.shoot()
		res = game.shoot(current_player_id, shot)
		current_player.track(shot, res)
		shots_made[current_player_id] += 1
		print_sea(game, current_player_id, shot, res)
	elif state == logic.BATTLE_ENDED:
		print "# BATTLE ENDED"
		print game.current_player(), "win, shots made:", shots_made[game.current_player()]
		break
	else:
		raise Exception("Unknown STATE %s" % state)
