from pyglet.gl import *
import random
import camera

g_slowdown = 1.1

def draw_task(texture_id, size, pos):
	size /= 2.0
	particles = [{
			'life': 1.0,
			'fade': random.uniform(0.1, 0.004),
			'r': 1.0, 'g': 1.0, 'b': 1.0,
			'x': 0.0, 'y': 0.0, 'z': 0.0,
			'xi': float(random.uniform(-0.5, 0.5)),
			'yi': float(random.uniform(-0.1, 0.1)),
			'zi': float(random.uniform(-0.5, 0.5)),
			'xg': 0.0, 'yg': -0.1, 'zg': 0.0,
					} for i in xrange(50)]

	while True:
		yield
		glDisable(GL_DEPTH_TEST)  # TODO: see if this integrates well with rest of render...
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE)
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, texture_id)
		glPushMatrix()
		glTranslatef(*pos)
		glRotatef(-camera.yaw, 0.0, 1.0, 0.0);
		glRotatef(-camera.pitch, 1.0, 0.0, 0.0);
		restart = False
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
			p['x'] += p['xi']
			p['y'] += p['yi']
			p['z'] += p['zi']
			p['xi'] = p['xi'] / g_slowdown + p['xg']
			p['yi'] = p['yi'] / g_slowdown + p['yg']
			p['zi'] = p['zi'] / g_slowdown + p['zg']

			if p['life'] < 0.0: continue
		glPopMatrix()
