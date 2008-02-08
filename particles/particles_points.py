from pyglet.gl import *
import random

g_slowdown = 2.0

# Query for the max point size supported by the hardware
maxSize = c_float(0.0)
glGetFloatv(GL_POINT_SIZE_MAX, pointer(maxSize))
print "GL_POINT_SIZE_MAX", maxSize.value # 256.0
g_maxSize = maxSize.value
g_maxSize = 10.0
a = 1
b = 0.0#1.0/g_maxSize**2
c = 0.01#1.0/g_maxSize

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
	# This is how will our point sprite's size will be modified by 
	# distance from the viewer
	glPointParameterfv(GL_POINT_DISTANCE_ATTENUATION, (c_float*3)(a,b,c))
	glPointSize(g_maxSize)
	# The alpha of a point is calculated to allow the fading of points instead
	# of shrinking them past a defined threshold size. The threshold is defined
	# by GL_POINT_FADE_THRESHOLD_SIZE_ARB and is not clamped to the minimum and
	# maximum point sizes.
	glPointParameterf(GL_POINT_FADE_THRESHOLD_SIZE, 60.0)
	glPointParameterf(GL_POINT_SIZE_MIN, 1.0)
	glPointParameterf(GL_POINT_SIZE_MAX, g_maxSize)

	while True:
		yield
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
