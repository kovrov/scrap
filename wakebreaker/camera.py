import math
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
		self.eye.set(pos)
		self.center.set(center)
		self.up.set(up)
	
	# this is an implementation of the gluLookAt() function
	def update(self):
		gluLookAt(self.eye.x,    self.eye.y,    self.eye.z,
 		          self.center.x, self.center.y, self.center.z,
		          self.up.x,     self.up.y,     self.up.z)
