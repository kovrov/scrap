import math
from utils import normalizeVector2, addVectors2, subtractVector2, distanceBetweenPoints2
from pyglet.window import key

# default key mapping
keys = {'move_up':       key.E,
        'move_down':     key.D,
        'move_left':     key.S,
        'move_right':    key.F}


SPEED = 64.0 # px/sec

class Ship(object):
	def __init__(self, scheduler):
		self.scheduler = scheduler
		self.pos = (0,0)
		self.task = None

	def move(self, x, y):
		if self.task:
			self.task.close()
		if self.pos != (x, y):
			self.task = self.move_task((x, y))
			self.task.next()
			self.scheduler.append(self.task)

	def move_task(self, pos):
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

	def key_handler(self, pressed, frame_time):
		x = y = 0
		if pressed[keys['move_up']]:    y += 1
		if pressed[keys['move_down']]:  y -= 1
		if pressed[keys['move_left']]:  x -= 1
		if pressed[keys['move_right']]: x += 1
		if x or y:
			real_x = self.pos[0] + x * SPEED * frame_time
			real_y = self.pos[1] + y * SPEED * frame_time
			self.pos = (real_x, real_y)
			if self.task:
				self.task.close()
