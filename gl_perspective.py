import math
import pyglet
from pyglet.gl import *


def perspective_frustum(fov, aspect, near, far):
	top = math.tan(math.radians(fov) / 2.0) * near
	bottom = -top
	left = bottom * aspect
	right = top * aspect
	glLoadIdentity()
	glFrustum(left, right, bottom, top, near, far)


def perspective_matrix(fov, aspect, near, far):
	f = 1.0 / math.tan(math.radians(fov) / 2.0)
	q = (far + near) / (near - far)
	qq = (2 * far * near) / (near - far)
	m = (GLfloat*16)(f / aspect,	0.0,	 0.0,	 0.0,
					 0.0,			f,		 0.0,	 0.0,
					 0.0,			0.0,	 q,		-1.0,
					 0.0,			0.0,	 qq,	 0.0)
	glLoadMatrixf(m)


if __name__ == '__main__':
	def PRINT_GL_PROJECTION_MATRIX():
		m = (GLfloat*16)()
		glGetFloatv(GL_PROJECTION_MATRIX, m)
		print "PROJECTION_MATRIX:"
		print m[0:4]
		print m[4:8]
		print m[8:12]
		print m[12:16]

	win = pyglet.window.Window()
	@win.event
	def on_resize(width, height):
		fov = 60.0
		near = 1.0
		far = 1024.0
		aspect = float(width) / float(height)
		glMatrixMode(GL_PROJECTION)

		print "gluPerspective"
		glLoadIdentity()
		gluPerspective(fov, aspect, near, far)
		PRINT_GL_PROJECTION_MATRIX()

		print "glFrustum"
		glLoadIdentity()
		perspective_frustum(fov, aspect, near, far)
		PRINT_GL_PROJECTION_MATRIX()

		print "glLoadMatrix"
		glLoadIdentity()
		perspective_matrix(fov, aspect, near, far)
		PRINT_GL_PROJECTION_MATRIX()

		glMatrixMode(GL_MODELVIEW)
		glViewport(0, 0, width, height)
		return pyglet.event.EVENT_HANDLED

	pyglet.app.run()
