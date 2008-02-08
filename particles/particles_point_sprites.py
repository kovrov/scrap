from pyglet.gl import gl_info
assert gl_info.have_extension("GL_ARB_point_sprite"), "ARB_point_sprite not available"

from pyglet.gl import *
import random

# see:
# http://www.opengl.org/registry/specs/ARB/point_sprite.txt
# http://www.opengl.org/registry/specs/ARB/point_parameters.txt

g_slowdown = 2.0

# Query for the max point size supported by the hardware
g_maxSize = c_float(0.0)
glGetFloatv(GL_POINT_SIZE_MAX_ARB, pointer(g_maxSize))
# Clamp size to 100.0f or the sprites could get a little too big on some of the
# newer graphic cards. My ATI card at home supports a max point size of 1024.0!
if (g_maxSize.value > 100.0): g_maxSize.value = 100.0

def draw_task(texture_id):
	particles = [{
			'life': 1.0,
			'fade': random.uniform(0.1, 0.004),
			#'r': 1.0, 'g': 1.0, 'b': 1.0,
			'r': 0.32, 'g': 0.32, 'b': 0.32,
			'x': 0.0, 'y': 0.0, 'z': 0.0,
			'xi': float(random.randint(-250, 250)),
			'yi': float(random.randint(-250, 250)),
			'zi': float(random.randint(-250, 250)),
			'xg': 0.0, 'yg': -0.8, 'zg': 0.0,
					} for i in xrange(1000)]
	glDisable(GL_DEPTH_TEST)  # TODO: see if this integrates well with rest of render...
	glEnable(GL_POINT_SPRITE_ARB) # affects global state
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE)
	# This is how will our point sprite's size will be modified by 
	# distance from the viewer
	glPointParameterfvARB(GL_POINT_DISTANCE_ATTENUATION_ARB, (c_float*3)(1.0, 0.0, 0.01))
	glPointSize(g_maxSize)
	# The alpha of a point is calculated to allow the fading of points instead
	# of shrinking them past a defined threshold size. The threshold is defined
	# by GL_POINT_FADE_THRESHOLD_SIZE_ARB and is not clamped to the minimum and
	# maximum point sizes.
#	glPointParameterfARB(GL_POINT_FADE_THRESHOLD_SIZE_ARB, 60.0)
#	glPointParameterfARB(GL_POINT_SIZE_MIN_ARB, 1.0)
#	glPointParameterfARB(GL_POINT_SIZE_MAX_ARB, g_maxSize)
	# Specify point sprite texture coordinate replacement mode for each
	# texture unit (see ARB_point_sprite specs)
	glTexEnvi(GL_POINT_SPRITE_ARB, GL_COORD_REPLACE_ARB, GL_TRUE) # per-texture unit

	while True:
		yield
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glBindTexture(GL_TEXTURE_2D, texture_id)
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
	glEnable(GL_BLEND)
	glDisable(GL_POINT_SPRITE_ARB)
