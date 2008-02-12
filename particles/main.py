from pyglet.gl import *
from pyglet import image
from pyglet import window
from pyglet.window import key
from pyglet.window import mouse
import pyglet.clock
import random
import math

import render_context

from particles_points import draw_task as draw_particles_points
from particles_quads import draw_task as draw_particles_quads
from cube import draw_task as draw_cube
import camera

def main():
	win = window.Window(resizable=True, visible=False, vsync=False)
	win.paused = False
	win.rotate = False

	@win.event
	def on_resize(width, height):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(90.0, float(width) / float(height), 0.0, 256.0)  # fov, ratio, near, far
		glMatrixMode(GL_MODELVIEW)
		glViewport(0, 0, width, height)
		render_context.width = width
		render_context.height = height
		render_context.update()

	@win.event
	def on_key_press(sym, mod):
		if sym == key.ESCAPE:
			win.has_exit = True
		if sym == key.SPACE:
			win.paused = not win.paused

	@win.event
	def on_mouse_press(x, y, buttons, modifiers):
		if buttons & mouse.LEFT:
			win.set_exclusive_mouse(True)
			win.rotate = True

	@win.event
	def on_mouse_release(x, y, button, modifiers):
		win.set_exclusive_mouse(False)
		win.rotate = False

	@win.event
	def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
		if win.rotate:
			camera.rotate_horizontal(dx * 0.2)
			camera.rotate_vertical(dy * 0.2)

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
	left_quads = draw_particles_quads(texture.id, 1.0, (-5.0, 0.0, 0.0)); left_quads.next()
	right_points = draw_particles_points(texture.id, 1.0, (5.0, 0.0, 0.0)) # right

	keys = key.KeyStateHandler()
	win.push_handlers(keys)

	while not win.has_exit:
		win.dispatch_events()
		if not win.paused:
			# update
			x = z = 0
			if keys[key.E]: z += 1
			if keys[key.D]: z -= 1
			if keys[key.F]: x += 1
			if keys[key.S]: x -= 1
			if x or z:
				camera.move(0.1, math.degrees(math.atan2(x, z)))
			# draw
			dt = clock.tick()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			cam.next()
			right_cube.next()
			left_cube.next()
			right_points.next()
			left_quads.send((camera.yaw, camera.pitch))
			win.flip()
	print "fps:  %d" % clock.get_fps()


if __name__ == "__main__":
	main()
