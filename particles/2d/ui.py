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

from pyglet.gl import *
from pyglet.image import create, SolidColorImagePattern
from pyglet import font

ft = font.load('Arial')
text = font.Text(ft, 'Hello, World!')
image = create(128, 32, SolidColorImagePattern((0x00, 0x00, 0x00, 0x7F)))
texture = image.get_texture()

def draw(w, h):
	# init
	glPushAttrib(GL_TRANSFORM_BIT)  # GL_MATRIX_MODE
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(0, w, 0, h, -1, 1)
	glMatrixMode(GL_MODELVIEW);
	glPushMatrix()
	glLoadIdentity()

	# draw
	glColor4f(1.0, 1.0, 1.0, 1.0)
	texture.blit(w // 2.0 - 4, h // 2.0 - 4)
	text.x = w // 2.0
	text.y = h // 2.0
	text.draw()

	# cleanup
	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glPopAttrib()

