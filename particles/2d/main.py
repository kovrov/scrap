import pyglet
from pyglet.gl import *

import view
import ui
import controller as ctl

win = pyglet.window.Window(resizable=True, vsync=False)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

test_texture = pyglet.resource.image('test.png').get_texture()

test_texture.anchor_x = test_texture.width / 2
test_texture.anchor_y = test_texture.height / 2

@win.event
def on_resize(width, height):
	glViewport(0, 0, width, height)
	view.resize(width, height)
	return True

@win.event
def on_draw():
	win.clear()
	# draw game objects
	win.clear()
	glColor4f(1.0, 1.0, 1.0, 1.0)
	test_texture.blit(*ship.pos)
	# UI is drawind always ...
	frame_time = 0
	ui.draw(win.width, win.height, frame_time)

win.set_handlers(ctl.on_key_press, ctl.on_mouse_press, ctl.on_mouse_scroll)
win.push_handlers(ctl.key_state)

def exit():
	pyglet.app.event_loop.exit()
button = ui.Button(exit, (10, 10), "Quit")
glClearColor(0.5, 0.5, 0.5, 1.0)

#pyglet.clock.set_fps_limit(3)
pyglet.app.run()
