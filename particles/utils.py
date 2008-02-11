import math

def addVectors(v1, v2):
	x = v1[0] + v2[0]
	y = v1[1] + v2[1]
	z = v1[2] + v2[2]
	return (x, y, z)

def normalizeVector(v):
	k = 1.0 / math.sqrt(v[0]**2.0 + v[1]**2.0 + v[2]**2.0)
	return (v[0] * k, v[1] * k, v[2] * k)

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
