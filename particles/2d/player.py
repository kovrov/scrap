from utils import normalizeVector2, addVectors2, subtractVector2, distanceBetweenPoints2

SPEED = 32.0 # px/sec

class Ship(object):
	def __init__(self, scheduler):
		self.scheduler = scheduler
		self.pos = (0,0)
		self.task = None

	def move(self, x, y):
		if self.task:
			self.task.close()
		self.task = self.move_task((x, y))
		self.task.next()
		self.scheduler.append(self.task)

	def move_task(self, pos):
		vect = normalizeVector2(subtractVector2(pos, self.pos))
		x_cmp = (lambda: self.pos[0] > pos[0]) if self.pos[0] > pos[0] else (lambda: self.pos[0] < pos[0])
		y_cmp = (lambda: self.pos[1] > pos[1]) if self.pos[1] > pos[1] else (lambda: self.pos[1] < pos[1])
		#while self.pos != pos:
		while x_cmp() or y_cmp():
			time = yield
			if time > 0.0:
				self.pos = (self.pos[0] + vect[0] * SPEED * time,
				            self.pos[1] + vect[1] * SPEED * time)
