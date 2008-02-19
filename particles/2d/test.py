from pyglet.gl import *
from pyglet import clock
from pyglet import window
from pyglet.window import key
from pyglet.window import mouse
from pyglet import font
from pyglet import image

import sparks

g_tasks = []

def flash_task(seconds):
	k = 1.0 / seconds
	t = 0.0
	while t < seconds:
		t += yield
		glClearColor(1 - k * t, 1 - k * t, 1 - k * t, 1.0)
	glClearColor(0.0, 0.0, 0.0, 1.0)

def main():
	win = window.Window(resizable=True, vsync=False)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	test_texture = image.load('test.png').texture

	def on_key_press(symbol, modifiers):
		if symbol == key.SPACE:
			print "on_key_press", (symbol, modifiers)
			return True
		print "fps_text", fps_text

	def on_mouse_press(x, y, button, modifiers):
		# background flash
		flash = flash_task(0.5); flash.next()
		g_tasks.append(flash)
		# sparks test
		task = sparks.draw_task((x, y, 0.0)); task.next()
		g_tasks.append(task)

	win.set_handlers(on_key_press, on_mouse_press)

	fps_text = font.Text(font.load('Verdana'), y=10)

	#clock.set_fps_limit(30)
	while not win.has_exit:
		win.dispatch_events()
		frame_time = clock.tick()

		win.clear()

		glColor4f(1.0, 1.0, 1.0, 1.0)
		test_texture.blit((win.width - test_texture.width) / 2, (win.height - test_texture.height) / 2)

		for task in g_tasks[:]:
			try: task.send(frame_time)
			except StopIteration: g_tasks.remove(task)

		fps_text.text = "fps: %d" % clock.get_fps()
		fps_text.draw()

		win.flip()

if __name__ == "__main__": main()
