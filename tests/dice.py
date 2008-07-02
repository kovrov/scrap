import random

def roll_dice():
	return random.randint(1, 6)


def simulate_turn():
	player_dices = roll_dice(), roll_dice()
	ai_dices = roll_dice(), roll_dice()

	player_double = player_dices[0] == player_dices[1]
	ai_double = ai_dices[0] == ai_dices[1]

	# as defined by "rules"
	if player_double and ai_double:
		if player_dices[0] < ai_dices[0]:
			winner = "ai"
		elif player_dices[0] > ai_dices[0]:
			winner = "player"
		else:
			winner = None
	elif player_double:
		winner = "player"
	elif ai_double:
		winner = "ai"
	else:
		player_sum = player_dices[0] + player_dices[1]
		ai_sum = ai_dices[0] + ai_dices[1]
		if player_sum < ai_sum:
			winner = "ai"
		elif player_sum > ai_sum:
			winner = "player"
		else:
			winner = None

	return winner, player_dices, ai_dices

#main
player_want_play = True
player_score = 0
ai_score = 0
while player_want_play:
	if random.random() < 0.7:  # this could be twiked
		predefined_winner = "ai"
		ai_score += 1
	else:
		predefined_winner = "player"
		player_score += 1
	
	winner, player_dices, ai_dices = simulate_turn()
	while winner and winner != predefined_winner: # cheating...
		#print "cheating..."
		winner, player_dices, ai_dices = simulate_turn()

	print winner, "wins (p:", player_dices, "ai:", ai_dices, ")"

	#print "p:", player_score, "ai:", ai_score, 100.0 / (ai_score + player_score) * ai_score,
	playrer_said = raw_input("continue? (y/n)")
	player_want_play = playrer_said != 'n'

