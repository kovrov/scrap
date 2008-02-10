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

if __name__ == "__main__":
	vect = (0.0, 0.0, 1.0)
	print "vect", vect
	print " 45", rotateVectorY(vect, 45.0)
	print " 90", rotateVectorY(vect, 90.0)
	print "135", rotateVectorY(vect, 135.0)
	print "225", rotateVectorY(vect, 225.0)
	print "270", rotateVectorY(vect, 270.0)
	print "315", rotateVectorY(vect, 315.0)

