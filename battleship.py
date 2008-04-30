"""
Battleship map generator
"""
import math
import random

def generate_ship_pos(ship_size, sea_side):
	horizontal = random.choice((True, False))
	h = random.randrange(sea_side - (ship_size if horizontal else 0))
	v = random.randrange(sea_side - (0 if horizontal else ship_size))
	index = v * sea_side + h
	orient = 1 if horizontal else sea_side
	return [index + i * orient for i in xrange(ship_size)]

def check_pos(sea, pos):
	for i in pos:
		if sea[i] in ('#', '.'):
			return False
	return True

def update_sea(sea, pos):
	S = int(math.sqrt(len(sea)))
	for i in pos:
		sea[i] = '#'
		# horizontal padding
		if i % S != 0 and i - 1 < len(sea) and i - 1 not in pos:
			sea[i - 1] = '.'
		if i % S != (S-1) and i + 1 < len(sea) and i + 1 not in pos:
			sea[i + 1] = '.'
		# vert padding
		if i - S > 0 and i - S < len(sea) and i - S not in pos:
			sea[i - S] = '.'
		if i + S < len(sea) and i + S not in pos:
			sea[i + S] = '.'
		# upper right padding
		if i-(S-1) > 0 and (i-(S-1)) % S != 0 and i-(S-1) < len(sea) and i-(S-1) not in pos and sea[i-(S-1)] == ' ':
			sea[i-(S-1)] = '.'
		# upper left padding
		if i-(S+1) > 0 and (i-(S+1)) % S != (S-1) and i-(S+1) < len(sea) and i-(S+1) not in pos and sea[i-(S+1)] == ' ':
			sea[i-(S+1)] = '.'
		# upper right padding
		if (i + (S+1)) % S != 0 and i + (S+1) < len(sea) and i + (S+1) not in pos and sea[i + (S+1)] == ' ':
			sea[i + (S+1)] = '.'
		# lower left padding
		if (i + (S-1)) % S != (S-1) and i + (S-1) < len(sea) and i + (S-1) not in pos and sea[i + (S-1)] == ' ':
			sea[i + (S-1)] = '.'

def place_ship(size, sea):
	sea_side = int(math.sqrt(len(sea)))
	pos = generate_ship_pos(size, sea_side)
	while not check_pos(sea, pos):
		pos = generate_ship_pos(size, sea_side)
	update_sea(sea, pos)
	return generate_ship_pos(size, sea_side)


# tests

def test(sea_side, fleet_conf):
	sea = [' '] * (sea_side**2)
	for ship in fleet_conf:
		for i in xrange(ship[0]):
			place_ship(ship[1], sea)
	# print sea
	for i in xrange(sea_side):
		for j in xrange(sea_side):
			print sea[i * sea_side + j],
		print

print "'russian' config"
test(10, (	(1, 4),  # one huge
			(2, 3),  # two bigs
			(3, 2),  # three mediums
			(4, 1)))  # four smalls

print "'not russian' config"
test(10, (	(1, 5),  # one carier
			(1, 4),  # one battleship
			(1, 3),  # one cruiser
			(2, 2),  # two destroyers
			(2, 1)))  # two submarines
