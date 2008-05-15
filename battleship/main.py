# test
import logic
import ai

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
		shot = current_player.shot()
		res = game.shot(current_player_id, shot)
		shots_made[current_player_id] += 1
		game.print_sea()
		print current_player_id, res, shot
		current_player.track(shot, res)
	elif state == logic.BATTLE_ENDED:
		print "# BATTLE ENDED"
		print game.current_player(), "win, shots made:", shots_made[game.current_player()]
		break
	else:
		raise Exception("Unknown STATE %s" % state)
