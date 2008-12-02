"""
The "game" is a manager, who:
1. load level|world
2. ...
"""
import pyglet
import data

class Game:
	def __init__(self):
		self.tmp = data.loadCube()

	def update(self, td):
		pass # rotate cube
