import math
from pyglet.gl import *
from pyglet.window import key

# default key mapping
keys = {'scroll_up':    key.UP,
        'scroll_down':  key.DOWN,
        'scroll_left':  key.LEFT,
        'scroll_right': key.RIGHT,
        'zoom_in':      key.PLUS,
        'zoom_out':     key.MINUS}

def key_handler(pressed, frame_time):
	# world scrolling
	x = y = 0
	if pressed[keys['scroll_up']]:    y += 1
	if pressed[keys['scroll_down']]:  y -= 1
	if pressed[keys['scroll_left']]:  x -= 1
	if pressed[keys['scroll_right']]: x += 1
	if x or y:
		scale = 1.0 + window.zoom / 10.0
		speed = window.height / 5.0 * scale
		x *= speed * frame_time
		y *= speed * frame_time
		update_projection(window.zoom, (window.pan[0] + x, window.pan[1] + y))

def update_projection(zoom, pan):
	if 1.0 + zoom / 10.0 > 0.0:  # max zoom in
		window.zoom = zoom
	window.pan = pan
	scale = 1.0 + window.zoom / 10.0

	glMatrixMode(gl.GL_PROJECTION)
	glLoadIdentity()

	left   = window.pan[0] + (-window.width / 2.0) * scale
	right  = window.pan[0] + ( window.width - window.width  / 2.0) * scale
	bottom = window.pan[1] + (-window.height / 2.0) * scale
	top    = window.pan[1] + ( window.height - window.height / 2.0) * scale

	if window.zoom == 0:
		left, right, bottom, top = math.floor(left), math.floor(right), math.floor(bottom), math.floor(top)

	glOrtho(left, right, bottom, top, -1, 1)
	glMatrixMode(gl.GL_MODELVIEW)
