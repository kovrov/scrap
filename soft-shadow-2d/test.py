import math
import pyglet
from pyglet.gl import *


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
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()

	radius = 128
	intensity = 1.
	numSubdivisions = 32
	increment = math.pi*2 / numSubdivisions

	glTranslatef(win.width/2, win.height/2, 0.)
	glBegin(GL_TRIANGLE_FAN)
	glColor4f(0., 0., 0., intensity)
	glVertex2f(0., 0.)
	glColor4f(0., 0., 0., 0.)
	for i in xrange(numSubdivisions+1):
		glVertex2f(radius*math.cos(i*increment), radius*math.sin(i*increment))
	glEnd()

@win.event
def on_mouse_motion(x, y, dx, dy):
	print "on_mouse_motion"

pyglet.app.run()
