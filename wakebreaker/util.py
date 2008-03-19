
# basic 3d vector class
class Vector3(object):
	__slots__ = ('__v',)

	def __get_x(self): return self.__v[0]
	def __set_x(self, x): self.__v[0] = float(x)
	x = property(__get_x, __set_x)

	def __get_y(self): return self.__v[1]
	def __set_y(self, y): self.__v[1] = float(y)
	y = property(__get_y, __set_y)

	def __get_z(self): return self.__v[2]
	def __set_z(self, z): self.__v[2] = float(z)
	z = property(__get_z, __set_z)

	def __iter__(self):
		return iter(self.__v)

	def __getitem__(self, index):
		return self.__v[index]

	def __init__(self, *args):
		if len(args) == 3:
			self.__v = map(float, args)
		elif not args:
			self.__v = [0.0, 0.0, 0.0]
		elif len(args) == 1:
			self.__v = map(float, args[0][:3])
		else:
			raise ValueError("wrong arguments")

	#---------------------------------------------------------------
	def set(self, *args):  # operator =
		if len(args) == 3:
			x, y, z = args
			v = self.__v
			v[0] = float(x)
			v[1] = float(y)
			v[2] = float(z)
		else:  # len(args) == 1:
			self.__v = args[0][:]
		return self

	#--------------------------------------------------------
	def __add__(self, other):  # operator +=
		"""
		>>> Vector3(1, 2, 3) + Vector3(-4, 5, 6) + (7, 8, -9)
		Vector3(4.0, 15.0, 0.0)
		"""
		x, y, z = self.__v
		ox, oy, oz = other
		v = self.__new__(self.__class__, object)
		v.__v = [x + ox, y + oy, z + oz]
		return v

	#--------------------------------------------------------
	def __iadd__(self, other):  # operator +=
		x, y, z = other
		v = self.__v
		v[0] += x
		v[1] += y
		v[2] += z
		return self

	#--------------------------------------------------------
	def __isub__(self, other):  # operator -=
		x, y, z = other
		v = self.__v
		v[0] -= x
		v[1] -= y
		v[2] -= z
		return self

	#---------------------------------------------------------------
	def __imul__(self, other):  # operator *=
		v = self.__v
		if hasattr(other, "__getitem__"):
			x, y, z = other
			v[0] *= x
			v[1] *= y
			v[2] *= z
		else:  # if hasattr(other, "__float__"):
			v[0] *= other
			v[1] *= other
			v[2] *= other
		return self

	#------------------------------------------------------
	def __idiv__(self, other):  # operator /=
		v = self.__v
		if hasattr(other, "__getitem__"):
			x, y, z = other
			v[0] /= ox
			v[1] /= oy
			v[2] /= oz
		else:  # if hasattr(other, "__float__"):
			v[0] /= other
			v[1] /= other
			v[2] /= other
		return self

	#------------------------------------------------------
	def __sub__(self, other):  # operator -
		x, y, z = self.__v
		ox, oy, oz = other
		v = self.__new__(self.__class__, object)
		v.__v = [x - ox, y - oy, z - oz]
		return v

	#------------------------------------------------------
	def __mul__(self, other):  # operator *
		"""
		>>> Vector3(1,2,3) * [1, 2.5, 3] * 2
		Vector3(2.0, 10.0, 18.0)
		"""
		x, y, z = self.__v
		v = self.__new__(self.__class__, object)
		if hasattr(other, "__getitem__"):
			ox, oy, oz = other
			v.__v = [x * ox, y * oy, z * oz]
		else:  # if hasattr(other, "__float__"):
			v.__v = [x * other, y * other, z * other]
		return v

	#------------------------------------------------------
	def cross(self, other):  # Cross product
		x, y, z = self.__v
		bx, by, bz = other
		v = self.__new__(self.__class__, object)
		v.__v = [y*bz - by*z, z*bx - bz*x, x*by - bx*y]
		return v

	#------------------------------------------------------
	def copy(self):
		v = self.__new__(self.__class__, object)
		v.__v = self.__v[:]
		return v

	#------------------------------------------------------
	def __repr__(self):
		return "Vector3(%s, %s, %s)" % tuple(self.__v)



if __name__ == '__main__':
	import doctest
	doctest.testmod()
