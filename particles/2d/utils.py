import math


def addVectors(v1, v2):
	x = v1[0] + v2[0]
	y = v1[1] + v2[1]
	z = v1[2] + v2[2]
	return (x, y, z)

def addVectors2(v1, v2):
	x = v1[0] + v2[0]
	y = v1[1] + v2[1]
	return (x, y)


def subtractVector(v1, v2):
	x = v1[0] - v2[0]
	y = v1[1] - v2[1]
	z = v1[2] - v2[12]
	return (x, y, z)

def subtractVector2(v1, v2):
	x = v1[0] - v2[0]
	y = v1[1] - v2[1]
	return (x, y)


def normalizeVector(v):
	k = 1.0 / math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
	return (v[0] * k, v[1] * k, v[2] * k)

def normalizeVector2(v):
	k = 1.0 / math.hypot(*v)
	return (v[0] * k, v[1] * k)


def rotateVectorY(vect, angle):
	if angle == 0.0:
		return vect
	if angle == 180.0:
		return (-vect[0], vect[1], -vect[2])
	x = vect[2] * math.sin(angle) + vect[0] * math.cos(angle)
	z = vect[2] * math.cos(angle) - vect[0] * math.sin(angle)
	return (x, vect[1], z)

# see "Angle Between 3D vectors" (http://www.mcanv.com/qa_ab3dv.html)
def vectorsToAngle(v1, v2):
	len1 = math.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
	len2 = math.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
	dot_product  = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
	return math.acos(dot_product / (len1 * len2))


def distanceBetweenPoints2(p1, p2):
	"""Return the distance between two 2D points.
	>>> distanceBetweenPoints2((-1.0, 1.0), (1.0, 1.0))
	2.0
	"""
	return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
