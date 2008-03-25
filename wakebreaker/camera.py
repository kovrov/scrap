import math
from pyglet.gl import *
from util import Vector3

class Camera:
	def __init__(self):
		self.eye       = Vector3(0, 0,-10)  # position
		self.center    = Vector3(0, 0,  0)  # what the camera is looking at
		self.up        = Vector3(0, 1,  0)  # the up vector
		self.direction = Vector3()  # normalized direction vector

	# moves the camera
	def translate(self, trans):
		self.eye += trans

	# fills the eye, center, up vectors for use when the camera updates
	def lookAt(self, pos, center, up):
		self.eye[:] = pos
		self.center[:] = center
		self.up[:] = up
	
	# this is an implementation of the gluLookAt() function
	def update(self):
		#gluLookAt(self.eye.x,    self.eye.y,    self.eye.z,
 		#          self.center.x, self.center.y, self.center.z,
		#          self.up.x,     self.up.y,     self.up.z)

		f = self.center - self.eye
		# normalize it
		f *= 1.0 / math.sqrt(f.x * f.x + f.y * f.y + f.z * f.z)
		# update direction
		self.direction[:] = f
		s = f.cross(self.up)
		u = s.cross(f)
		matrix_gl = (GLfloat*16)(s.x, u.x, -f.x, 0.0,
							s.y, u.y, -f.y, 0,
							s.z, u.z, -f.z, 0, 
							0.0, 0.0,  0.0,  1.0)
		glMultMatrixf(matrix_gl)
		glTranslatef(-self.eye.x, -self.eye.y, -self.eye.z)
