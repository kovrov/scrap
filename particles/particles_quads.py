from pyglet.gl import *
import random

g_slowdown = 2.0

def draw_task(texture_id, size, pos):
	size /= 2.0
	particles = [{
			'life': 1.0,
			'fade': random.uniform(0.1, 0.004),
			'r': 1.0, 'g': 1.0, 'b': 1.0,
			'x': 0.0, 'y': 0.0, 'z': 0.0,
			'xi': float(random.randint(-250, 250)),
			'yi': float(random.randint(-250, 250)),
			'zi': float(random.randint(-250, 250)),
			'xg': 0.0, 'yg': -0.8, 'zg': 0.0,
					} for i in xrange(50)]
	glDisable(GL_DEPTH_TEST)  # TODO: see if this integrates well with rest of render...
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE)

	while True:
		view_yaw, view_pitch = yield
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, texture_id)
		glPushMatrix()
		glTranslatef(*pos)
		glRotatef(-view_yaw, 0.0, 1.0, 0.0);
		glRotatef(-view_pitch, 1.0, 0.0, 0.0);
		for p in particles:
			glColor4f(p['r'], p['g'], p['b'], p['life'])

			glPushMatrix()
			glTranslatef(p['x'], p['y'], p['z'])
			glBegin(GL_QUADS)

			glTexCoord2d(0,1); glVertex2f(-size,  size)
			glTexCoord2d(0,0); glVertex2f(-size, -size)
			glTexCoord2d(1,0); glVertex2f( size, -size)
			glTexCoord2d(0,0); glVertex2f( size,  size)

			glEnd()
			glPopMatrix()

			# update
			p['life'] -= p['fade']
			p['x'] += p['xi'] / (g_slowdown * 1000)
			p['y'] += p['yi'] / (g_slowdown * 1000)
			p['z'] += p['zi'] / (g_slowdown * 1000)
			p['xi'] += p['xg']
			p['yi'] += p['yg']
			p['zi'] += p['zg']

			if p['life'] < 0.0:
				p['life'] = 1.0
				p['fade'] = random.uniform(0.1, 0.004)
				p['x'] = 0.0; p['y'] = 0.0; p['z'] = 0.0
				p['xi'] = random.uniform(-32.0, 32.0)
				p['yi'] = random.uniform(-32.0, 32.0)
				p['zi'] = random.uniform(-32.0, 32.0)
		glPopMatrix()
		glDisable(GL_TEXTURE_2D)
	glEnable(GL_BLEND)
