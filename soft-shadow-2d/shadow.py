"""
http://www.gamedev.net/reference/programming/features/2dsoftshadow/
http://www.incasoftware.de/~kamm/projects/index.php/2007/09/08/soft-shadows-2d/
"""

import math
import pyglet
from pyglet.gl import *

def create_window():
	screen = pyglet.window.get_platform().get_default_display().get_default_screen()
	template = pyglet.gl.Config(alpha_size=8, depth_size=24, double_buffer=True)
	config = screen.get_best_config(template)
	context = config.create_context(None)
	return pyglet.window.Window(resizable=True, vsync=True, context=context)
win = create_window()


class Point:
	def __init__(self, x=0., y=0.):
		self.x = x
		self.y = y
	def __imul__(self, val):
		self.x *= val; self.y *= val; return self
	def __mul__(self, val):
		return Point(self.x*val, self.y*val)
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	def cross(self, other):  # cross product
		return self.x * other.y - self.y * other.x
	def dot(self, other):  # dot product
		return self.x*other.x + self.y*other.y
	def normalise(self):
		length = self.length()
		if length == 0.:
			return 0.
		self *= (1. / length)
		return length
	def normaliseCopy(self):
		p = Point(self.x, self.y)
		p.normalise()
		return p
	def length(self):  # length of vector
		return math.sqrt(self.x*self.x + self.y*self.y)
	def angle(self, other):  # angle to other vector
		dot = self.dot(other)
		cross = self.cross(other)
		return math.atan2(cross, dot)  # angle between segments
	def __iter__(self):
		return iter((self.x, self.y))


class Edge:
	def __init__(self, src, dst):
		self.src = src #TODO: value
		self.dst = dst #TODO: value
	def normal(self):
		p = self.dst - self.src
		return Point(p.y, -p.x)
	def tangent(self):
		return self.dst - self.src


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
					lastbackfacing = i-1
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
		for i in xrange(len(self.edges)):
			nexti = i+1 if i+1 < len(self.edges) else 0
			if self.edges[i].dst != self.edges[nexti].src:
				return False
			if self.edges[i].tangent().cross(self.edges[nexti].tangent()) <= 0:
				return False
		return True


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


class Light:
	texture = pyglet.image.load("media/light.png").get_texture()

	def __init__(self, pos, color=(1.,1.,1.), outerradius=128., sourceradius=5.):
		self.position = pos #TODO: value
		self.color = tuple(color)
		self.outerradius = outerradius
		self.sourceradius = sourceradius

	def drawSource(self):
		segments = 20
		increment = math.pi*2 / segments
		radius = self.sourceradius
		x, y = self.position
		glBegin(GL_TRIANGLE_FAN)
		glColor3f(1.,1.,0.)
		glVertex2f(x, y)
		for i in xrange(segments + 1):
			glVertex2f(radius*math.cos(i*increment)+x, radius*math.sin(i*increment)+y)
		glEnd()

	def drawLight(self):
		glBindTexture(self.texture.target, self.texture.id) #GL_TEXTURE_2D
		glColor3f(*self.color)
		x, y = self.position.x - self.outerradius, self.position.y - self.outerradius
		width = height = self.outerradius*2
		self.texture.blit(x, y, 0, width, height)


class Penumbra:
	texture = pyglet.image.load("media/penumbra.png").get_texture()

	class Section:
		def __init__(self, base, direction, intensity):
			self.base = base
			self.direction = direction
			self.intensity = intensity

	# line between 'base' and 'base + direction' has the
	# shadow intensity 'intensity'
	def __init__(self):
		self.sections = []

	def draw(self):
		assert len(self.sections) >= 2
		#glEnable(GL_TEXTURE_2D)
		#glBindTexture(GL_TEXTURE_2D, self.texture.id)
		glBegin(GL_TRIANGLES)
		for i, s in enumerate(self.sections[:-1]):
			glTexCoord2d(0.,                           1.); glVertex2f(*(s.base))
			glTexCoord2d(s.intensity,                  0.); glVertex2f(*(s.base + s.direction))
			glTexCoord2d(self.sections[i+1].intensity, 0.); glVertex2f(*(self.sections[i+1].base + self.sections[i+1].direction))
		glEnd()
		#glDisable(GL_TEXTURE_2D)


class Umbra:
	class Section:
		def __init__(self, base, direction):
			self.base = base
			self.direction = direction
	def __init__(self):
		self.sections = []
	def draw(self):
		style = GL_TRIANGLE_STRIP;
		glBegin(style);
		for s in self.sections[:len(self.sections)/2+1]:
			glVertex2f(s.base.x, s.base.y)
			glVertex2f(*(s.base + s.direction))
		glEnd();
		glBegin(style);
		for s in reversed(self.sections[len(self.sections)/2:]):
			glVertex2f(s.base.x, s.base.y)
			glVertex2f(*(s.base + s.direction))
		glEnd();


def renderShadow(light, blocker):
	# get the line that blocks light for the blocker and light combination
	# move the light position towards blocker by its sourceradius to avoid
	# popping of penumbrae
	normal = blocker.position - light.position
	normal.normalise()

	blockerLine = blocker.getBlockedLine(light.position + normal * light.sourceradius)

	# if the light source is completely surrounded by the blocker, don't draw its shadow
	if len(blockerLine) == len(blocker.shape.edges) + 1:
		return

	# scales a vector with respect to the light radius used for penumbra and umbra
	# lights where the tips are not supposed to be visible
	def extendDir(direction):
		return direction.normaliseCopy() * light.outerradius * 1.5

	# Displaces the light pos by sourceradius orthogonal to the line from
	# reference to the light's position. Used for calculating penumbra size.
	def getLightDisplacement(reference):
		p = reference - light.position
		lightdisp = Point(-p.y, p.x)
		lightdisp.normalise()
		lightdisp *= light.sourceradius
		if lightdisp.dot(reference - blocker.position) < 0.:
			lightdisp *= -1.
		return lightdisp

	# Gets the direction that marks the beginning of total shadow
	# for the given point.
	def getTotalShadowStartDirection(at):
		return extendDir(at - (light.position + getLightDisplacement(at)))

	#
	# build penumbrae (soft shadows), cast from the edges
	rightpenumbra = Penumbra()
	startdir = extendDir(blockerLine[0] - (light.position - getLightDisplacement(blockerLine[0])))
	rightpenumbra.sections.append(Penumbra.Section(blockerLine[0], startdir, 0.0))
	for i in xrange(len(blockerLine) - 1):
		wanted = abs(startdir.angle(getTotalShadowStartDirection(blockerLine[i])))
		available = abs(startdir.angle(blockerLine[i+1] - blockerLine[i]))
		if wanted < available:
			rightpenumbra.sections.append(Penumbra.Section(blockerLine[i], getTotalShadowStartDirection(blockerLine[i]), 1.0))
			break
		else:
			rightpenumbra.sections.append(Penumbra.Section(blockerLine[i+1], extendDir(blockerLine[i+1] - blockerLine[i]), available / wanted))

	leftpenumbra = Penumbra()
	startdir = extendDir(blockerLine[-1] - (light.position - getLightDisplacement(blockerLine[-1])))
	leftpenumbra.sections.append(Penumbra.Section(blockerLine[-1], startdir, 0.0))
	for i in xrange(i < len(blockerLine) - 1):
		wanted = abs(startdir.angle(getTotalShadowStartDirection(blockerLine[len(blockerLine)-i-1])))
		available = abs(startdir.angle(blockerLine[len(blockerLine)-i-2] - blockerLine[len(blockerLine)-i-1]))
		if wanted < available:
			leftpenumbra.sections.append(Penumbra.Section(blockerLine[len(blockerLine)-i-1], getTotalShadowStartDirection(blockerLine[len(blockerLine)-i-1]), 1.0))
			break
		else:
			leftpenumbra.sections.append(Penumbra.Section(blockerLine[len(blockerLine)-i-2], extendDir(blockerLine[len(blockerLine)-i-2] - blockerLine[len(blockerLine)-i-1]), available / wanted))

	#
	# build umbrae (hard shadows), cast between the insides of penumbrae
	umbra = Umbra()
	umbra.sections.append(Umbra.Section(rightpenumbra.sections[-1].base, rightpenumbra.sections[-1].direction))

	for vert in blockerLine[len(rightpenumbra.sections)-1:len(blockerLine)-len(leftpenumbra.sections)+1]:
		umbra.sections.append(Umbra.Section(vert, extendDir((leftpenumbra.sections[-1].direction + rightpenumbra.sections[-1].direction) * 0.5)))

	umbra.sections.append(Umbra.Section(leftpenumbra.sections[-1].base, leftpenumbra.sections[-1].direction))

	#
	# draw shadows to alpha
	umbra.draw()
	leftpenumbra.draw()
	rightpenumbra.draw()


lights = [
	# this first light will move with the mouse cursor
	Light(Point(0, 0), (1.,1.,1.), 200, 10),  # white
	# stationary lights
	Light(Point(350, 330), (0.,1.,0.)),  # Green
	Light(Point(270, 260), (0.,0.,1.)),  # Blue
	Light(Point(200, 400), (1.,1.,0.), 200),  # Yellow
	Light(Point(500,  50), (1.,0.,0.)),  # Red
	Light(Point(450,  50), (0.,1.,0.)),  # Green
	Light(Point(475,  75), (0.,0.,1.))]  # Blue

lightBlockers = [
	# small box
	LightBlocker(Point(225, 220),
		ConvexPolygon([
			Point(-10, -10),
			Point( 10, -10),
			Point( 10,  10),
			Point(-10,  10)])),
	# some polygon
	LightBlocker(Point(450, 360),
		ConvexPolygon([
			Point(-20, -20),
			Point(  0, -30),
			Point( 20, -20),
			Point( 20,   0),
			Point(  0,  20),
			Point(-15,  10)])),
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
			Point(-80,  80)]))]

@win.event
def on_draw():
	# accumulate lighting in a texture
	glClearColor(0.,0.,0.,0.)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glEnable(GL_BLEND)
	for light in lights:
		# clear alpha to full visibility
		glColorMask(False, False, False, True)
		glClear(GL_COLOR_BUFFER_BIT)
		# write shadow volumes to alpha
		glBlendFunc(GL_ONE, GL_ONE)
		glColor4f(0.,0.,0.,1.)
		for blocker in lightBlockers:
			renderShadow(light, blocker)
		# draw light
		glColorMask(True, True, True, False)
		glBlendFunc(GL_ONE_MINUS_DST_ALPHA, GL_ONE)
		light.drawLight()
	# render regular scene
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	for blocker in lightBlockers:
		blocker.draw()
	# render lights on top, so they're clearly visible
	glBlendFunc(GL_ONE, GL_ZERO)
	for light in lights:
		light.drawSource()


@win.event
def on_mouse_motion(x, y, dx, dy):
	lights[0].position.x = x
	lights[0].position.y = y

pyglet.app.run()
