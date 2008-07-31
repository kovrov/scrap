import pyglet
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)
image = pyglet.resource.image('test.png')

pos = 0, 0

@window.event
def on_mouse_motion(x, y, dx, dy):
	global pos
	pos = x, y

@window.event
def on_draw():
	window.clear()

	glEnable(GL_TEXTURE_2D) # this is important
	glBegin(GL_POINTS) # or GL_whatever
	glEnd()
#	glDisable(GL_TEXTURE_2D)

	#image.blit(*pos)
	x, y = pos
	z=0
	t = image.tex_coords
	x2 = x + image.width
	y2 = y + image.height
	array = (GLfloat * 32)(
		 t[0],  t[1],  t[2],  1.,
		 x,     y,     z,     1.,
		 t[3],  t[4],  t[5],  1., 
		 x2,    y,     z,     1.,
		 t[6],  t[7],  t[8],  1., 
		 x2,    y2,    z,     1.,
		 t[9],  t[10], t[11], 1., 
		 x,     y2,    z,     1.)

	glPushAttrib(GL_ENABLE_BIT)
	glEnable(image.target)
	glBindTexture(image.target, image.id)
	glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
	glInterleavedArrays(GL_T4F_V4F, 0, array)
	glDrawArrays(GL_QUADS, 0, 4)
	glPopClientAttrib()
	glPopAttrib()

pyglet.app.run()
