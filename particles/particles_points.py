# http://www.opengl.org/registry/specs/ARB/point_parameters.txt
from pyglet.gl import gl_info
assert gl_info.have_extension("GL_ARB_point_parameters"), "ARB_point_parameters not available"

from pyglet.gl import *
import random
import math

g_slowdown = 2.0

# Query for the max point size supported by the hardware
maxSize = c_float(0.0)
maxSize = GLfloat(0.0)
glGetFloatv(GL_POINT_SIZE_MAX_ARB, maxSize)
print "GL_POINT_SIZE_MAX_ARB", maxSize.value # 256.0


def draw_task(texture_id, size, pos):

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
	glDisable(GL_TEXTURE_2D)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE)
	mat = (GLfloat*16)()
	viewport = (GLint*4)()

	while True:
		yield
		glGetIntegerv (GL_VIEWPORT, viewport)
		attenuation = (GLfloat*3)(0.0,  0.0, 2.0/(viewport[3]**2))

		# set point sprite parameters
		glPointParameterfvARB(GL_POINT_DISTANCE_ATTENUATION_ARB, attenuation)
		glPointParameterfARB(GL_POINT_SIZE_MAX_ARB, maxSize)
		glPointParameterfARB(GL_POINT_SIZE_MIN_ARB, 0.0)
		#glPointParameterfARB(GL_POINT_SPRITE_COORD_ORIGIN_ARB, GL_LOWER_LEFT)
		#glTexEnvf(GL_POINT_SPRITE_ARB, GL_COORD_REPLACE_ARB, GL_TRUE)
		glPointSize(1.0)
				
		# draw the point sprites 

		glPushMatrix()
		glTranslatef(*pos)
		glBegin(GL_POINTS)
		for p in particles:
			# draw
			glColor4f(p['r'], p['g'], p['b'], p['life'])
			glVertex3f(p['x'], p['y'], p['z'])

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
		glEnd()
		glPopMatrix()
	glEnable(GL_BLEND)
