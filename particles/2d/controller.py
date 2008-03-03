from pyglet.window import key

import tasks
import view
import player
import fx

ship = player.Ship()
ship.pos = (0, 0)

key_state = key.KeyStateHandler()

# default key mapping
keys = {'scroll_up':    key.UP,
        'scroll_down':  key.DOWN,
        'scroll_left':  key.LEFT,
        'scroll_right': key.RIGHT,
        'zoom_in':      key.PLUS,
        'zoom_out':     key.MINUS,
        'move_up':      key.E,
        'move_down':    key.D,
        'move_left':    key.S,
        'move_right':   key.F}

def on_key_press(symbol, modifiers):
	if symbol in (keys['move_up'], keys['move_down'], keys['move_left'], keys['move_right']):
		return update_ship_movement()
	if symbol in (keys['scroll_up'], keys['scroll_down'], keys['scroll_left'], keys['scroll_right']):
		return update_view_panning()
	if symbol == keys['zoom_in']:
		return view.zoom(1)
	if symbol == keys['zoom_out']:
		return view.zoom(-1)

def on_key_release(symbol, modifiers):
	if symbol in (keys['move_up'], keys['move_down'], keys['move_left'], keys['move_right']):
		return update_ship_movement()
	if symbol in (keys['scroll_up'], keys['scroll_down'], keys['scroll_left'], keys['scroll_right']):
		return update_view_panning()

def on_mouse_scroll(x, y, scroll_x, scroll_y):
	view.zoom(-scroll_y)

def on_mouse_press(x, y, button, modifiers):
	if ui.on_mouse_press(x, y, button, modifiers):
		return True
	real_x, real_y = view.screen2world(x, y)
	ship.translate(real_x, real_y)
	# background flash
	tasks.append(fx.flash_task(0.5))
	# sparks test
	tasks.append(fx.sparks_task((real_x, real_y, 0.0)))

def update_ship_movement():
	if key_state[keys['view_up']]:    y += 1
	if key_state[keys['view_down']]:  y -= 1
	if key_state[keys['view_left']]:  x -= 1
	if key_state[keys['view_right']]: x += 1
	if x or y:
		ship.move(x, y)

def update_view_panning():
	x = y = 0
	if key_state[keys['scroll_up']]:    y += 1
	if key_state[keys['scroll_down']]:  y -= 1
	if key_state[keys['scroll_left']]:  x -= 1
	if key_state[keys['scroll_right']]: x += 1
	if x or y:
		view.pan(x, y)
