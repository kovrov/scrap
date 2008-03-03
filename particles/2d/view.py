import math
from pyglet.gl import *

# state variables. module-level private.
width = 0
height = 0
origin = (0.0, 0,0)
g_zoom = 0


def screen2world(x, y):
	scale = 1.0 + g_zoom / 10.0
	real_x = origin[0] + (x - width  / 2.0) * scale
	real_y = origin[1] + (y - height / 2.0) * scale
	return (real_x, real_y)


def zoom(z):
	global g_zoom
	if 1.0 + (g_zoom + z) / 10.0 > 0.0:  # max zoom in
		g_zoom += z
		update_projection()


def resize(w, h):
	global width, height
	width, height = w, h
	update_projection()


def update_projection():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	scale = 1.0 + g_zoom / 10.0
	left   = origin[0] + (-width / 2.0) * scale
	right  = origin[0] + ( width - width  / 2.0) * scale
	bottom = origin[1] + (-height / 2.0) * scale
	top    = origin[1] + ( height - height / 2.0) * scale
	if g_zoom == 0:
		left, right, bottom, top = math.floor(left), math.floor(right), math.floor(bottom), math.floor(top)
	glOrtho(left, right, bottom, top, -1, 1)
	glMatrixMode(GL_MODELVIEW)

def pan():
	pass
