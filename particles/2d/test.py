from pyglet.gl import *
from pyglet import clock
from pyglet import window
from pyglet.window import key
from pyglet.window import mouse
from pyglet import font
from pyglet import image

import sparks
import player

g_tasks = []

def flash_task(seconds):
	k = 1.0 / seconds
	t = 0.0
	while t < seconds:
		t += yield
		glClearColor(1 - k * t, 1 - k * t, 1 - k * t, 1.0)
	glClearColor(0.0, 0.0, 0.0, 1.0)

def update_projection(win, zoom, pan):
	if 1.0 + zoom / 10.0 > 0.0:  # max zoom in
		win.zoom = zoom
	win.pan = pan
	scale = 1.0 + win.zoom / 10.0

	glMatrixMode(gl.GL_PROJECTION)
	glLoadIdentity()

	left   = win.pan[0] + (-win.width / 2.0) * scale
	right  = win.pan[0] + ( win.width - win.width  / 2.0) * scale
	bottom = win.pan[1] + (-win.height / 2.0) * scale
	top    = win.pan[1] + ( win.height - win.height / 2.0) * scale

	glOrtho(left, right, bottom, top, -1, 1)
	glMatrixMode(gl.GL_MODELVIEW)

def main():
	win = window.Window(resizable=True, vsync=False)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	test_texture = image.load('test.png').get_texture()

	test_texture.anchor_x = test_texture.width / 2
	test_texture.anchor_y = test_texture.height / 2

	def on_resize(width, height):
		glViewport(0, 0, width, height)
		update_projection(win, win.zoom, win.pan)
		return True

	def on_key_press(symbol, modifiers):
		if symbol == key.SPACE:
			print "on_key_press", (symbol, modifiers)
			return True
		if symbol == key.UP:
			update_projection(win, win.zoom, (win.pan[0], win.pan[1] + win.height / 10.0))
			return True
		if symbol == key.DOWN:
			update_projection(win, win.zoom, (win.pan[0], win.pan[1] - win.height / 10.0))
			return True
		if symbol == key.LEFT:
			update_projection(win, win.zoom, (win.pan[0] - win.width / 10.0, win.pan[1]))
			return True
		if symbol == key.RIGHT:
			update_projection(win, win.zoom, (win.pan[0] + win.width / 10.0, win.pan[1]))
			return True

	def on_mouse_press(x, y, button, modifiers):
		scale = 1.0 + win.zoom / 10.0

		real_x = win.pan[0] + (x - win.width  / 2.0) * scale
		real_y = win.pan[1] + (y - win.height / 2.0) * scale

		ship.move(real_x, real_y)
		# background flash
		flash = flash_task(0.5); flash.next()
		g_tasks.append(flash)
		# sparks test
		task = sparks.draw_task((real_x, real_y, 0.0)); task.next()
		g_tasks.append(task)

	win.zoom = 0
	win.pan = (0.0, 0,0)
	def on_mouse_scroll(x, y, scroll_x, scroll_y):
		update_projection(win, win.zoom + (-scroll_y), win.pan)

	win.set_handlers(on_key_press, on_mouse_press, on_mouse_scroll, on_resize)

	ship = player.Ship(g_tasks)
	ship.pos = (0, 0)

	fps_text = font.Text(font.load('Verdana'), y=10)

	#clock.set_fps_limit(3)
	while not win.has_exit:
		win.dispatch_events()
		frame_time = clock.tick()

		win.clear()

		glColor4f(1.0, 1.0, 1.0, 1.0)
		test_texture.blit(*ship.pos)

		for task in g_tasks[:]:
			try: task.send(frame_time)
			except StopIteration: g_tasks.remove(task)

		#fps_text.text = "fps: %d" % clock.get_fps()
		#fps_text.draw()

		win.flip()

if __name__ == "__main__": main()
