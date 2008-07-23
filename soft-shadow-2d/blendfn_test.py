import math
import pyglet
from pyglet.window import key
from pyglet.gl import *

gl_symbols = {	GL_CONSTANT_ALPHA: "GL_CONSTANT_ALPHA",
				GL_CONSTANT_COLOR: "GL_CONSTANT_COLOR",
				GL_DST_ALPHA: "GL_DST_ALPHA",
				GL_DST_COLOR: "GL_DST_COLOR",
				GL_ONE: "GL_ONE",
				GL_ONE_MINUS_CONSTANT_ALPHA: "GL_ONE_MINUS_CONSTANT_ALPHA",
				GL_ONE_MINUS_CONSTANT_COLOR: "GL_ONE_MINUS_CONSTANT_COLOR",
				GL_ONE_MINUS_DST_ALPHA: "GL_ONE_MINUS_DST_ALPHA",
				GL_ONE_MINUS_DST_COLOR: "GL_ONE_MINUS_DST_COLOR",
				GL_ONE_MINUS_SRC_ALPHA: "GL_ONE_MINUS_SRC_ALPHA",
				GL_ONE_MINUS_SRC_COLOR: "GL_ONE_MINUS_SRC_COLOR",
				GL_SRC_ALPHA: "GL_SRC_ALPHA",
				GL_SRC_ALPHA_SATURATE: "GL_SRC_ALPHA_SATURATE",
				GL_SRC_COLOR: "GL_SRC_COLOR",
				GL_ZERO: "GL_ZERO"}

sfactor = (	GL_ZERO,
			GL_ONE,
			GL_SRC_COLOR,
			GL_ONE_MINUS_SRC_COLOR,
			GL_DST_COLOR,
			GL_ONE_MINUS_DST_COLOR,
			GL_SRC_ALPHA,
			GL_ONE_MINUS_SRC_ALPHA,
			GL_DST_ALPHA,
			GL_ONE_MINUS_DST_ALPHA,
			#GL_CONSTANT_COLOR,
			#GL_ONE_MINUS_CONSTANT_COLOR,
			#GL_CONSTANT_ALPHA,
			#GL_ONE_MINUS_CONSTANT_ALPHA,
			GL_SRC_ALPHA_SATURATE)
dfactor = (	GL_ZERO,
			GL_ONE,
			GL_SRC_COLOR,
			GL_ONE_MINUS_SRC_COLOR,
			GL_DST_COLOR,
			GL_ONE_MINUS_DST_COLOR,
			GL_SRC_ALPHA,
			GL_ONE_MINUS_SRC_ALPHA,
			GL_DST_ALPHA,
			GL_ONE_MINUS_DST_ALPHA,
			#GL_CONSTANT_COLOR,
			#GL_ONE_MINUS_CONSTANT_COLOR,
			#GL_CONSTANT_ALPHA,
			#GL_ONE_MINUS_CONSTANT_ALPHA
			)
factors = [(s,d) for d in dfactor for s in sfactor]
shadow_factor = 0
geometry_factor = 0
geometry_factors = factors
shadow_factors = (	(GL_SRC_ALPHA, GL_DST_ALPHA),
					(GL_SRC_ALPHA_SATURATE, GL_ONE_MINUS_SRC_ALPHA),
					(GL_ONE_MINUS_DST_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
					(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
					(GL_ONE_MINUS_SRC_COLOR, GL_ONE_MINUS_SRC_ALPHA),
					(GL_ZERO, GL_ONE_MINUS_SRC_ALPHA),
					(GL_SRC_ALPHA, GL_ONE))

# Create template config
config = pyglet.gl.Config()
config.buffer_size = 32
# Create a window using this config
win = pyglet.window.Window(config=config, resizable=True, vsync=True)

@win.event
def on_draw():
	#glClearColor(0.0, 0.0, 0.0, 0.3)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(win.width/2, win.height/2, 0.)

	glEnable(GL_BLEND)
	glBlendFunc(*shadow_factors[shadow_factor])
	glColorMask(False, False, False, True)  # disable color buffer
	draw_light( 50,  50, 200, (1.,0.,0.))
	draw_light(-50, -50, 200, (0.,0.,1.))
	glColorMask(True, True, True, True)  # enable color buffer

	glBlendFunc(*geometry_factors[geometry_factor])#GL_ONE_MINUS_DST_COLOR, GL_ONE_MINUS_SRC_COLOR
	draw_scene()

	# apply light color
	#glEnable(GL_BLEND)
	#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	#draw_light( 50,  50, 200, (1.,0.,0.))
	#draw_light(-50, -50, 200, (0.,0.,1.))


def draw_light(x, y, radius, color=(1., 1., 1.), intensity=1., numSubdivisions=32):
	increment = math.pi*2 / numSubdivisions
	glBegin(GL_TRIANGLE_FAN)
	glColor4f(color[0], color[1], color[2], intensity)
	glVertex2f(x, y)
	glColor4f(color[0], color[1], color[2], 0.)
	for i in xrange(numSubdivisions+1):
		glVertex2f(radius*math.cos(i*increment)+x, radius*math.sin(i*increment)+y)
	glEnd()

def draw_scene():
	glBegin(GL_TRIANGLES)
	glColor3f(0., 1., 0.)
	glVertex2f( 200., -200.)
	glVertex2f( 200.,  200.)
	glVertex2f(-200.,  200.)
	glColor3f(1., 0., 0.)
	glVertex2f(-200.,  200.)
	glVertex2f(-200., -200.)
	glVertex2f( 200., -200.)
	glEnd()

@win.event
def on_mouse_motion(x, y, dx, dy):
	pass

@win.event
def on_key_press(symbol, modifiers):
	global shadow_factor, geometry_factor

	if symbol == key.PAGEUP:
		shadow_factor += 1
		if len(shadow_factors) < shadow_factor+1:
			shadow_factor = 0
			print "#"
	if symbol == key.PAGEDOWN:
		shadow_factor -= 1
		if 0 > shadow_factor:
			shadow_factor = len(shadow_factors)-1
			print "#"

	if symbol == key.HOME:
		geometry_factor += 1
		if len(geometry_factors) < geometry_factor+1:
			geometry_factor = 0
			print "#"
	if symbol == key.END:
		geometry_factor -= 1
		if 0 > geometry_factor:
			geometry_factor = len(geometry_factors)-1
			print "#"

	print "shadow", gl_symbols[shadow_factors[shadow_factor][0]], gl_symbols[shadow_factors[shadow_factor][1]]
	print "geometry", gl_symbols[geometry_factors[geometry_factor][0]], gl_symbols[geometry_factors[geometry_factor][1]]

"""
shadow GL_SRC_ALPHA GL_ONE_MINUS_SRC_ALPHA
geometry GL_ONE_MINUS_DST_COLOR GL_ONE_MINUS_SRC_COLOR

shadow GL_ONE_MINUS_DST_ALPHA GL_ONE_MINUS_SRC_ALPHA
geometry GL_ONE_MINUS_DST_COLOR GL_ONE_MINUS_SRC_COLOR

shadow GL_SRC_ALPHA_SATURATE GL_ONE_MINUS_SRC_ALPHA
geometry GL_ONE_MINUS_DST_COLOR GL_ONE_MINUS_SRC_COLOR

shadow GL_SRC_ALPHA GL_DST_ALPHA
geometry GL_ONE_MINUS_DST_COLOR GL_ONE_MINUS_SRC_COLOR

shadow GL_ZERO GL_ONE_MINUS_SRC_ALPHA
geometry GL_ONE_MINUS_DST_COLOR GL_ONE_MINUS_SRC_COLOR
"""

pyglet.app.run()
