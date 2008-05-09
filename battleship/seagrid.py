"""
This module purpose is to help track of player's fleets.
It incapsulates implementation of tasks like fleet setup, player shots,
validation of actopns, and provides status information.
This is typical "model" in MVC terminology.
"""
import math

def is_squares_available(sea, indices):
	for i in indices:
		if sea[i] != ' ':
			return False
	return True

def occupy_squares(sea, indices):
	S = int(math.sqrt(len(sea)))
	assert S**2 == len(sea)
	for i in indices:
		assert sea[i] == ' '
		sea[i] = '#'
		# horizontal margin
		if i % S != 0 and i-1 >= 0 and i-1 < len(sea) and i-1 not in indices:
			assert sea[i-1] != '#'
			sea[i-1] = '.'  # left
		if (i+1) % S != 0 and i+1 >= 0 and i+1 < len(sea) and i+1 not in indices:
			assert sea[i+1] != '#'
			sea[i+1] = '.'  # right
		# vertical margin
		if i-S >= 0 and i-S < len(sea) and i-S not in indices:
			assert sea[i-S] != '#'
			sea[i-S] = '.'  # up
		if i+S >= 0 and i+S < len(sea) and i+S not in indices:
			assert sea[i+S] != '#'
			sea[i+S] = '.'  # down
		# diagonal margin
		if (i-S+1) % S != 0 and i-S+1 >= 0 and i-S+1 < len(sea):
			assert sea[i-S+1] != '#'
			sea[i-S+1] = '.'  # upper-right
		if i % S != 0 and i-S-1 >= 0 and i-S-1 < len(sea):
			assert sea[i-S-1] != '#'
			sea[i-S-1] = '.'  # upper-left
		if (i+S+1) % S != 0 and i+S+1 >= 0 and i+S+1 < len(sea):
			assert sea[i+S+1] != '#'
			sea[i+S+1] = '.'  # lower-right
		if i % S != 0 and i+S-1 >= 0 and i+S-1 < len(sea):
			assert sea[i+S-1] != '#'
			sea[i+S-1] = '.'  # lower-left

def shoot_square(sea, pos):
	sea_side = int(math.sqrt(len(sea)))
	assert sea_side**2 == len(sea)
	index = pos[1] * sea_side + pos[0]
	if sea[index] == '#':
		return True
	return False
