"""
Battleship map generator
"""
import math
import random

class ComputerPlayer:
	def __init__(self, sea_side, fleet_conf):
		self.sea_side = sea_side
		self.shots = range(self.sea_side ** 2)
		self.targets = []  # hit, but not yet sunk opponent ships

	def shot(self):
		assert len(self.shots) > 0
		for target in self.targets:
			if len(target) < 2:
				get_squares = neighbor_squares
			else:
				span = abs(target[0] - target[1])
				if span == 1:  # horisontal target
					get_squares = horizontal_neighbor_squares
				elif span == self.sea_side: # vertical target
					get_squares = vertical_neighbor_squares
				else:
					raise Exception("this is impossible!")
			for i in target:
				for shot in get_squares(i, self.sea_side):
					if shot in self.shots:
						self.shots.remove(shot)
						return (shot % 10, shot // 10)
			raise Exception("this is impossible!")
		shot = random.choice(self.shots)
		self.shots.remove(shot)
		print "removing shot", shot
		return (shot % 10, shot // 10)

	def track(self, shot, res):
		assert res in ('miss', 'hit', 'sunk')
		if res == 'miss':
			return
		index = shot[1] * self.sea_side + shot[0]
		print index, ":"
		# clear diagonal shots
		for i in diagonal_squares(index, self.sea_side):
			if i in self.shots:
				self.shots.remove(i)
				print "removing diagonal", i
		# find the target if its in not a new one
		target = None
		for t in self.targets:
			assert index not in t
			for n in neighbor_squares(index, self.sea_side):
				if n in t:
					target = t
					break
		if res == 'hit':
			if target is not None:
				target.append(index)
				return
			self.targets.append([index,])
		if res == 'sunk':
			for n in neighbor_squares(index, self.sea_side):
				if n in self.shots:
					self.shots.remove(n)
					print "removing sunk shot", n
			if target is not None:
				self.targets.remove(target)
				for i in target:
					for n in neighbor_squares(i, self.sea_side):
						if n in self.shots:
							self.shots.remove(n)
							print "removing sunk target", n

def diagonal_squares(index, side):
	res = []
	length = side ** 2
	pos = index - side + 1  # upper-right
	if pos % side != 0 and pos >= 0 and pos < length:
		res.append(pos)
	pos = index - side - 1  # upper-left
	if index % side != 0 and pos >= 0 and pos < length:
		res.append(pos)
	pos = index + side + 1  # lower-right
	if pos % side != 0 and pos >= 0 and pos < length:
		res.append(pos)
	pos = index + side - 1  # lower-left
	if index % side != 0 and pos >= 0 and pos < length:
		res.append(pos)
	return res

def neighbor_squares(index, side):
	return horizontal_neighbor_squares(index, side) + vertical_neighbor_squares(index, side)

def horizontal_neighbor_squares(index, side):
	res = []
	length = side ** 2
	pos = index - 1  # left
	if index % side != 0 and pos >= 0 and pos < length:
		res.append(pos)
	pos = index + 1  # right
	if pos % side != 0 and pos >= 0 and pos < length:
		res.append(pos)
	return res

def vertical_neighbor_squares(index, side):
	res = []
	length = side ** 2
	pos = index - side  # up
	if pos >= 0 and pos < length:
		res.append(pos)
	pos = index + side  # down
	if pos >= 0 and pos < length:
		res.append(pos)
	return res

###--------------

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
	for quantity, size in fleet_conf:
		for i in xrange(quantity):
			ships.append(randomly_place_ship(size, sea))
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
	x = random.randrange(sea_side - (ship_size if horizontal else 0))
	y = random.randrange(sea_side - (0 if horizontal else ship_size))
	return (x, y, ship_size, horizontal)

def is_squares_available(sea, ship):
	sea_side = int(math.sqrt(len(sea)))
	x, y, ship_size, horizontal = ship
	index = y * sea_side + x
	orient = 1 if horizontal else sea_side
	for i in [index + i * orient for i in xrange(ship_size)]:
		if sea[i] != ' ':
			return False
	return True

def occupy_squares(sea, ship):
	sea_side = int(math.sqrt(len(sea)))
	x, y, ship_size, horizontal = ship
	index = y * sea_side + x
	orient = 1 if horizontal else sea_side
	pos = [index + i * orient for i in xrange(ship_size)]
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
