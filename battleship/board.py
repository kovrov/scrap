"""
This module purpose is to help track of player's fleets.
It incapsulates implementation of tasks like fleet setup, player shots,
validation of actions, and provides status information.
This is typical "model" in MVC terminology.
"""

class SeaGrid:
	def __init__(self, side):
		self.side = side
		self.grid = [' '] * (side**2)
		self.ships = []

	def place_ship(self, indices):
		row = self.side
		grid_len = len(self.grid)
		for i in indices:
			assert self.grid[i] == ' '
			self.grid[i] = '#'
			# horizontal margin
			pos = i - 1  # left
			if i % row != 0 and pos >= 0 and pos < grid_len:
				if pos not in indices:
					assert self.grid[pos] != '#'
					self.grid[pos] = '.'
			pos = i + 1  # right
			if pos % row != 0 and pos >= 0 and pos < grid_len:
				if pos not in indices:
					assert self.grid[pos] != '#'
					self.grid[pos] = '.'
			# vertical margin
			pos = i - row  # up
			if pos >= 0 and pos < grid_len:
				if pos not in indices:
					assert self.grid[pos] != '#'
					self.grid[pos] = '.'
			pos = i + row  # down
			if pos >= 0 and pos < grid_len:
				if pos not in indices:
					assert self.grid[pos] != '#'
					self.grid[pos] = '.'
			# diagonal margins
			pos = i - row + 1  # upper-right
			if pos % row != 0 and pos >= 0 and pos < grid_len:
				assert self.grid[pos] != '#'
				self.grid[pos] = '.'
			pos = i - row - 1  # upper-left
			if i % row != 0 and pos >= 0 and pos < grid_len:
				assert self.grid[pos] != '#'
				self.grid[pos] = '.'
			pos = i + row + 1  # lower-right
			if pos % row != 0 and pos >= 0 and pos < grid_len:
				assert self.grid[pos] != '#'
				self.grid[pos] = '.'
			pos = i + row - 1  # lower-left
			if i % row != 0 and pos >= 0 and pos < grid_len:
				assert self.grid[pos] != '#'
				self.grid[pos] = '.'
		self.ships.append(indices)

	def shoot_square(self, coords):
		index = coords[1] * self.side + coords[0]
		if self.grid[index] != '#':
			self.grid[index] = '*'
			return 'miss'
		self.grid[index] = 'x'
		# update ships list
		for ship in self.ships:
			if index in ship:
				for i in ship:
					if self.grid[i] == '#':
						return 'hit'
				self.ships.remove(ship)
				return 'sunk'
		raise RuntimeError("board integrity compromised")

	def has_ships(self):
		return len(self.ships) > 0
