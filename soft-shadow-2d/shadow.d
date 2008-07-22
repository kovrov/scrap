/*
	This code is released under the zlib/libpng license.

	Copyright (C) 2007 Christian Kamm (kamm incasoftware de)
	
	This software is provided 'as-is', without any express or implied
	warranty.  In no event will the authors be held liable for any damages
	arising from the use of this software.
	
	Permission is granted to anyone to use this software for any purpose,
	including commercial applications, and to alter it and redistribute it
	freely, subject to the following restrictions:
	
	1. The origin of this software must not be misrepresented; you must not
	   claim that you wrote the original software. If you use this software
	   in a product, an acknowledgment in the product documentation would be
	   appreciated but is not required.
	2. Altered source versions must be plainly marked as such, and must not be
	   misrepresented as being the original software.
	3. This notice may not be removed or altered from any source distribution.
*/
				 
module shadow;

import std.stdio : writefln;
import std.math : fabs, PI;

static import arc.window;
static import arc.input;
static import arc.time;
import arc.texture : Texture;
import arc.types : Point, Color, Size;
import arc.draw.image : drawImage;

import derelict.opengl.gl;

//TODO: Hardware pixel buffers would speed things up

/// oriented edge, normal is 'to the right'
struct Edge
{
	Point src, dst;
	
	Point normal()
	{
		Point rotate90cw(ref Point p)	{
			return Point(p.y, -p.x);
		}
		
		return rotate90cw(dst - src);
	}
	
	Point tangent()
	{
		return dst - src;
	}
}

/// holds the vertices of a convex polygon
struct ConvexPolygon
{
	/// constructs from a vertex list, vertices must be in ccw order
	static ConvexPolygon fromVertices(Point[] verts)
	{
		assert(verts.length > 3, "Polygon needs at least 3 vertices");
		
		ConvexPolygon poly;
		for(size_t i = 1; i < verts.length; ++i)
			poly.edges ~= Edge(verts[i-1], verts[i]);
		poly.edges ~= Edge(verts[$-1], verts[0]);
		
		assert(poly.isValid());
		return poly;
	}
	
	/// edges, in ccw order
	Edge[] edges;

	/**
		Finds the edges that face away from a given location 'src'.
	
		Returns:
			A list of indices into 'edges'. In ccw order.
	**/
	size_t[] getBackfacingEdgeIndices(ref Point src)
	{
		assert(isValid());
		
		size_t[] result;
		
		// find the indices of the two edges that face away from 'src' and that
		// have one adjacent edge facing towards 'src'
		size_t firstbackfacing = size_t.max, lastbackfacing = size_t.max;
		
		{			
			bool prev_edge_front, cur_edge_front;
			foreach(i, ref edge; edges)
			{
				if(edge.normal.dot(src - edge.src) < 0)
					cur_edge_front = true;
				else
					cur_edge_front = false;
				
				if(i != 0)
				{
					if(cur_edge_front && !prev_edge_front)
						firstbackfacing = i;
					else if(!cur_edge_front && prev_edge_front)
						lastbackfacing = i-1;
				}
				
				prev_edge_front = cur_edge_front;
			}
		}
		
		// if no change between front and backfacing vertices was found,
		// we are inside the polygon, consequently all edges face backwards
		if(firstbackfacing == size_t.max && lastbackfacing == size_t.max)
		{
			for(size_t i = 0; i < edges.length; ++i)
				result ~= i;
			return result;
		}
		// else, if one one of the changes was found, we missed the one at 0
		else if(firstbackfacing == size_t.max)
			firstbackfacing = 0;
		else if(lastbackfacing == size_t.max)
			lastbackfacing = edges.length - 1;
		
		// if this is true, we can just put the indices in result in order
		if(firstbackfacing <= lastbackfacing)
		{
			for(size_t i = firstbackfacing; i <= lastbackfacing; ++i)
				result ~= i;
		}
		// else we must go from first to $ and from 0 to last
		else
		{
			for(size_t i = firstbackfacing; i < edges.length; ++i)
				result ~= i;
			for(size_t i = 0; i <= lastbackfacing; ++i)
				result ~= i;
		}
		
		return result;
	}
	
	/// returns true if the edges list makes up a convex polygon and are in ccw order
	bool isValid()
	{
		for(size_t i = 0; i < edges.length; ++i)
		{
			size_t nexti = i+1 < edges.length ? i+1 : 0;
			if(edges[i].dst != edges[nexti].src)
				return false;
			if(edges[i].tangent().cross(edges[nexti].tangent()) <= 0)
				return false;
		}
		
		return true;
	}
}

/// defines an area that blocks light by a convex polygon
struct LightBlocker
{
	Point position;
	ConvexPolygon shape;
	
	/// returns a sequence of vertices that form a line, indicating
	/// where light is blocked
	Point[] getBlockedLine(ref Point src)
	{
		size_t[] edgeIndices = shape.getBackfacingEdgeIndices(src - position);
		
		Point[] ret;
		ret ~= position + shape.edges[edgeIndices[0]].src;
		foreach(ind; edgeIndices)
			ret ~= position + shape.edges[ind].dst;
		
		return ret;
	}
	
	void draw()
	{
		glDisable(GL_TEXTURE_2D);
		Color.Red.setGLColor();
		
		glBegin(GL_TRIANGLE_FAN);
		foreach(ref edge; shape.edges)
		{
			glVertex2f(position.x + edge.src.x, position.y + edge.src.y); 
			glVertex2f(position.x + edge.dst.x, position.y + edge.dst.y); 
		}
		glEnd();
	}
}

/// a light source
struct Light
{
	Point position;
	Color color = Color.White;
	
	/// the light does not provide any illumination further away than that
	real outerradius = 128;
	
	/** 
		Controls the size of the lightsource and thereby the softness of shadows.
		If lightblockers are smaller than this, there'll be artifacts.
	**/
	real sourceradius = 5;
	
	void draw()
	{
		glDisable(GL_TEXTURE_2D);
		Color.Yellow.setGLColor();
		
		glBegin(GL_TRIANGLE_FAN);
		
		makeVertex(position);
		
		int segments = 20;
		for(int i = 0; i < segments + 1; ++i)
		{
			makeVertex(position + Point.fromPolar(sourceradius, 2*PI*i / segments));
		}
		
		glEnd();
	}
	
	static Texture texture;
}

/// convenience function to convert points to OpenGL vertices
void makeVertex(inout Point p) { 
	glVertex2f(p.x, p.y); 
}


/**
	Penumbrae are the regions of half-shadow generated by voluminous
	light sources.
	
	They are represented by a series of sections, each containing a line
	and an intensity. The intensity gives the strength of the shadow on
	that line between 0. (fully lit) and 1. (complete shadow).
**/
struct Penumbra
{
	/// line line between 'base' and 'base + direction' has the
	/// shadow intensity 'intensity'
	struct Section
	{
		Point base;
		Point direction;
		real intensity;
	}
	Section[] sections;
	
	void draw()
	{
		assert(sections.length >= 2);
		
		glEnable(GL_TEXTURE_2D);
		glBindTexture(GL_TEXTURE_2D, texture.getID());
		
		glBegin(GL_TRIANGLES);
		
		foreach(i, ref s; sections[0..$-1])
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
}
				
/**
	Umbrae are the regions of full shadow behind light blockers.
	
	Represented by a series of lines.
**/
struct Umbra 
{ 
	struct Section
	{
		Point base; 
		Point direction;
	}
	Section[] sections;
	
	void draw()
	{
		assert(sections.length >= 2);
		
		auto style = GL_TRIANGLE_STRIP;
		// auto style = GL_LINES;
		
		// the umbra draw regions (if considered quads) can sometimes 
		// be concave, so use triangles and start once from left and 
		// once from right to minimize problems
		
		glBegin(style);		
		foreach(ref s; sections[0..$/2+1])
		{
			makeVertex(s.base);
			makeVertex(s.base + s.direction);
		}		
		glEnd();
	
		glBegin(style);		
		foreach_reverse(ref s; sections[$/2..$])
		{
			makeVertex(s.base);
			makeVertex(s.base + s.direction);
		}		
		glEnd();		
	}
}

//
// global world data
//
LightBlocker[] lightBlockers;
Light[] lights;


void main()
{
	arc.window.open("2D Shadows", 640, 480, false);
	arc.input.open();
	arc.time.open();
	
	//
	// load textures
	//
	Penumbra.texture = Texture("media/penumbra.png");
	Light.texture = Texture("media/light.png");
	
	//
	// setup world data
	//
	setupWorld();
	
	//
	// initialize dynamic texture
	//
	GLuint rendertex;
	uint rendertexsize = 256;
	{
		ubyte[] texdata = new ubyte[rendertexsize*rendertexsize*4];		
		foreach (ref color; texdata)
			color = 255;
		glGenTextures(1, &rendertex);
		glBindTexture(GL_TEXTURE_2D, rendertex);
		glTexImage2D(GL_TEXTURE_2D, 0, 4, rendertexsize, rendertexsize, 0,
		             GL_RGBA, GL_UNSIGNED_BYTE, texdata.ptr);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
		delete texdata;	
	}

	//
	// main loop
	//
	while (!arc.input.keyDown(arc.input.ARC_QUIT))
	{
		arc.time.process();
		arc.input.process();
		
		// light 0 follows the mouse
		lights[0].position = arc.input.mousePos;
		
		//
		// accumulate lighting in a texture
		//
		glClearColor(0., 0., 0., 0.);
		glViewport(0, 0, rendertexsize, rendertexsize);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		foreach (inout light; lights)
		{
			// clear alpha to full visibility
			glColorMask(false, false, false, true);
			glClear(GL_COLOR_BUFFER_BIT);
			
			// write shadow volumes to alpha
			glBlendFunc(GL_ONE, GL_ONE);
			glDisable(GL_TEXTURE_2D);
			glColor4f(0., 0., 0., 1.);
			foreach (inout blocker; lightBlockers)
			{
				renderShadow(light, blocker);
			}
						
			// draw light
			glColorMask(true, true, true, false);
			glBlendFunc(GL_ONE_MINUS_DST_ALPHA, GL_ONE);
			drawImage(light.texture, light.position, Size(2*light.outerradius, 2*light.outerradius), Point(0,0), 0, light.color);
		}
		
		//
		// copy lighting into texture
		//
		glBindTexture(GL_TEXTURE_2D, rendertex);
		glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGB8, 0, 0, rendertexsize, rendertexsize, 0);
		
		//
		// render regular scene
		//
		glViewport(0,0,640,480);
		glClearColor(1.,1.,1.,0.);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		foreach (ref blocker; lightBlockers)
			blocker.draw();
		
		//
		// apply lighting by rending light texture on top
		//
		glBlendFunc(GL_DST_COLOR, GL_ZERO);
		glEnable(GL_TEXTURE_2D);
		glBindTexture(GL_TEXTURE_2D, rendertex);  
		Color.White.setGLColor();
		glBegin(GL_QUADS);
		glTexCoord2d(0.,1.); glVertex2f(0,0); 
		glTexCoord2d(0.,0.); glVertex2f(0,480);
		glTexCoord2d(1.,0.); glVertex2f(640,480);
		glTexCoord2d(1.,1.); glVertex2f(640,0);     
		glEnd();
		
		//
		// render lights on top, so they're clearly visible
		//
		glBlendFunc(GL_ONE, GL_ZERO);
		foreach (ref light; lights)
			light.draw();
		
		//
		// swap and limit framerate
		//
		arc.window.swap();		
		arc.time.limitFPS(40);
	}
}

/**
	Draws the shadow of 'blocker' under the given 'light'
**/
void renderShadow(ref Light light, ref LightBlocker blocker)
{
	// get the line that blocks light for the blocker and light combination
	// move the light position towards blocker by its sourceradius to avoid
	// popping of penumbrae
	Point[] blockerLine = blocker.getBlockedLine(light.position + (blocker.position - light.position).normaliseCopy() * light.sourceradius);
	
	// if the light source is completely surrounded by the blocker, don't draw its shadow
	if(blockerLine.length == blocker.shape.edges.length + 1)
		return;
	
	/**
		scales a vector with respect to the light radius
		used for penumbra and umbra lights where the tips
		are not supposed to be visible
	**/
	Point extendDir(ref Point dir) { 
		return dir.normaliseCopy() * light.outerradius * 1.5; 
	}
	
	/**
		Displaces the light pos by sourceradius orthogonal to the line from
		reference to the light's position. Used for calculating penumbra size.
	**/
	Point getLightDisplacement(ref Point reference)	{
		Point lightdisp = Point.makePerpTo(reference - light.position);
		lightdisp.normalise();
		lightdisp *= light.sourceradius;
		if(lightdisp.dot(reference - blocker.position) < 0.)
			lightdisp *= -1.;
		return lightdisp;
	}
	
	/**
		Gets the direction that marks the beginning of total shadow
		for the given point.
	**/
	Point getTotalShadowStartDirection(ref Point at) {
		return extendDir(at - (light.position + getLightDisplacement(at)));
	}

	//
	// build penumbrae (soft shadows), cast from the edges
	//
	
	Penumbra rightpenumbra;
	{
		Point startdir = extendDir(blockerLine[0] - (light.position - getLightDisplacement(blockerLine[0])));
		rightpenumbra.sections ~= Penumbra.Section(
			blockerLine[0], 
			startdir,
			0.0);
		for(size_t i = 0; i < blockerLine.length - 1; ++i)
		{
			real wanted = fabs(startdir.angle(getTotalShadowStartDirection(blockerLine[i])));
			real available = fabs(startdir.angle(blockerLine[i+1] - blockerLine[i]));
			
			if(wanted < available)
			{
				rightpenumbra.sections ~= Penumbra.Section(
					blockerLine[i], 
					getTotalShadowStartDirection(blockerLine[i]), 
					1.0);
				break;
			}
			else
			{
				rightpenumbra.sections ~= Penumbra.Section(
					blockerLine[i+1], 
					extendDir(blockerLine[i+1] - blockerLine[i]),
					available / wanted);
			}
		}
	}
	
	Penumbra leftpenumbra;
	{
		Point startdir = extendDir(blockerLine[$-1] - (light.position - getLightDisplacement(blockerLine[$-1])));
		leftpenumbra.sections ~= Penumbra.Section(
			blockerLine[$-1], 
			startdir,
			0.0);
		for(size_t i = 0; i < blockerLine.length - 1; ++i)
		{
			real wanted = fabs(startdir.angle(getTotalShadowStartDirection(blockerLine[$-i-1])));
			real available = fabs(startdir.angle(blockerLine[$-i-2] - blockerLine[$-i-1]));
			
			if(wanted < available)
			{
				leftpenumbra.sections ~= Penumbra.Section(
					blockerLine[$-i-1], 
					getTotalShadowStartDirection(blockerLine[$-i-1]), 
					1.0);
				break;
			}
			else
			{
				leftpenumbra.sections ~= Penumbra.Section(
					blockerLine[$-i-2], 
					extendDir(blockerLine[$-i-2] - blockerLine[$-i-1]),
					available / wanted);
			}
		}
	}
	
	//
	// build umbrae (hard shadows), cast between the insides of penumbrae
	//
					
	Umbra umbra;
						
	umbra.sections ~= Umbra.Section(rightpenumbra.sections[$-1].base, rightpenumbra.sections[$-1].direction);
				
	foreach(ref vert; blockerLine[rightpenumbra.sections.length-1..$-leftpenumbra.sections.length+1])
		umbra.sections ~= Umbra.Section(vert, extendDir(0.5 * (leftpenumbra.sections[$-1].direction + rightpenumbra.sections[$-1].direction)));
	
	umbra.sections ~= Umbra.Section(leftpenumbra.sections[$-1].base, leftpenumbra.sections[$-1].direction);
						
	//
	// draw shadows to alpha
	//
	
	umbra.draw();
	rightpenumbra.draw();
	leftpenumbra.draw();	
}


/**
	Setup some blockers and some lights
**/
void setupWorld()
{
	// small box
	lightBlockers ~= LightBlocker(Point(225,220), 
		ConvexPolygon.fromVertices([
			Point(-10,-10),
			Point( 10,-10),
			Point( 10, 10),
			Point(-10, 10)]));
	
	// some polygon
	lightBlockers ~= LightBlocker(Point(450,360), 
		ConvexPolygon.fromVertices([
			Point(-20,-20),
			Point(  0,-30),
			Point( 20,-20),
			Point( 20,  0),
			Point( 0,  20),
			Point(-15, 10)]));

	// rectangle that's much longer than wide
	lightBlockers ~= LightBlocker(Point(150,100), 
		ConvexPolygon.fromVertices([
			Point(-120,-10),
			Point( 300,-10),
			Point( 300, 10),
			Point(-120, 10)]));
		
	// diagonal line
	lightBlockers ~= LightBlocker(Point(300,300), 
		ConvexPolygon.fromVertices([
			Point( 80,-80),
			Point(100,-70),
			Point(-70,100),
			Point(-80,80)]));

	
	// this first light will move with the mouse cursor
	lights ~= Light(Point(0,0), Color.White, 200, 10);
	
	// stationary lights
	lights ~= Light(Point(350,330), Color.Green);
	lights ~= Light(Point(270,260), Color.Blue);
	lights ~= Light(Point(200,400), Color.Yellow, 200);
	lights ~= Light(Point(500,50), Color.Red);
	lights ~= Light(Point(450,50), Color.Green);
	lights ~= Light(Point(475,75), Color.Blue);		
}
