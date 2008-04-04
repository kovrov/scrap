import pyglet
from pyglet.gl import *
from menu import Menu
from game import Game
import view

menu = Menu()
game = Game()
fps_display = pyglet.clock.ClockDisplay()

window = pyglet.window.Window(vsync=False)

ortho_matrix = persp_matrix = None

@window.event
def on_resize(width, height):
	global ortho_matrix, persp_matrix
	glViewport(0, 0, width, height)
	persp_matrix = view.get_persp_matrix(60, width / float(height), 1, 256)
	ortho_matrix = view.get_ortho_matrix(0, width, 0, height, -1, 1)
	return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadMatrixf(persp_matrix)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	#scene.draw()
	glMatrixMode(GL_PROJECTION)
	glLoadMatrixf(ortho_matrix)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	fps_display.draw()

def set_menu_state():
	unschedule(game.update)
	schedule_interval_soft(menu.update)
	schedule_interval_soft(game.update)

def set_game_state():
	unschedule(menu.update)
	schedule(game.update)

pyglet.app.run()
