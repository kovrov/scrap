"""
http://www.gamedev.net/reference/programming/features/2dsoftshadow/
http://www.incasoftware.de/~kamm/projects/index.php/2007/09/08/soft-shadows-2d/
"""

import pyglet
from pyglet.gl import *


# convenience function to convert points to OpenGL vertices
def makeVertex(p):
	glVertex2f(p.x, p.y)

# oriented edge, normal is 'to the right'
class Edge:
	def __init__(self):
		self.src = Point()
		self.dst = Point()
	def normal(self):
		def rotate90cw(p):
			return Point(p.y, -p.x)
		return rotate90cw(self.dst - self.src)
	def tangent(self):
		return self.dst - self.src


# holds the vertices of a convex polygon
class ConvexPolygon:
	# constructs from a vertex list, vertices must be in ccw order
	def __init__(self, verts=None):
		# edges, in ccw order
		self.edges = []
		if not verts:
			return
		assert verts.length > 3, "Polygon needs at least 3 vertices"
		for i in xrange(1, verts.length):
			self.edges.append(Edge(verts[i-1], verts[i]))
		self.edges.append(Edge(verts[$-1], verts[0])
		assert self.isValid()
	
	"""	Finds the edges that face away from a given location 'src'.
		Returns a list of indices into 'edges'. In ccw order.
	"""
	def getBackfacingEdgeIndices(self, src):
		assert self.isValid()
		
		result = []
		
		# find the indices of the two edges that face away from 'src' and that
		# have one adjacent edge facing towards 'src'
		size_t firstbackfacing = size_t.max, lastbackfacing = size_t.max;
		
		{			
			prev_edge_front = cur_edge_front = False
			for i, edge in edges:
				if edge.normal.dot(src - edge.src) < 0:
					cur_edge_front = true
				else
					cur_edge_front = false
				if i != 0:
					if cur_edge_front and not prev_edge_front:
						firstbackfacing = i
					elif not cur_edge_front and prev_edge_front:
						lastbackfacing = i-1
				prev_edge_front = cur_edge_front
		}
		# if no change between front and backfacing vertices was found,
		# we are inside the polygon, consequently all edges face backwards
		if firstbackfacing == size_t.max and lastbackfacing == size_t.max:
			for i in xrange(edges.length):
				result ~= i
			return result
		# else, if one one of the changes was found, we missed the one at 0
		elif firstbackfacing == size_t.max:
			firstbackfacing = 0
		elif lastbackfacing == size_t.max:
			lastbackfacing = edges.length - 1
		if firstbackfacing <= lastbackfacing: # we can just put the indices in result in order
			for i in xrange(firstbackfacing, lastbackfacing+1):
				result ~= i
		else: # we must go from first to $ and from 0 to last
			for i in xrange(firstbackfacing, edges.length):
				result ~= i
			for i in xrange(lastbackfacing+1):
				result ~= i
		return result
	# returns true if the edges list makes up a convex polygon and are in ccw order
	def isValid(self):
		for i in xrange(self.edges.length):
			nexti = i+1 < self.edges.length ? i+1 : 0
			if edges[i].dst != self.edges[nexti].src:
				return False
			if self.edges[i].tangent().cross(self.edges[nexti].tangent()) <= 0:
				return False
		return True


class Light:  # a light source
	texture = Texture()
	def __init__(self):
		self.position = Point()
		self.color = Color.White
		self.outerradius = 128
		self.sourceradius = 5
	def draw(self):
		glDisable(GL_TEXTURE_2D)
		Color.Yellow.setGLColor()
		glBegin(GL_TRIANGLE_FAN)
		makeVertex(self.position)
		segments = 20
		for i in xrange(segments + 1):
			makeVertex(self.position + Point.fromPolar(self.sourceradius, 2*PI*i / segments))
		glEnd()


win = pyglet.window.Window(resizable=True, vsync=True)

lights = [
	# this first light will move with the mouse cursor
	Light(Point(0,0), Color.White, 200, 10),
	# stationary lights
	Light(Point(350,330), Color.Green),
	Light(Point(270,260), Color.Blue),
	Light(Point(200,400), Color.Yellow, 200),
	Light(Point(500, 50), Color.Red),
	Light(Point(450, 50), Color.Green),
	Light(Point(475, 75), Color.Blue)]

lightBlockers = [
	# small box
	LightBlocker(Point(225,220), 
		ConvexPolygon.fromVertices([
			Point(-10,-10),
			Point( 10,-10),
			Point( 10, 10),
			Point(-10, 10)])),
	# some polygon
	LightBlocker(Point(450,360), 
		ConvexPolygon.fromVertices([
			Point(-20,-20),
			Point(  0,-30),
			Point( 20,-20),
			Point( 20,  0),
			Point( 0,  20),
			Point(-15, 10)])),
	# rectangle that's much longer than wide
	LightBlocker(Point(150,100), 
		ConvexPolygon.fromVertices([
			Point(-120,-10),
			Point( 300,-10),
			Point( 300, 10),
			Point(-120, 10)])),
	# diagonal line
	LightBlocker(Point(300,300), 
		ConvexPolygon.fromVertices([
			Point( 80,-80),
			Point(100,-70),
			Point(-70,100),
			Point(-80,80)]))]


@win.event
def on_draw():
	""" accumulate lighting in a texture """
	glClearColor(0., 0., 0., 0.)
	glViewport(0, 0, rendertexsize, rendertexsize)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	for light in lights:
		# clear alpha to full visibility
		glColorMask(false, false, false, true)
		glClear(GL_COLOR_BUFFER_BIT)
		# write shadow volumes to alpha
		glBlendFunc(GL_ONE, GL_ONE)
		glDisable(GL_TEXTURE_2D)
		glColor4f(0., 0., 0., 1.)
		for blocker in lightBlockers:
			renderShadow(light, blocker)
		# draw light
		glColorMask(True, True, True, False)
		glBlendFunc(GL_ONE_MINUS_DST_ALPHA, GL_ONE)
		drawImage(light.texture, light.position, Size(2*light.outerradius, 2*light.outerradius), Point(0,0), 0, light.color)
	""" copy lighting into texture """
	glBindTexture(GL_TEXTURE_2D, rendertex)
	glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8, 0, 0, rendertexsize, rendertexsize, 0)
	""" render regular scene """
	glViewport(0, 0, 640, 480)
	glClearColor(1., 1., 1., 0.)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	for blocker in lightBlockers:
		blocker.draw()
	""" apply lighting by rending light texture on top """
	glBlendFunc(GL_DST_COLOR, GL_ZERO)
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, rendertex)  
	Color.White.setGLColor()
	glBegin(GL_QUADS)
	glTexCoord2d(0., 1.); glVertex2f(0,   0) 
	glTexCoord2d(0., 0.); glVertex2f(0,   480)
	glTexCoord2d(1., 0.); glVertex2f(640, 480)
	glTexCoord2d(1., 1.); glVertex2f(640, 0)     
	glEnd()
	""" render lights on top, so they're clearly visible """
	glBlendFunc(GL_ONE, GL_ZERO)
	for light in lights:
		light.draw()
	""" swap and limit framerate """
	arc.window.swap()		
	arc.time.limitFPS(40)


@win.event
def on_mouse_motion(x, y, dx, dy):
	print "on_mouse_motion"

pyglet.app.run()
