from pyglet.gl import *

import random
from math import sin, cos

import utils


def flash_task(seconds):
	k = 1.0 / seconds
	t = 0.0
	while t < seconds:
		t += yield
		glClearColor(1 - k * t, 1 - k * t, 1 - k * t, 1.0)
	glClearColor(0.0, 0.0, 0.0, 1.0)


def sparks_task(pos):
	particles = tuple({
			'life': 1.0,
			'decay': random.uniform(0.5, 0.8),
			'r': 1.0, 'g': 1.0, 'b': 1.0,
			'x': 0.0, 'y': 0.0,
			#'vect': (random.uniform(-24.0, 24.0), random.uniform(-24.0, 24.0)),
			'vect': utils.normalizeVector2((random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))),
			'speed': random.uniform(0.0, 64.0)
					} for i in xrange(64))
	done = False
	while not done:
		time = yield

		# TODO: push attributes
		glDisable(GL_DEPTH_TEST)  # TODO: see if this integrates well with rest of render...
		#glEnable(GL_BLEND)
		#glBlendFunc(GL_SRC_ALPHA, GL_ONE)

		glPushMatrix()
		glTranslatef(*pos)

		glPointSize(5.0)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		done = True
		for p in particles:
			if p['life'] > 0.0:
				done = False
				# draw
				glColor4f(p['r'], p['g'], p['b'], p['life'])
				glVertex2f(p['x'], p['y'])
				# update
				p['life'] -= p['decay'] * time
				p['x'] += p['vect'][0] * p['speed'] * time
				p['y'] += p['vect'][1] * p['speed'] * time
				# task control

		glEnd()
		glDisable(GL_POINT_SMOOTH)
		glPopMatrix()
