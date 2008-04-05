import math
from pyglet.gl import *

MATRIX4F = GLfloat*16

def get_persp_matrix(fov, aspect, near, far):
	"""
	perspective projection matrix
	"""
	f = 1. / math.tan(math.radians(fov) / 2.)
	q = (far + near) / (near - far)
	qq = (2. * far * near) / (near - far)
	return MATRIX4F(f / aspect,	0.,   0.,   0.,
	                0.,         f,    0.,   0.,
	                0.,         0.,	  q,   -1.,
	                0.,         0.,   qq,   0.)

def get_ortho_matrix(left, right, bottom, top, near, far):
	"""
	orthographic projection matrix
	"""
	x = 2. / (right - left)
	y = 2. / (top - bottom)
	z = -2. / (far - near)
	tx = -(right + left) / (right - left)
	ty = -(top + bottom) / (top - bottom)
	tz = -(far + near) / (far - near)
	return MATRIX4F(x,   0.,  0.,  0.,
	                0.,  y,   0.,  0.,
	                0 ,  0.,  z,   0.,
	                tx,  ty,  tz,  1.)
