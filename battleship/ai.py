"""
Battleship map generator
"""
import math
import random

def setup_ships(sea_side, fleet_conf):
	"""
	typical_config = [
	(1, 4),  # one huge
	(2, 3),  # two bigs
	(3, 2),  # three mediums
	(4, 1)]  # four smalls
	"""
	ships = []
	sea = [' '] * (sea_side**2)
	for ship in fleet_conf:
		for i in xrange(ship[0]):
			ships.append(randomly_place_ship(ship[1], sea))
	return ships

def randomly_place_ship(size, sea):
	sea_side = int(math.sqrt(len(sea)))
	pos = generate_random_position(size, sea_side)
	while not is_squares_available(sea, pos):
		pos = generate_random_position(size, sea_side)
	occupy_squares(sea, pos)
	return pos

def generate_random_position(ship_size, sea_side):
	horizontal = random.choice((True, False))
	h = random.randrange(sea_side - (ship_size if horizontal else 0))
	v = random.randrange(sea_side - (0 if horizontal else ship_size))
	index = v * sea_side + h
	orient = 1 if horizontal else sea_side
	return [index + i * orient for i in xrange(ship_size)]

def is_squares_available(sea, pos):
	for i in pos:
		if sea[i] != ' ':
			return False
	return True

def occupy_squares(sea, pos):
	S = int(math.sqrt(len(sea)))
	for i in pos:
		assert sea[i] == ' '
		sea[i] = '#'
		# horizontal margin
		if i % S != 0 and i-1 >= 0 and i-1 < len(sea) and i-1 not in pos:
			assert sea[i-1] != '#'
			sea[i-1] = '.'  # left
		if (i+1) % S != 0 and i+1 >= 0 and i+1 < len(sea) and i+1 not in pos:
			assert sea[i+1] != '#'
			sea[i+1] = '.'  # right
		# vertical margin
		if i-S >= 0 and i-S < len(sea) and i-S not in pos:
			assert sea[i-S] != '#'
			sea[i-S] = '.'  # up
		if i+S >= 0 and i+S < len(sea) and i+S not in pos:
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
