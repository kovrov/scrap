import math
"""
7
6
5    .[2,5]  *[6,5]
4
3
2    *[2,2]  .[6,2]
1    
0    
 0 1 2 3 4 5 6 7
0    
1    
2    *[2,2]  .[6,2]
3
4
5    .[2,5]  *[6,5]
6
7

cos = a / c
 a = cos * c
sin = b / c
 b = sin * c

"""

def multmat2(A,B):
    "A*B"
    if len(A) != len(B): raise Exception("error")  # this check is not enough!
    n = range(len(A))
    C = []
    for i in n:
        C.append([0]*len(A))  # add a row to C
        for j in n:
            a = A[i]    # get row i from A
            b = [row[j] for row in B] # get col j from B
            C[i][j] = sum([x*y for x,y in zip(a,b)])
    return C

def unit_vector(src, dst, unit=1):
	"""returns "normalized vector" directed from src to dst"""
	x, y = dst[0] - src[0], dst[1] - src[1]
	#x, y = dst[0] - src[0], src[1] - dst[1]
	#vlen = math.sqrt(x**2 + y**2)
	ang = math.atan2(y, x)
	return (math.cos(ang) * unit, math.sin(ang) * unit)

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

print "\n"
print unit_vector((2,2), (5,6))
print unit_vector((1,0), (-2,-4))
print "\n"
print unit_vector((2,2), (6,5))
print unit_vector((6,5), (2,2))
