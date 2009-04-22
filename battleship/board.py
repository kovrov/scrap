"""
This module purpose is to help track of player's fleets.
It incapsulates implementation of tasks like fleet setup, player shots,
validation of actions, and provides status information.
This is typical "model" in MVC terminology.
"""

class SeaGrid:
	def __init__(self, side, ship_anchors):
		"""
		side is grid size (grid is square)
		ship_anchors is list of ships
			each ship is presented as coordinate (anchor), direction, and length
		"""
		grid_len = side**2
		grid = [' '] * grid_len

		self.side = side
		self.ships = []
		self.active_ships = []
		self.shots = []
		for anchor in ship_anchors:
			x, y, ship_size, horizontal = anchor
			index = y * side + x
			orient = 1 if horizontal else side
			indices = [index + i * orient for i in xrange(ship_size)]
			for i in indices:
				assert grid[i] == ' '
				grid[i] = '#'
				# horizontal margin
				pos = i - 1  # left
				if i % side != 0 and pos >= 0 and pos < grid_len:
					if pos not in indices:
						assert grid[pos] != '#'
						grid[pos] = '.'
				pos = i + 1  # right
				if pos % side != 0 and pos >= 0 and pos < grid_len:
					if pos not in indices:
						assert grid[pos] != '#'
						grid[pos] = '.'
				# vertical margin
				pos = i - side  # up
				if pos >= 0 and pos < grid_len:
					if pos not in indices:
						assert grid[pos] != '#'
						grid[pos] = '.'
				pos = i + side  # down
				if pos >= 0 and pos < grid_len:
					if pos not in indices:
						assert grid[pos] != '#'
						grid[pos] = '.'
				# diagonal margins
				pos = i - side + 1  # upper-right
				if pos % side != 0 and pos >= 0 and pos < grid_len:
					assert grid[pos] != '#'
					grid[pos] = '.'
				pos = i - side - 1  # upper-left
				if i % side != 0 and pos >= 0 and pos < grid_len:
					assert grid[pos] != '#'
					grid[pos] = '.'
				pos = i + side + 1  # lower-right
				if pos % side != 0 and pos >= 0 and pos < grid_len:
					assert grid[pos] != '#'
					grid[pos] = '.'
				pos = i + side - 1  # lower-left
				if i % side != 0 and pos >= 0 and pos < grid_len:
					assert grid[pos] != '#'
					grid[pos] = '.'
			ship = [ShipSegment(i % side, i // side) for i in indices]
			self.ships.append(ship)
			self.active_ships.append(ship)
		#self.grid = grid

	def shoot_square(self, coords):
		if coords in self.shots:
			raise Exception("can't shoot twice")
		self.shots.append(coords)
		x, y = coords
		for ship in self.ships:
			for segment in ship:
				if segment.x == x and segment.y == y:
					assert segment.active
					segment.active = False
					if len([s for s in ship if s.active]):
						return 'hit'
					else:
						self.active_ships.remove(ship)
						return 'sunk'
		return 'miss'

class ShipSegment(object):
	__slots__ = ('x', 'y', 'active')
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.active = True
