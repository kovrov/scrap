from utils import normalizeVector2, addVectors2, subtractVector2, distanceBetweenPoints2
import math

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

		while x_cmp() or y_cmp():
			time = yield
			if time > 0.0:
				self.pos = (self.pos[0] + vect[0] * SPEED * time,
				            self.pos[1] + vect[1] * SPEED * time)

		self.pos = (x_rnd(self.pos[0]), y_rnd(self.pos[1]))
