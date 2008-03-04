# lib
import math
# framework
import pyglet
from pyglet.window import key
from pyglet.gl import *
# project
from utils import normalizeVector2, addVectors2, subtractVector2, distanceBetweenPoints2
import tasks

# default key mapping
keys = {'move_up':       key.E,
        'move_down':     key.D,
        'move_left':     key.S,
        'move_right':    key.F}


SPEED = 64.0 # px/sec

class Ship(object):
	def __init__(self):
		self.texture = pyglet.resource.image('test.png').get_texture()
		self.texture.anchor_x = self.texture.width / 2
		self.texture.anchor_y = self.texture.height / 2
		self.pos = (0,0)
		self.task = None

	def translate(self, x, y):
		if self.task:
			self.task.close()
		if self.pos != (x, y):
			self.task = self.translate_task((x, y))
			tasks.append(self.task)

	def translate_task(self, pos):
		vect = normalizeVector2(subtractVector2(pos, self.pos))
		# set up stop condition checker
		if self.pos[0] > pos[0]:
			x_cmp = lambda: self.pos[0] > pos[0]
			x_rnd = math.ceil
		else:
			x_cmp = lambda: self.pos[0] < pos[0]
			x_rnd = math.floor
		if self.pos[1] > pos[1]:
			y_cmp = lambda: self.pos[1] > pos[1]
			y_rnd = math.ceil
		else:
			y_cmp = lambda: self.pos[1] < pos[1]
			y_rnd = math.floor
		# move until stop condition occures
		while x_cmp() or y_cmp():
			time = yield
			if time > 0.0:
				self.pos = (self.pos[0] + vect[0] * SPEED * time,
				            self.pos[1] + vect[1] * SPEED * time)
		#
		self.pos = (x_rnd(self.pos[0]), y_rnd(self.pos[1]))

	def move(self, vect):
		if self.task:
			self.task.close()
			self.task = None
		if not vect:
			return
		self.task = self.move_task(vect)
		tasks.append(self.task)

	def move_task(self, vect):
		x, y = vect
		while True:
			time = yield
			real_x = self.pos[0] + x * SPEED * time
			real_y = self.pos[1] + y * SPEED * time
			self.pos = (real_x, real_y)

	def draw(self):
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glColor4f(1.0, 1.0, 1.0, 1.0)
		self.texture.blit(*self.pos)
