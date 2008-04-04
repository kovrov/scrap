import math
from pyglet.gl import *

MATRIX4F = GLfloat*16

def get_persp_matrix(fov, aspect, near, far):
	f = 1.0 / math.tan(math.radians(fov) / 2.0)
	q = (far + near) / (near - far)
	qq = (2 * far * near) / (near - far)
	return MATRIX4F(f / aspect,	0.0,    0.0,    0.0,
	                0.0,        f,      0.0,    0.0,
	                0.0,        0.0,	q,     -1.0,
	                0.0,        0.0,    qq,     0.0)

def get_ortho_matrix(left, right, bottom, top, near, far):
	tx = -(right + left) / (right - left)
	ty = -(top + bottom) / (top - bottom)
	tz = -(far + near) / (far - near)
	return MATRIX4F(2./(right-left), 0,               0,             0,#tx,
	                0,               2./(top-bottom), 0,             0,#ty,
	                0,               0,              -2./(far-near), tz,
	               -1,              -1,               0,             1)
