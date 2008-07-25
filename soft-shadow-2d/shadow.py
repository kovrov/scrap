"""
http://www.gamedev.net/reference/programming/features/2dsoftshadow/
http://www.incasoftware.de/~kamm/projects/index.php/2007/09/08/soft-shadows-2d/
"""

import pyglet
from pyglet.gl import *


class Color:
	pass

class Size:
	pass

class Point:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0

'''
class Edge:
	def __init__(self):
		self.src = Point()
		self.dst = Point()
	def normal():
		p = dst - src
		return Point(p.y, -p.x)
	def tangent():
		return dst - src
'''

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

	"""
		Finds the edges that face away from a given location 'src'.

		Returns:
			A list of indices into 'edges'. In ccw order.
	"""
	def getBackfacingEdgeIndices(src):
		assert(isValid());

		size_t[] result;

		# find the indices of the two edges that face away from 'src' and that
		# have one adjacent edge facing towards 'src'
		size_t firstbackfacing = size_t.max, lastbackfacing = size_t.max;

		{
			bool prev_edge_front, cur_edge_front;
			for i, ref edge; edges:
				if (edge.normal.dot(src - edge.src) < 0)
					cur_edge_front = true;
				else
					cur_edge_front = false;

				if (i != 0)
				{
					if (cur_edge_front && !prev_edge_front)
						firstbackfacing = i;
					else if (!cur_edge_front && prev_edge_front)
						lastbackfacing = i-1;
				}

				prev_edge_front = cur_edge_front;

		}

		# if no change between front and backfacing vertices was found,
		# we are inside the polygon, consequently all edges face backwards
		if firstbackfacing == size_t.max && lastbackfacing == size_t.max:
			for (size_t i = 0; i < edges.length; ++i)
				result.append(i)
			return result;
		# else, if one one of the changes was found, we missed the one at 0
		elif (firstbackfacing == size_t.max)
			firstbackfacing = 0;
		elif (lastbackfacing == size_t.max)
			lastbackfacing = edges.length - 1;

		# if this is true, we can just put the indices in result in order
		if firstbackfacing <= lastbackfacing:
			for (size_t i = firstbackfacing; i <= lastbackfacing; ++i)
				result.append(i)
		# else we must go from first to $ and from 0 to last
		else:
			for (size_t i = firstbackfacing; i < edges.length; ++i)
				result.append(i)
			for (size_t i = 0; i <= lastbackfacing; ++i)
				result.append(i)

		return result;

	# returns true if the edges list makes up a convex polygon and are in ccw order
	bool isValid():
		for (size_t i = 0; i < edges.length; ++i)
			size_t nexti = i+1 < edges.length ? i+1 : 0;
			if (edges[i].dst != edges[nexti].src)
				return false;
			if (edges[i].tangent().cross(edges[nexti].tangent()) <= 0)
				return false;
		return true;


class LightBlocker:
	def __init__(self):
		self.position = Point()
		self.shape = ConvexPolygon()

	# returns a sequence of vertices that form a line, indicating
	# where light is blocked
	def getBlockedLine(self, src):
		edgeIndices = self.shape.getBackfacingEdgeIndices(src - self.position)
		ret = []  #Point[]
		ret.append(self.position + self.shape.edges[edgeIndices[0]].src)
		for ind in edgeIndices:
			ret.append(self.position + self.shape.edges[ind].dst)
		return ret

	def draw(self, offset = Point(0,0)):
		glDisable(GL_TEXTURE_2D)
		glColor3f(1.0, 0.0, 0.0)
		glBegin(GL_TRIANGLE_FAN)
		for edge in self.shape.edges:
			glVertex2f(self.position.x + offset.x + edge.src.x, self.position.y + offset.y + edge.src.y)
			glVertex2f(self.position.x + offset.x + edge.dst.x, self.position.y + offset.y + edge.dst.y)
		glEnd()


class Light:
	texture = Texture()
	def __init__(self):
		self.position = Point()
		self.color = Color.White
		self.outerradius = 128.0
		self.sourceradius = 5.0
	def draw():
		glDisable(GL_TEXTURE_2D);
		Color.Yellow.setGLColor();
		glBegin(GL_TRIANGLE_FAN);
		makeVertex(position);
		segments = 20;
		for (int i = 0; i < segments + 1; ++i)
			makeVertex(position + Point.fromPolar(sourceradius, 2*PI*i / segments));
		glEnd()


def makeVertex(p):
	glVertex2f(p.x, p.y)

'''
class Penumbra:
	# line line between 'base' and 'base + direction' has the
	# shadow intensity 'intensity'
	class Section:
	{
		Point base;
		Point direction;
		real intensity;
	}
	Section[] sections;

	def draw()
	{
		assert(sections.length >= 2);

		glEnable(GL_TEXTURE_2D);
		glBindTexture(GL_TEXTURE_2D, texture.getID());

		glBegin(GL_TRIANGLES);

		for (i, ref s; sections[0..$-1])
		{
			glTexCoord2d(0., 1.);
			makeVertex(s.base);

			glTexCoord2d(s.intensity, 0.);
			makeVertex(s.base + s.direction);

			glTexCoord2d(sections[i+1].intensity, 0.);
			makeVertex(sections[i+1].base + sections[i+1].direction);
		}

		glEnd();

		glDisable(GL_TEXTURE_2D);
	}

	static Texture texture;
'''

'''
class Umbra:
	class Section:
		def __init(self):
			self.base =  Point()
			self.direction = Point()
	def __init__(self):
		self.sections = [] #Section[]
	def draw():
		style = GL_TRIANGLE_STRIP;
		glBegin(style);
		for (ref s; sections[0..$/2+1]):
			makeVertex(s.base);
			makeVertex(s.base + s.direction);
		glEnd();
		glBegin(style);
		foreach_reverse(ref s; sections[$/2..$])
			makeVertex(s.base);
			makeVertex(s.base + s.direction);
		glEnd();
'''

'''
def renderShadow(light, blocker):
	# get the line that blocks light for the blocker and light combination
	# move the light position towards blocker by its sourceradius to avoid
	# popping of penumbrae
	normal = blocker.position - light.position
	normal.normalise()

	Point[] blockerLine = blocker.getBlockedLine(light.position + normal * light.sourceradius);

	# if the light source is completely surrounded by the blocker, don't draw its shadow
	if (blockerLine.length == blocker.shape.edges.length + 1)
		return;

	"""
		scales a vector with respect to the light radius
		used for penumbra and umbra lights where the tips
		are not supposed to be visible
	"""
	Point extendDir(ref Point dir) {
		return dir.normaliseCopy() * light.outerradius * 1.5;
	}

	"""
		Displaces the light pos by sourceradius orthogonal to the line from
		reference to the light's position. Used for calculating penumbra size.
	"""
	Point getLightDisplacement(ref Point reference)	{
		Point lightdisp = Point.makePerpTo(reference - light.position);
		lightdisp.normalise();
		lightdisp *= light.sourceradius;
		if (lightdisp.dot(reference - blocker.position) < 0.)
			lightdisp *= -1.;
		return lightdisp;
	}

	"""
		Gets the direction that marks the beginning of total shadow
		for the given point.
	"""
	Point getTotalShadowStartDirection(ref Point at) {
		return extendDir(at - (light.position + getLightDisplacement(at)));
	}

	#
	# build penumbrae (soft shadows), cast from the edges
	#

	Penumbra rightpenumbra;
	{
		Point startdir = extendDir(blockerLine[0] - (light.position - getLightDisplacement(blockerLine[0])));
		rightpenumbra.sections.append(Penumbra.Section(blockerLine[0], startdir, 0.0))
		for (size_t i = 0; i < blockerLine.length - 1; ++i)
		{
			real wanted = abs(startdir.angle(getTotalShadowStartDirection(blockerLine[i])));
			real available = abs(startdir.angle(blockerLine[i+1] - blockerLine[i]));

			if (wanted < available)
			{
				rightpenumbra.sections.append(Penumbra.Section(blockerLine[i], getTotalShadowStartDirection(blockerLine[i]), 1.0))
				break;
			}
			else
			{
				rightpenumbra.sections.append(Penumbra.Section(
					blockerLine[i+1],
					extendDir(blockerLine[i+1] - blockerLine[i]),
					available / wanted))
			}
		}
	}

	Penumbra leftpenumbra;
	{
		Point startdir = extendDir(blockerLine[$-1] - (light.position - getLightDisplacement(blockerLine[$-1])));
		leftpenumbra.sections.append(Penumbra.Section(
			blockerLine[$-1],
			startdir,
			0.0))
		for (size_t i = 0; i < blockerLine.length - 1; ++i)
		{
			real wanted = abs(startdir.angle(getTotalShadowStartDirection(blockerLine[$-i-1])));
			real available = abs(startdir.angle(blockerLine[$-i-2] - blockerLine[$-i-1]));

			if (wanted < available)
			{
				leftpenumbra.sections.append(Penumbra.Section(
					blockerLine[$-i-1],
					getTotalShadowStartDirection(blockerLine[$-i-1]),
					1.0))
				break;
			}
			else
			{
				leftpenumbra.sections.append(Penumbra.Section(
					blockerLine[$-i-2],
					extendDir(blockerLine[$-i-2] - blockerLine[$-i-1]),
					available / wanted))
			}
		}
	}

	#
	# build umbrae (hard shadows), cast between the insides of penumbrae
	#
	Umbra umbra;

	umbra.sections.append(Umbra.Section(rightpenumbra.sections[$-1].base, rightpenumbra.sections[$-1].direction))

	for (ref vert; blockerLine[rightpenumbra.sections.length-1..$-leftpenumbra.sections.length+1])
		umbra.sections.append(Umbra.Section(vert, extendDir(0.5 * (leftpenumbra.sections[$-1].direction + rightpenumbra.sections[$-1].direction))))

	umbra.sections.append(Umbra.Section(leftpenumbra.sections[$-1].base, leftpenumbra.sections[$-1].direction))

	#
	# draw shadows to alpha
	#
	umbra.draw();
	rightpenumbra.draw();
	leftpenumbra.draw();
'''


win = pyglet.window.Window(resizable=True, vsync=True)

lights = [
	# this first light will move with the mouse cursor
	Light(Point(0, 0), Color.White, 200, 10),
	# stationary lights
	Light(Point(350, 330), Color.Green),
	Light(Point(270, 260), Color.Blue),
	Light(Point(200, 400), Color.Yellow, 200),
	Light(Point(500,  50), Color.Red),
	Light(Point(450,  50), Color.Green),
	Light(Point(475,  75), Color.Blue)]

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
	glClearColor(0., 0., 0., 0.)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	for light in lights:
		# clear alpha to full visibility
		glColorMask(False, False, False, True)
		glClear(GL_COLOR_BUFFER_BIT)
		# write shadow volumes to alpha
		glBlendFunc(GL_ONE, GL_ONE)
		glDisable(GL_TEXTURE_2D)
		glColor4f(0., 0., 0., 1.)
	#	for blocker in lightBlockers:
	#		renderShadow(light, blocker);
		# draw light
		glColorMask(True, True, True, False)
		glBlendFunc(GL_ONE_MINUS_DST_ALPHA, GL_ONE)
		drawImage(light.texture, light.position, Size(2*light.outerradius, 2*light.outerradius), Point(0,0), 0, light.color)
	# render regular scene
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	for blocker in lightBlockers:
		blocker.draw()
	# render lights on top, so they're clearly visible
	glBlendFunc(GL_ONE, GL_ZERO)
	for light in lights:
		light.draw()


@win.event
def on_mouse_motion(x, y, dx, dy):
	print "on_mouse_motion"


#main
arc.window.open("2D Shadows", 640, 480, false);
arc.input.open();
# load textures
Penumbra.texture = Texture("media/penumbra.png");
Light.texture = Texture("media/light.png");
# setup world data
setupWorld();
# initialize dynamic texture
GLuint rendertex;
uint rendertexsize = 256;
{
	ubyte[] texdata = new ubyte[rendertexsize*rendertexsize*4];
	for (ref color; texdata)
		color = 255;
	glGenTextures(1, &rendertex);
	glBindTexture(GL_TEXTURE_2D, rendertex);
	glTexImage2D(GL_TEXTURE_2D, 0, 4, rendertexsize, rendertexsize, 0,
				 GL_RGBA, GL_UNSIGNED_BYTE, texdata.ptr);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
	delete texdata;
}

pyglet.app.run()
