import ctypes
from pyglet.gl import *


class POINT3(ctypes.Structure):
	_fields_ = [("x", GLfloat), ("y", GLfloat), ("z", GLfloat)]


# basic 3d vector class
class Vector3(ctypes.Union):
	"""
	Vector3 exposes data via 'x', 'y', 'z' and 'vect' properties.
	>>> v = Vector3()
	>>> v.x = 1.5
	>>> v.y = -2
	>>> v.vect[:]
	[1.5, -2.0, 0.0]
	"""
	_fields_ = [("__pos", POINT3), ("vect", GLfloat*3)]
	_anonymous_ = ("__pos",)

	def __init__(self, *args):
		"""
		Could be initialized with list of values or any iteratable (incuding
		another Vector3 instances):
		>>> Vector3(1, 2, 3)
		Vector3(1.0, 2.0, 3.0)
		>>> Vector3([1, 2, 3])
		Vector3(1.0, 2.0, 3.0)
		>>> Vector3(Vector3(1, 2, 3))
		Vector3(1.0, 2.0, 3.0)
		"""
		if len(args) == 1:
			self.vect = tuple(args[0])
		else:
			self.vect = args

	def __iter__(self):
		return iter(self.vect)

	def set(self, *args):  # operator =
		"""
		>>> v = Vector3()
		>>> v.set(1, 2, 3)
		Vector3(1.0, 2.0, 3.0)
		>>> v.set([4, 5, 6])
		Vector3(4.0, 5.0, 6.0)
		"""
		if len(args) == 1:
			self.vect = tuple(args[0])
		else:
			self.vect = args
		return self

	def __add__(self, other):  # operator +=
		"""
		>>> Vector3(1, 2, 3) + Vector3(-4, 5, 6) + (7, 8, -9)
		Vector3(4.0, 15.0, 0.0)
		"""
		x, y, z = self.vect
		ox, oy, oz = other
		v = self.__new__(self.__class__, object)
		v.vect = x + ox, y + oy, z + oz
		return v

	def __iadd__(self, other):  # operator +=
		"""
		>>> v = Vector3(1, 2, 3)
		>>> v += 4, 5, -6
		>>> v
		Vector3(5.0, 7.0, -3.0)
		"""
		x, y, z = other
		self.x += x
		self.y += y
		self.z += z
		return self

	def __isub__(self, other):  # operator -=
		"""
		>>> v = Vector3(1, 2, 3)
		>>> v -= Vector3(3, 2, 1)
		>>> v
		Vector3(-2.0, 0.0, 2.0)
		"""
		x, y, z = other
		self.x -= x
		self.y -= y
		self.z -= z
		return self

	def __imul__(self, other):  # operator *=
		"""
		>>> v = Vector3(1, 2, 3)
		>>> v *= 2
		>>> print v
		Vector3(2.0, 4.0, 6.0)
		>>> v *= Vector3(-1, -2, -3)
		>>> print v
		Vector3(-2.0, -8.0, -18.0)
		"""
		if hasattr(other, "__iter__"):
			x, y, z = other
		else:  # if hasattr(other, "__float__"):
			x = y = z = other
		self.x *= x
		self.y *= y
		self.z *= z
		return self

	#---
	def __idiv__(self, other):  # operator /=
		v = self.vect
		if hasattr(other, "__iter__"):
			x, y, z = other
			v[0] /= ox
			v[1] /= oy
			v[2] /= oz
		else:  # if hasattr(other, "__float__"):
			v[0] /= other
			v[1] /= other
			v[2] /= other
		return self

	#---
	def __sub__(self, other):  # operator -
		x, y, z = self.vect
		ox, oy, oz = other
		v = self.__new__(self.__class__, object)
		v.vect = x - ox, y - oy, z - oz
		return v

	def __mul__(self, other):  # operator *
		"""
		>>> Vector3(1,2,3) * [1, 2.5, 3] * 2
		Vector3(2.0, 10.0, 18.0)
		"""
		x, y, z = self.vect
		v = self.__new__(self.__class__, object)
		if hasattr(other, "__iter__"):
			ox, oy, oz = other
			v.vect = x * ox, y * oy, z * oz
		else:  # if hasattr(other, "__float__"):
			v.vect = x * other, y * other, z * other
		return v

	#---
	def cross(self, other):  # Cross product
		"""
		Cross product of two vectors:
		>>> v = Vector3(1,2,3)
		>>> v.cross(Vector3(4,5,6))
		Vector3(-3.0, 6.0, -3.0)
		>>> v.cross((4,5,6))
		Vector3(-3.0, 6.0, -3.0)
		>>> v.cross([4,5,6])
		Vector3(-3.0, 6.0, -3.0)
		"""
		x, y, z = self.vect
		bx, by, bz = other
		v = self.__new__(self.__class__, object)
		v.vect = y*bz - by*z, z*bx - bz*x, x*by - bx*y
		#        y*oz - z*oy, x*oz - z*oz, x*oy - y*oz
		return v

	def copy(self):
		"""
		Constructs new object of this class.
		>>> v1 = Vector3(1,2)
		>>> v2 = v1.copy()
		>>> v1.x = 0.75
		>>> v2.y = -1.5
		>>> print v1, v2
		Vector3(0.75, 2.0, 0.0) Vector3(1.0, -1.5, 0.0)
		"""
		v = self.__new__(self.__class__, object)
		v.vect = self.vect  # c_float_Array is "value" type, cool =)
		return v

	def __repr__(self):
		assert type(self.vect) is (GLfloat*3)
		return "Vector3(%s, %s, %s)" % tuple(self.vect)



if __name__ == '__main__':
	#print help(Vector3)
	import doctest
	doctest.testmod()
