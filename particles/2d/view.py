import math
from pyglet.gl import *
import tasks

# state variables. module-level private.
width = 0
height = 0
origin = (0.0, 0,0)
zoom_level = 0
task = None

def screen2world(x, y):
	scale = 1.0 + zoom_level / 10.0
	real_x = origin[0] + (x - width  / 2.0) * scale
	real_y = origin[1] + (y - height / 2.0) * scale
	return (real_x, real_y)


def zoom(z):
	global zoom_level
	if 1.0 + (zoom_level + z) / 10.0 > 0.0:  # max zoom in
		zoom_level += z
		update_projection()


def resize(w, h):
	global width, height
	width, height = w, h
	update_projection()


def update_projection():
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	scale = 1.0 + zoom_level / 10.0
	left   = origin[0] + (-width / 2.0) * scale
	right  = origin[0] + ( width - width  / 2.0) * scale
	bottom = origin[1] + (-height / 2.0) * scale
	top    = origin[1] + ( height - height / 2.0) * scale
	if zoom_level == 0:
		left, right, bottom, top = math.floor(left), math.floor(right), math.floor(bottom), math.floor(top)
	glOrtho(left, right, bottom, top, -1, 1)
	glMatrixMode(GL_MODELVIEW)

def pan(vect):
	global task
	if task:
		task.close()
		task = None
	if not vect:
		return
	task = pan_task(vect)
	tasks.append(task)

def pan_task(vect):
	global origin
	x, y = vect
	scale = 1.0 + zoom_level / 10.0
	speed = height / 2.0 * scale
	while True:
		time = yield
		real_x = x * speed * time
		real_y = y * speed * time
		origin = (origin[0] + real_x, origin[1] + real_y)
		update_projection()
