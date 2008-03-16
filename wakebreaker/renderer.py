import ctypes
#import game
#import renderdata
#import vector3
from pyglet.gl import *

from util import Vector3

class Renderer:
	def __init__(self):
		self.currData = None  # used to reduce state changes
		self.currTexture = None  # used to reduce state changes
		self.fogEnabled = False

	# sets up the openGL enable/disables
	def initialize(self, width, height):
		self.currTexture = -1
		# Enable the zbuffer
		glEnable(GL_DEPTH_TEST)
		# Set the view port size to the window size
		glViewport(0, 0, width, height)
		# Diable lighting and alpha blending
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


	# Renders a renderInstance tot he screen
	def render(self, data):
		if data.renderData != self.currData:
			if data.renderData.texCoords:
				glTexCoordPointer(2,GL_FIXED,0, data.renderData.texCoords[0])
			glVertexPointer(3, GL_FIXED, 0, data.renderData.vertices[0].v)
			if data.renderData.colorData:
				glColorPointer(4, GL_UNSIGNED_BYTE, 0, data.renderData.colorData[0].v)	# Set the color data source
			self.currData = data.renderData
		if data.renderData.texture and self.currTexture != data.renderData.texture.id():
			data.renderData.texture.Bind()
			self.currTexture = data.renderData.texture.id()
		glPushMatrix()
		glTranslatex(data.position().x,data.position().y,data.position().z)
		glScalex(data.scale().x,data.scale().y,data.scale().z)
		glRotatex(data.rotation().y,0,1,0)
		glRotatex(data.rotation().x,1,0,0)
		glRotatex(data.rotation().z,0,0,1)
		glDrawElements(GL_TRIANGLES, data.renderData.numIndices, data.renderData.indexDataType, data.renderData.indices)# Draw the triangle
		glPopMatrix()


	#Draws a screen size quad with tex on it
	def draw2DQuad(self, tex):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glLoadIdentity()
		glTranslatex(0,  FTOX(-0.25), ITOX(-5))
		FaceData = [
				-FTOX(3), -ITOX(2), ITOX(0),    # First vertex position
				 FTOX(3), -ITOX(2), ITOX(0),    # Second vertex position
				-FTOX(3),  ITOX(2), ITOX(0),    # Third vertex position
				 FTOX(3),  ITOX(2), ITOX(0),    # First vertex position
				 FTOX(3), -ITOX(2), ITOX(0),    # Second vertex position
				-FTOX(3),  ITOX(2), ITOX(0)]    # Third vertex position
		TexCoordData = [
				 FTOX(0.0), FTOX(0.0),
				 FTOX(1.0), FTOX(0.0),
				 FTOX(0.0), FTOX(1.0),
				 FTOX(1.0), FTOX(1.0),
				 FTOX(1.0), FTOX(0.0),
				 FTOX(0.0), FTOX(1.0)]
		tex.bind()
		IndexData = [0, 1, 2, 5, 4, 3]
		glVertexPointer(3, GL_FIXED, 0, FaceData)  # Set the vertex (position) data source
		glTexCoordPointer(2, GL_FIXED, 0, TexCoordData)  # Set the vertex (position) data source
		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, IndexData)  # Draw the triangle
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
		self.indices = indices  # uint16*
		self.vertices = vertices  # Vector3*
		self.texCoords = uvmap
		self.texture = texture
		self.colorData = None  # Color4*
		self.indexDataType = GL_UNSIGNED_SHORT



class TexCoord2:
	def __init__(self):
		self.u = 0
		self.v = 0
