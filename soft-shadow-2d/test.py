import math
import pyglet
from pyglet.gl import *

def iter_current_next(iterable):
    it = iter(iterable)
    first = current = it.next()
    for next in it:
        yield current, next
        current = next
    yield current, first


class Point:
	def __init__(self, x=0., y=0.):
		self.x = x
		self.y = y
	def __imul__(self, val):
		self.x *= val; self.y *= val; return self
	def __mul__(self, val):
		return Point(self.x * val, self.y * val)
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	def cross(self, other):  # cross product
		return self.x * other.y - self.y * other.x
	def dot(self, other):  # dot product
		return self.x * other.x + self.y * other.y
	def normalise(self):
		length = self.length()
		if length != 0.:
			self *= (1. / length)
		return self
	def normaliseCopy(self):
		return Point(self.x, self.y).normalise()
	def length(self):  # length of vector
		return math.sqrt(self.x * self.x + self.y * self.y)
	def angle(self, other):  # angle to other vector
		return math.atan2(self.cross(other), self.dot(other))  # angle between segments
	def __iter__(self):
		return iter((self.x, self.y))


class ConvexPolygon:
	# constructs from a vertex list, vertices must be in ccw order
	def __init__(self, verts):
		# edges, in ccw order
		self.edges = []
		assert len(verts) > 3, "Polygon needs at least 3 vertices"
		for i in xrange(1, len(verts)):
			self.edges.append(Edge(verts[i-1], verts[i]))
		self.edges.append(Edge(verts[-1], verts[0]))
		assert self.isValid()

	# Finds the edges that face away from a given location 'point'.
	# Returns a list of indices into 'edges'. In ccw order.
	def getBackfacingEdgeIndices(self, point):
		assert self.isValid()
		result = []
		# find the indices of the two edges that face away from 'point' and that
		# have one adjacent edge facing towards 'point'
		firstbackfacing = lastbackfacing = None
		prev_edge_front = cur_edge_front = False
		for i, edge in enumerate(self.edges):
			direction = point - edge.src
			if direction.dot(edge.normal()) < 0:
				cur_edge_front = True
			else:
				cur_edge_front = False
			if i != 0:
				if cur_edge_front and not prev_edge_front:
					firstbackfacing = i
				elif not cur_edge_front and prev_edge_front:
					lastbackfacing = i - 1
			prev_edge_front = cur_edge_front
		# if no change between front and backfacing vertices was found,
		# we are inside the polygon, consequently all edges face backwards
		if firstbackfacing is None and lastbackfacing is None:
			for i in xrange(len(self.edges)):
				result.append(i)
			return result
		# else, if one one of the changes was found, we missed the one at 0
		elif firstbackfacing is None:
			firstbackfacing = 0
		elif lastbackfacing is None:
			lastbackfacing = len(self.edges) - 1
		# if this is true, we can just put the indices in result in order
		if firstbackfacing <= lastbackfacing:
			for i in xrange(firstbackfacing, lastbackfacing+1):
				result.append(i)
		else:  # we must go from first to $ and from 0 to last
			for i in xrange(firstbackfacing, len(self.edges)):
				result.append(i)
			for i in xrange(lastbackfacing+1):
				result.append(i)
		return result

	# returns true if the edges list makes up a convex polygon and are in ccw order
	def isValid(self):
		current = self.edges[-1]
		for next in self.edges:
			if current.dst is not next.src:
				return False
			if current.tangent().cross(next.tangent()) < 1.:
				return False
			current = next
		return True


class Edge:
	def __init__(self, src, dst):
		self.src = src #TODO: value
		self.dst = dst #TODO: value
	def normal(self):
		p = self.dst - self.src
		return Point(p.y, -p.x)
	def tangent(self):
		return self.dst - self.src


class Light:
	texture = pyglet.resource.image("light.png").get_texture()

	def __init__(self, pos, color=(1.,1.,1.), outerradius=128., sourceradius=5.):
		self.position = pos #TODO: value
		self.color = tuple(color)
		self.outerradius = outerradius
		self.sourceradius = sourceradius

	def drawSource(self):
		segments = 20
		increment = math.pi * 2 / segments
		radius = self.sourceradius
		x, y = self.position
		glBegin(GL_TRIANGLE_FAN)
		glColor3f(*self.color)
		glVertex2f(x, y)
		for i in xrange(segments + 1):
			glVertex2f(radius*math.cos(i*increment)+x, radius*math.sin(i*increment)+y)
		glEnd()

	def drawLight(self):
		glBindTexture(self.texture.target, self.texture.id) #GL_TEXTURE_2D
		glColor3f(*self.color)
		x, y = self.position.x - self.outerradius, self.position.y - self.outerradius
		width = height = self.outerradius * 2
		self.texture.blit(x, y, 0, width, height)


class LightBlocker:
	def __init__(self, pos, shape):
		self.position = pos #TODO: value
		self.shape = shape

	# returns a sequence of vertices that form a line, indicating
	# where light is blocked
	def getBlockedLine(self, src):
		edgeIndices = self.shape.getBackfacingEdgeIndices(src - self.position)
		ret = [] 
		ret.append(self.position + self.shape.edges[edgeIndices[0]].src)
		for ind in edgeIndices:
			ret.append(self.position + self.shape.edges[ind].dst)
		return ret

	def draw(self):
		glColor3f(1.,0.,0.)
		glBegin(GL_TRIANGLE_FAN)
		for edge in self.shape.edges:
			glVertex2f(self.position.x + edge.src.x, self.position.y + edge.src.y)
			glVertex2f(self.position.x + edge.dst.x, self.position.y + edge.dst.y)
		glEnd()


light = Light(Point(0, 0), (1.,1.,1.), 200, 10)
lightBlockers = [
	# small box
	LightBlocker(Point(225, 220),
		ConvexPolygon([
			Point(-10, -10),
			Point( 10, -10),
			Point( 10,  10),
			Point(-10,  10)])),
	# rectangle that's much longer than wide
	LightBlocker(Point(150, 100),
		ConvexPolygon([
			Point(-120,-10),
			Point( 300,-10),
			Point( 300, 10),
			Point(-120, 10)])),
	# diagonal line
	LightBlocker(Point(300, 300),
		ConvexPolygon([
			Point( 80, -80),
			Point(100, -70),
			Point(-70, 100),
			Point(-80,  80)])),
	# some polygon
	LightBlocker(Point(450, 360),
		ConvexPolygon([
			Point(-20, -20),
			Point(  0, -30),
			Point( 20, -20),
			Point( 20,   0),
			Point(  0,  20),
			Point(-15,  10)]))]

win = pyglet.window.Window(resizable=True)

@win.event
def on_mouse_motion(x, y, dx, dy):
	light.position.x = x
	light.position.y = y

@win.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	for blocker in lightBlockers:
		blocker.draw()
		# blocked lines
		blockerLine = blocker.getBlockedLine(light.position)
		glColor3f(1.,1.,1.)
		glBegin(GL_LINE_STRIP)
		for point in blockerLine:
			glVertex2f(*point)
		glEnd()

pyglet.app.run()
