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
factor = 0
selected_factors = ((GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA),
					(GL_SRC_ALPHA,GL_ONE),
					(GL_SRC_ALPHA,GL_DST_ALPHA))

win = pyglet.window.Window(resizable=True, vsync=True)

def render(scene):
	glDepthMask(true)
	glClearDepth(1.)
	glClearColor(0., 0., 0., 0.)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glMatrixMode(GL_TEXTURE)
	glLoadIdentity()
	glDisable(GL_CULL_FACE)

	findVisibleLights(scene)
	# First we need to fill the z-buffer
	findVisibleObjects(scene, null)
	fillZBuffer()
	# For every light
	for currentLight in visibleLights:
		# Clear current alpha
		clearFramebufferAlpha(scene, currentLight)
		# Load new alpha
		writeFramebufferAlpha(currentLight)
		# Mask off shadow regions
		mergeShadowHulls(scene, currentLight)
		# Draw geometry pass
		drawGeometryPass(currentLight)
	# Emmissive / self illumination pass
	# ..


@win.event
def on_draw():
	glClearColor(0.5, 0.5, 0.5, 0.)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(win.width/2, win.height/2, 0.)

	glDisable(GL_BLEND)
	draw_scene()

	glEnable(GL_BLEND)
	glBlendFunc(*selected_factors[factor])
	draw_light( 50,  50, 200, (1.,0.,0.))
	draw_light(-50, -50, 200, (0.,0.,1.))


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
	glColor3f(0.5, 0., 0.)
	glVertex2f(-200.,  200.)
	glVertex2f(-200., -200.)
	glVertex2f( 200., -200.)
	glEnd()

@win.event
def on_mouse_motion(x, y, dx, dy):
	pass

@win.event
def on_key_press(symbol, modifiers):
	global factor
	#bf_light
	if symbol == key.PAGEUP:
		factor += 1
		if len(selected_factors) < factor+1:
			factor = 0
			print "#"
	if symbol == key.PAGEDOWN:
		factor -= 1
		if 0 > factor:
			factor = len(selected_factors)-1
			print "#"
	print gl_symbols[selected_factors[factor][0]], gl_symbols[selected_factors[factor][1]]

# 83 (17, 94)
# GL_SRC_ALPHA|GL_ONE_MINUS_SRC_ALPHA (GL_SRC_ALPHA|GL_ONE, GL_SRC_ALPHA GL_DST_ALPHA)

pyglet.app.run()
