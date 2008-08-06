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
	def length(self):  # length of vector
		return math.sqrt(self.x * self.x + self.y * self.y)
	def angle(self, other):  # angle to other vector
		return math.atan2(self.cross(other), self.dot(other))  # angle between segments
	def __iter__(self):
		return iter((self.x, self.y))
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __ne__(self, other):
		return self.x != other.x or self.y != other.y

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
		#
		# find the indices of the two edges that face away from 'point' and that
		# have one adjacent edge facing towards 'point'
		first_face_id = last_face_id = None
		prev_edge_front = cur_edge_front = False
		for i, edge in enumerate(self.edges):
			point_dir = point - edge.src  # wtf?
			cur_edge_front = False if point_dir.dot(edge.normal()) < 0 else True
#			print i, "front" if cur_edge_front else ""
			if i != 0:  # not first element?
				if cur_edge_front and not prev_edge_front:
					first_face_id = i
#					print "  first_face_id"
				elif not cur_edge_front and prev_edge_front:
					last_face_id = i
#					print "  last_face_id"
			prev_edge_front = cur_edge_front
#		assert 0
		#
		# if no change between front and backfacing vertices was found,
		# we are inside the polygon, consequently all edges face backwards
		if first_face_id is None and last_face_id is None:
			return xrange(len(self.edges))
		# else, if one one of the changes was found, we missed the one at 0
		if first_face_id is None:
			first_face_id = 0
		if last_face_id is None:
			last_face_id = len(self.edges)
		# if this is true, we can just put the indices in result in order
		if first_face_id < last_face_id:
			return xrange(first_face_id, last_face_id)
		# or we must go from first to $ and from 0 to last
		return range(first_face_id, len(self.edges)) + range(last_face_id)

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
		# debug
		self.labels = []
		for edge in self.shape.edges:
			x, y = self.position + edge.src
			self.labels.append(pyglet.text.Label('%g,%g' % (edge.src.x, edge.src.y), x=x, y=y))

	# returns a sequence of vertices that form a line, indicating where light
	# is blocked
	def getBlockedLine(self, point):
		edgeIndices = self.shape.getBackfacingEdgeIndices(point - self.position)
		ret = [] 
		ret.append(self.position + self.shape.edges[edgeIndices[0]].src)
		for ind in edgeIndices:
			ret.append(self.position + self.shape.edges[ind].dst)
		return ret

	def draw(self):
		glColor3f(1.,0.,0.)
		glBegin(GL_TRIANGLE_FAN)
		for edge in self.shape.edges:
			glVertex2f(*self.position + edge.src)
			glVertex2f(*self.position + edge.dst)
		glEnd()
		# debug
		for label in self.labels:
			label.draw()


light = Light(Point(160, 200), (1.,1.,1.), 200, 4)
blocker = LightBlocker(Point(200, 200),
                       ConvexPolygon([Point(-40,  10),
                                      Point(-20, -20),
                                      Point( 10, -40),
                                      Point( 40, -10),
                                      Point( 20,  20),
                                      Point(-10,  40)]))

win = pyglet.window.Window(resizable=True)

@win.event
def on_mouse_motion(x, y, dx, dy):
	light.position.x = x
	light.position.y = y

@win.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	blocker.draw()
	# blocked lines
	blockerLine = blocker.getBlockedLine(light.position)
	glColor3f(1.,1.,1.)
	glBegin(GL_LINE_STRIP)
	for point in blockerLine:
		glVertex2f(*point)
	glEnd()
	# visalize begin-end of the line
	begin = blockerLine[0]
	end = blockerLine[-1]
	if begin != end:
		glPointSize(4)
		glBegin(GL_POINTS)
		glColor3f(0., 1.0, 0.)
		glVertex2f(*begin)
		glColor3f(0., 0.9, 0.9)
		glVertex2f(*end)
		glEnd()
	light.drawSource()

pyglet.app.run()
