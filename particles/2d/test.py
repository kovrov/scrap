from pyglet.gl import *
from pyglet import clock
from pyglet import window
from pyglet.window import key
from pyglet.window import mouse
from pyglet import image

import fx
import player
import view
import ui


g_tasks = []


def main():
	win = window.Window(resizable=True) #vsync=False
	view.window = win
	win.zoom = 0
	win.origin = (0.0, 0,0)

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	test_texture = image.load('test.png').get_texture()

	test_texture.anchor_x = test_texture.width / 2
	test_texture.anchor_y = test_texture.height / 2

	def on_resize(width, height):
		glViewport(0, 0, width, height)
		view.update_projection(win.zoom, win.origin)
		return True

	def on_key_press(symbol, modifiers):
		pass

	def on_mouse_scroll(x, y, scroll_x, scroll_y):
		#view.zoom(-scroll_y)
		view.update_projection(win.zoom - scroll_y, win.origin)

	def on_mouse_press(x, y, button, modifiers):
		if ui.on_mouse_press(x, y, button, modifiers):
			return True
		real_x, real_y = view.screen2world(x, y)
		ship.move(real_x, real_y)
		# background flash
		flash = fx.flash_task(0.5); flash.next()
		g_tasks.append(flash)
		# sparks test
		task = fx.sparks_task((real_x, real_y, 0.0)); task.next()
		g_tasks.append(task)

	win.set_handlers(on_key_press, on_mouse_press, on_mouse_scroll, on_resize)
	keys = key.KeyStateHandler()
	win.push_handlers(keys)

	ship = player.Ship(g_tasks)
	ship.pos = (0, 0)

	def exit():
		win.has_exit = True
	button = ui.Button(exit, (10, 10), "Quit")

	#clock.set_fps_limit(3)
	glClearColor(0.5, 0.5, 0.5, 1.0)
	while not win.has_exit:
		win.dispatch_events()
		frame_time = clock.tick()
		# update game objects state
		ship.key_handler(keys, frame_time)
		# update view
		view.key_handler(keys, frame_time)
		# draw game objects
		win.clear()
		glColor4f(1.0, 1.0, 1.0, 1.0)
		test_texture.blit(*ship.pos)
		# drawing tasks scheduler run
		for task in g_tasks[:]:
			try: task.send(frame_time)
			except StopIteration: g_tasks.remove(task)
		# UI is drawind always ...
		ui.draw(win.width, win.height, frame_time)
		win.flip()


if __name__ == "__main__": main()
