import pyglet
from pyglet.gl import *

import view
import scene
import ui
import controller as ctl


win = pyglet.window.Window(resizable=True, vsync=False)

@win.event
def on_resize(width, height):
	glViewport(0, 0, width, height)
	view.resize(width, height)
	return True

@win.event
def on_draw():
	win.clear()
	scene.draw()
	ui.draw(win.width, win.height)

win.set_handlers(ctl.on_key_press, ctl.on_mouse_press, ctl.on_mouse_scroll, ctl.on_key_release)
win.push_handlers(ctl.key_state)

#pyglet.clock.set_fps_limit(3)
pyglet.app.run()
