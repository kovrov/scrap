from pyglet.gl import *
from pyglet import image
from pyglet import window
from pyglet.window import key
import pyglet.clock
import random

from particles_points import draw_task as draw_particles_points
from particles_quads import draw_task as draw_particles_quads
from cube import draw_task as draw_cube
import camera

def main():
	win = window.Window(resizable=True, visible=False, vsync=False)
	@win.event
	def on_resize(width, height):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(90.0, float(width) / float(height), 0.0, 256.0)  # fov, ratio, near, far
		glMatrixMode(GL_MODELVIEW)
		glViewport(0, 0, width, height)

	win.paused = False
	@win.event
	def on_key_press(sym, mod):
		if sym == key.ESCAPE:
			win.has_exit = True
		if sym == key.SPACE:
			win.paused = not win.paused
		if sym == key.E:
			camera.move(5, (0.0, 0.0, -1.0))
		if sym == key.D:
			camera.move(5, (0.0, 0.0, 1.0))
		if sym == key.F:
			#camera.move(5, (1.0, 0.0, 0.0))
			camera.rotate_horizontal(15)
		if sym == key.S:
			#camera.move(5, (-1.0, 0.0, 0.0))
			camera.rotate_horizontal(-15)
	# init
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.5, 0., 0.0)
	glClearDepth(1.0)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glEnable(GL_TEXTURE_2D)

	win.set_visible()
	clock = pyglet.clock.Clock()

	texture = image.load('smoke.png').texture
	glBindTexture(GL_TEXTURE_2D, texture.id)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

	camera.position = [0.0, 0.0, 10.0]
	cam = camera.draw_task()
	left_cube = draw_cube(5.0, (-5.0, 0.0, 0.0))
	right_cube = draw_cube(5.0, ( 5.0, 0.0, 0.0))
	left_quads = draw_particles_quads(texture.id, 1.0, (-5.0, 0.0, 0.0)) # left
	right_points = draw_particles_points(texture.id, 1.0, (5.0, 0.0, 0.0)) # right

	while not win.has_exit:
		win.dispatch_events()
		if not win.paused:
			dt = clock.tick()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			cam.next()
			right_cube.next()
			left_cube.next()
			right_points.next()
			left_quads.next()
			win.flip()
	print "fps:  %d" % clock.get_fps()


if __name__ == "__main__":
	main()
