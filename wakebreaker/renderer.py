import ctypes
#import game
#import renderdata
#import vector3
from pyglet.gl import *

from util import Vector3

class Renderer:
	# sets up the openGL enable/disables
	def __init__(self):
		self.currData = None  # used to reduce state changes
		self.currTexture = None  # used to reduce state changes
		self.fogEnabled = False
		# Enable the zbuffer
		glEnable(GL_DEPTH_TEST)
		# Disable lighting and alpha blending
		glDisable(GL_LIGHTING)
		glDisable(GL_BLEND)
		glCullFace(GL_BACK)
		glEnable(GL_CULL_FACE)
		glEnable(GL_TEXTURE_2D)
		glDisable(GL_DITHER)
		glClearColor(0.745, 0.95, 1.0, 0.0)
		glMatrixMode(GL_PROJECTION)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		# Set up fog
		glFogf(GL_FOG_DENSITY, 0.01)
		glFogi(GL_FOG_MODE, GL_EXP)
		glHint(GL_FOG_HINT, GL_DONT_CARE)
		#------------
		color = (GLfloat*4)(*(0.745, 0.95, 1.0, 0.0))
		glFogfv(GL_FOG_COLOR, ctypes.cast(ctypes.pointer(color), ctypes.POINTER(GLfloat)))
		#--------
		# Set the model view to identity
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		# Enable the arrays we want used when we glDrawElements()
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_TEXTURE_COORD_ARRAY)


	# Renders a renderInstance to the screen
	def render(self, data):
		if data.renderData is not self.currData:
			if data.renderData.texCoords:
				tex_coords_gl = (GLfloat * len(data.renderData.texCoords))(*data.renderData.texCoords)
				glTexCoordPointer(2, GL_FLOAT, 0, tex_coords_gl)
			vertices_gl = (GLfloat * len(data.renderData.vertices))(*data.renderData.vertices)
			glVertexPointer(3, GL_FLOAT, 0, vertices_gl)
			if data.renderData.colorData:
				color_data_gl = (GLfloat * len(data.renderData.colorData))(*data.renderData.colorData)
				glColorPointer(4, GL_UNSIGNED_BYTE, 0, color_data_gl)  # Set the color data source
			self.currData = data.renderData
		if data.renderData.texture and self.currTexture != data.renderData.texture.id:
			glBindTexture(GL_TEXTURE_2D, data.renderData.texture.id)
			self.currTexture = data.renderData.texture.id
		glPushMatrix()
		glTranslatef(data.position.x, data.position.y, data.position.z)
		glScalef(data.scale.x, data.scale.y, data.scale.z)
		glRotatef(data.rotation.y, 0.0, 1.0, 0.0)
		glRotatef(data.rotation.x, 1.0, 0.0, 0.0)
		glRotatef(data.rotation.z, 0.0, 0.0, 1.0)
		indices_len = len(data.renderData.indices)
		indices_gl = (GLuint* indices_len)(*data.renderData.indices)
		glDrawElements(GL_TRIANGLES, indices_len, data.renderData.indexDataType, indices_gl)  # Draw the triangle
		glPopMatrix()


	#Draws a screen size quad with texure on it
	def draw2DQuad(self, tex):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glLoadIdentity()
		glTranslatef(0.0, -0.25, -5.0)
		glBindTexture(GL_TEXTURE_2D, tex.id)
		face_data = (
				-3.0, -2.0, 0.0,    # First vertex position
				 3.0, -2.0, 0.0,    # Second vertex position
				-3.0,  2.0, 0.0,    # Third vertex position
				 3.0,  2.0, 0.0,    # First vertex position
				 3.0, -2.0, 0.0,    # Second vertex position
				-3.0,  2.0, 0.0)    # Third vertex position
		face_data_gl = (GLfloat * len(face_data))(*face_data)
		glVertexPointer(3, GL_FLOAT, 0, face_data_gl)  # Set the vertex (position) data source
		tex_coord_data = (
				 0.0, 0.0,
				 1.0, 0.0,
				 0.0, 1.0,
				 1.0, 1.0,
				 1.0, 0.0,
				 0.0, 1.0)
		tex_coord_data_gl = (GLfloat * len(tex_coord_data))(*tex_coord_data)
		glTexCoordPointer(2, GL_FLOAT, 0, tex_coord_data_gl)  # Set the vertex (position) data source
		indices_gl = (c_ubyte * 6)(0, 1, 2, 5, 4, 3)
		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, indices_gl)  # Draw the triangle
		glPopMatrix()


	def EnableFog(self):
		if not self.fogEnabled:
			glEnable(GL_FOG)
			self.fogEnabled = True

	def DisableFog(self):
		if self.fogEnabled:
			glDisable(GL_FOG)
			self.fogEnabled = False





# This stores the positional data and renderable data of a an object
class RenderInstance:
	def __init__(self):
		self.renderData = None  # the render data, as requested from the modelmanager
		self.position   = Vector3(0, 0, 0)
		self.rotation   = Vector3(0, 0, 0)
		self.scale      = Vector3(65536, 65536, 65536)

	def rotate(self, p):  # Vector3
		# cap all the values
		if m_rotation.x + p.x > 23527424 or m_rotation.x + p.x < -23527424:
			m_rotation.x = 0;
		if m_rotation.y + p.y > 23527424 or m_rotation.y + p.y < -23527424:
			m_rotation.y = 0;
		if m_rotation.z + p.z > 23527424 or m_rotation.z + p.z < -23527424:
			m_rotation.z = 0;
		m_rotation += p;

	def scale(self, s):
		if type(s) is Vector3:
			self.scale = s
		else:
			self.scale.x = s[0]
			self.scale.y = s[1]
			self.scale.z = s[2]

	def translate(self, trans):
		if type(trans) is Vector3:
			self.position += trans
		else:
			self.position.x += trans[0]
			self.position.y += trans[1]
			self.position.z += trans[2]



class RenderData:
	def __init__(self, vertices, indices, uvmap, texture):
		self.indices =   indices  # uint16*
		self.vertices =  sum(vertices[1:], vertices[0])  # Vector3*
		self.texCoords = sum(uvmap[1:], uvmap[0])
		self.texture = texture
		self.colorData = None  # Color4*
		self.indexDataType = GL_UNSIGNED_SHORT



class TexCoord2:
	def __init__(self):
		self.u = 0
		self.v = 0



if __name__ == '__main__':
	import math


	win = pyglet.window.Window(320, 240)
	@win.event
	def on_resize(width, height):
		fov = 45.0
		near = 1.0
		far = 10000.0
		aspect = float(width) / float(height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(fov, aspect, near, far)
		glMatrixMode(GL_MODELVIEW)
		glViewport(0, 0, width, height)
		return pyglet.event.EVENT_HANDLED

	@win.event
	def on_draw():
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		r.draw2DQuad(tex)

	r = Renderer()
	tex = pyglet.image.load('splash.png').get_texture()
	pyglet.app.run()
