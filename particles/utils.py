import math

def addVectors(v1, v2):
	x = v1[0] + v2[0]
	y = v1[1] + v2[1]
	z = v1[2] + v2[2]
	return (x, y, z)

def normalizeVector(v):
	k = 1.0 / math.sqrt(v[0]**2.0 + v[1]**2.0 + v[2]**2.0)
	return (v[0] * k, v[1] * k, v[2] * k)

def rotateVector(vect, angle):
	angle = math.radians(angle)
	z = vect[2] * math.cos(angle) - vect[0] * math.sin(angle)
	x = vect[2] * math.sin(angle) + vect[0] * math.cos(angle)
	return(x, vect[1], z)
