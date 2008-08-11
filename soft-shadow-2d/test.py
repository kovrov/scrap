import math
import pyglet
from pyglet.gl import *

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
	def __repr__(self):
		return "(%g,%g)" % (self.x, self.y)

class ConvexPolygon:
	# constructs from a vertex list, vertices must be in ccw order
	def __init__(self, verts):
		self.vertices = [Point(x,y) for x,y in verts]
		assert self.isValid(), "the points must form edges in ccw order"

	def iter_edges(self):
		"""
		To iterate over edges in form of ("source", "destination") points
		"""
		it = iter(self.vertices)
		first_src = src = it.next()
		for dst in it:
			yield src, dst
			src = dst
		yield src, first_src

	def extreme_vertices_id(self, point):
		"""
		find the left and right extreme vertices relative to given 'point'
		"""
		assert self.isValid()
		right_id = left_id = None
		prev_faced_to_point = None
		for i, (edge_src, edge_dst) in enumerate(self.iter_edges()):
			#
			# determine if current edge is faced towards the point
			point_dir = point - edge_src
			edge_dir = edge_dst - edge_src
			edge_normal = Point(edge_dir.y, -edge_dir.x)
			faced_to_point = False if point_dir.dot(edge_normal) < 0. else True
			#
			# set possible "left" or "right" edge id
			if faced_to_point != prev_faced_to_point:
				if faced_to_point:
					left_id = i
				else:
					right_id = i
			prev_faced_to_point = faced_to_point
		return right_id, left_id

	def back_points_ids(self, point):
		right_id, left_id = self.extreme_vertices_id(point)
		#
		# if the point is inside this polygon, first and last vertices overlaps
		if right_id is None or left_id is None:
			return xrange(-1, len(self.vertices))
		#
		# if indices are consecutive, just generate range
		if right_id < left_id:
			return xrange(right_id, left_id+1)
		#
		# in this case, the indices are not consecutive
		return range(right_id, len(self.vertices)) + range(left_id+1)

	def front_points_ids(self, point):
		right_id, left_id = self.extreme_vertices_id(point)
		#
		# if the point is inside polygon, there nothing to return
		if right_id is None or left_id is None:
			return []
		#
		# if indices are consecutive, just generate range
		if left_id < right_id:
			return xrange(left_id, right_id+1)
		#
		# in this case, the indices are not consecutive
		return range(left_id, len(self.vertices)) + range(right_id+1)

	def isValid(self):
		"""
		returns true if the edges list makes up a convex polygon and are in ccw order
		"""
		it = self.iter_edges()
		first_src, first_dst = current_src, current_dst = it.next()
		for next_src, next_dst in it:
			assert current_dst == next_src
			if test_angle((current_src, current_dst), (next_src, next_dst)) < 1.:
				return False
			current_src, current_dst = next_src, next_dst
		if test_angle((current_src, current_dst), (first_src, first_dst)) < 1.:
			return False
		return True


def test_angle(edge1, edge2):
	return edge_tangent(edge1).cross(edge_tangent(edge2))

def edge_tangent(edge):
	src, dst = edge
	return dst - src

def fill_circle(position, radius, color):
		segments = 20
		increment = math.pi * 2 / segments
		radius = radius
		x, y = position
		glBegin(GL_TRIANGLE_FAN)
		glColor3f(*color)
		glVertex2f(x, y)
		for i in xrange(segments + 1):
			glVertex2f(radius*math.cos(i*increment)+x, radius*math.sin(i*increment)+y)
		glEnd()

def draw_circle(position, radius, color):
		segments = 32
		increment = math.pi * 2 / segments
		radius = radius
		x, y = position
		glBegin(GL_LINE_STRIP)
		for i in xrange(segments + 1):
			glVertex2f(radius*math.cos(i*increment)+x, radius*math.sin(i*increment)+y)
		glEnd()

class Light:
	texture = pyglet.resource.image("light.png").get_texture()

	def __init__(self, pos, color=(1.,1.,1.), outerradius=128., sourceradius=5.):
		self.position = pos #TODO: value
		self.color = tuple(color)
		self.outerradius = outerradius
		self.sourceradius = sourceradius

	def drawSource(self):
		fill_circle(self.position, self.sourceradius, self.color)
		draw_circle(self.position, self.outerradius, self.color)

	def drawLight(self):
		glBindTexture(self.texture.target, self.texture.id) #GL_TEXTURE_2D
		glColor3f(*self.color)
		x, y = self.position.x - self.outerradius, self.position.y - self.outerradius
		width = height = self.outerradius * 2
		self.texture.blit(x, y, 0, width, height)


class LightBlocker:
	def __init__(self, pos, shape):
		self.position = Point(*pos)
		self.shape = shape
		# debug
		self.labels = []
		for vertex in self.shape.vertices:
			x, y = self.position + vertex
			self.labels.append(pyglet.text.Label('%g,%g' % (vertex.x/10, vertex.y/10), x=x, y=y))

	def getBlockedLine(self, point):
		"""
		returns a sequence of vertices that form a line, indicating where light
		is blocked
		"""
		ids = self.shape.back_points_ids(point - self.position)
		return [self.position + self.shape.vertices[i] for i in ids]

	def getBlockingLine(self, point):
		ids = self.shape.front_points_ids(point - self.position)
		return [self.position + self.shape.vertices[i] for i in ids]

	def draw(self):
		glColor3f(1.,0.,0.)
		glBegin(GL_TRIANGLE_FAN)
		for vertex in self.shape.vertices:
			glVertex2f(*self.position + vertex)
		glEnd()
		# debug
		for label in self.labels:
			label.draw()


light = Light(Point(150, 200), (1.,1.,1.), 200, 4)
blocker = LightBlocker((200, 200),
                       ConvexPolygon([(-40,  10),
                                      (-20, -20),
                                      ( 10, -40),
                                      ( 40, -10),
                                      ( 20,  20),
                                      (-10,  40)]))

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
	blocking_line = blocker.getBlockingLine(light.position)
	glColor3f(1.,1.,1.)
	glBegin(GL_LINE_STRIP)
	for point in blocking_line:
		glVertex2f(*point)
	glEnd()
	# visalize begin-end of the line
	if len(blocking_line) > 0:
		glPointSize(4)
		glBegin(GL_POINTS)
		glColor3f(0., 1.0, 0.)
		glVertex2f(*blocking_line[0])  # begin
		glColor3f(0., 0.9, 0.9)
		glVertex2f(*blocking_line[-1])  # end
		glEnd()
	light.drawSource()

pyglet.app.run()
