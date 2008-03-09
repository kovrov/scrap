import random
import time
from math import sin, cos

from pyglet.gl import *

import utils


def flash_task(seconds):
	k = 1.0 / seconds
	t = 0.0
	while t < seconds:
		t += yield
		glClearColor(1 - k * t, 1 - k * t, 1 - k * t, 1.0)
	glClearColor(0.0, 0.0, 0.0, 1.0)


class Sparks:
	def __init__(self, pos):
		self.pos = pos
		self.particles = tuple({
				'life': 1.0,
				'decay': random.uniform(0.5, 0.8),
				'r': 1.0, 'g': 1.0, 'b': 1.0,
				'x': 0.0, 'y': 0.0,
				#'vect': (random.uniform(-24.0, 24.0), random.uniform(-24.0, 24.0)),
				'vect': utils.normalizeVector2((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))),
				'speed': random.uniform(0.0, 64.0)
						} for i in xrange(64))

	def draw(self):
		# TODO: push attributes
		glDisable(GL_DEPTH_TEST)  # TODO: see if this integrates well with rest of render...
		#glEnable(GL_BLEND)
		#glBlendFunc(GL_SRC_ALPHA, GL_ONE)

		glPushMatrix()
		glTranslatef(*self.pos)

		glPointSize(5.0)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		for p in self.particles:
			if p['life'] > 0.0:
				glColor4f(p['r'], p['g'], p['b'], p['life'])
				glVertex2f(p['x'], p['y'])
		glEnd()
		glDisable(GL_POINT_SMOOTH)
		glPopMatrix()

	def update_task(self):
		done = False
		while not done:
			time = yield
			done = True
			for p in self.particles:
				if p['life'] > 0.0:
					done = False
					p['life'] -= p['decay'] * time
					p['x'] += p['vect'][0] * p['speed'] * time
					p['y'] += p['vect'][1] * p['speed'] * time


class Ruler:
	def __init__(self, begin, end):
		self.begin = begin
		self.end = end
		self.label = pyglet.text.Label(str(self.begin), x=end[0], y=end[1])
		self.time = time.clock()

	def draw(self):
		glBegin(GL_LINES)
		glColor4f(1.0, 1.0, 1.0, 1.0)
		glVertex2f(*self.begin)
		glVertex2f(*self.end)
		glEnd()
		t = time.clock()
		if (t - self.time > 0.25):
			self.time = t
			dist = utils.distanceBetweenPoints2(self.begin, self.end)
			self.label.text = str(dist)
		self.label.draw()
