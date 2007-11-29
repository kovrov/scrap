import math
"""
angle = math.atan2(self.plane.rect.centery - gun[1], self.plane.rect.centerx - gun[0])
self.fpdy = self.speed * math.sin(angle)
self.fpdx = self.speed * math.cos(angle)


 0 1 2 3 4 5 6 7 8
0    
1    
2    .[2,2]  .[6,2]
3
4
5    .[2,5]  *[6,5]

src = [2, 2]
dst = [2, 5] # right
dst = [2, 5] # down
dst = [2, 5] # up

math.degrees(math.atan2(dst[1] - src[1], dst[0] - src[0])) # angle
math.cos(math.atan2(dst[1] - src[1], dst[0] - src[0])) * speed # x
math.sin(math.atan2(dst[1] - src[1], dst[0] - src[0])) * speed # y



math.degrees(math.atan2(1, 1)) # a 45
math.degrees(math.atan2(1, 0)) # a 90
math.degrees(math.atan2(0, 1)) # a 0
math.cos(math.atan2(1, 1)) # x 45
math.cos(math.atan2(1, 0)) # x 90
math.cos(math.atan2(0, 1)) # x 0

3 = 6 / 2
cos = a / c
 a = cos * c
sin = b / c
 b = sin * c

"""
def test(a,b, name):
	c = math.sqrt(a**2 + b**2)
	ang = math.atan2(b, a)
	deg = math.degrees(ang)
	sin = math.sin(ang)
	cos = math.cos(ang)
	tan = math.tan(ang)
	if 0.0 == sin: cot = 0
	else: cot = cos/sin
	print "\n"
	print name
	print "a", a
	print "b", b
	print "c", c
	print "angle", ang, "degrees", deg
	print "sin", sin
	print "cos", cos
	print "tan", tan
	print "cot", cot
	if a != 0.0: print "b/a", b/a, "(tan)", tan
	if c != 0.0: print "b/c", b/c, "(sin)", sin
	if b != 0.0: print "a/b", a/b, "(cot?)", cot
	if c != 0.0: print "a/c", a/c, "(cos)", cos
	if a != 0.0: print "c/a", c/a, "(?)"
	if b != 0.0: print "c/b", c/b, "(?)"

test(5.0, 0.0, "right")
test(5.0, 5.0, "45")
test(0.0, 5.0, "up")
test(3.0, 4.0, "3/4")
test(4.0, 3.0, "3/4")
