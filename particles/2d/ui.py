"""
main menu
opions menu
hud
dialog windows

slider
button
text input
drop list
check box
"""

main_menu = ['play', 'help', 'opions', 'exit']

import pyglet
from pyglet.gl import *
from pyglet.image import create, SolidColorImagePattern

image = create(128, 32, SolidColorImagePattern((0x00, 0x00, 0x00, 0x7F)))
texture = image.get_texture()

theme = {'text_color':       (0x00, 0xFF, 0xFF, 0xFF),
         'border_width':      2,
         'border_color':     (0.0, 1.0, 1.0, 0.2),
         'background_color': (0.0, 0.0, 0.0, 0.6)}

g_tasks = []

visible_objects = []

def on_mouse_press(x, y, button, modifiers):
	for o in visible_objects:
		if o.hitTest((x, y)):
			return o.press(button, modifiers)

def append(task):
	task.next()  # init
	g_tasks.append(task)

def draw(w, h, frame_time=0):
	# init
	glPushAttrib(GL_DEPTH_BUFFER_BIT|GL_TRANSFORM_BIT)  # GL_DEPTH_TEST, GL_MATRIX_MODE
	glDisable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(0, w, 0, h, -1, 1)
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()

	for task in g_tasks[:]:
		try: task.send(frame_time)
		except StopIteration: g_tasks.remove(task)

	# cleanup
	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glPopAttrib()


class Button:
	def __init__(self, callback, pos, text, size=None, anchor=(0,0)):
		self.callback = callback
		self.pos = pos
		self.text = pyglet.text.Label(text, valign='bottom',
		                              font_name='Verdana', font_size=14,
		                              color=theme['text_color'])
		self.size = size
		self.anchor = anchor
		self.task = self.draw()
		self.padding = 2
		append(self.task)
		visible_objects.append(self)

	def __del__(self):
		if self.task:
			self.task.close()
	
	def hitTest(self, point):
		border = theme['border_width']
		x, y = self.pos[0], self.pos[1]
		w = self.text.content_width  + self.padding * 2 + border * 2
		h = self.text.content_height + self.padding * 2 + border * 2
		if x < point[0] and point[0] < x + w and y < point[1] and point[1] < y + h:
			return True
	def press(self, button, modifiers):
		self.callback()
		return True

	def draw(self):
		while True:
			yield
			border = theme['border_width']
			glDisable(GL_TEXTURE_2D)
			x, y = self.pos[0], self.pos[1]
			w = self.text.content_width  + self.padding * 2 + border * 2
			h = self.text.content_height + self.padding * 2 + border * 2
			# back
			glColor4f(*theme['background_color'])
			glBegin(GL_QUADS)
			glVertex2d(x + border / 2.0,     y + border / 2.0)
			glVertex2d(x - border / 2.0 + w, y + border / 2.0)
			glVertex2d(x - border / 2.0 + w, y - border / 2.0 + h)
			glVertex2d(x + border / 2.0,     y - border / 2.0 + h)
			glEnd()
			# border
			glColor4f(*theme['border_color'])
			glLineWidth(border)
			glBegin(GL_LINE_LOOP)
			#glBegin(GL_POLYGON)
			glVertex2d(x,     y)
			glVertex2d(x + w, y)
			glVertex2d(x + w, y + h)
			glVertex2d(x,     y + h)
			glEnd()
			# contents
			self.text.x = x + self.padding + border
			self.text.y = y + self.padding + border
			self.text.draw()
