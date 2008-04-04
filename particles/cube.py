from pyglet.gl import *

def draw_task(size, pos):
	size /= 2.0
	while True:
		yield
		glDisable(GL_TEXTURE_2D)
		glPushMatrix()
		glTranslatef(*pos)
		glColor3f(1.0, 1.0, 1.0)
		glBegin(GL_LINE_LOOP)
		glVertex3f(-size, -size,  size)	 # front bottom left
		glVertex3f( size, -size,  size)	 # front bottom right
		glVertex3f( size,  size,  size)	 # front top right
		glVertex3f(-size,  size,  size)	 # front top left
		glEnd()
		glBegin(GL_LINE_LOOP)
		glVertex3f(-size, -size,  size)	 # front bottom left
		glVertex3f(-size,  size,  size)	 # front top left
		glVertex3f(-size,  size, -size)	 # back top left
		glVertex3f(-size, -size, -size)	 # back bottom left
		glEnd()
		glBegin(GL_LINE_LOOP)
		glVertex3f(-size, -size, -size)	 # back bottom left
		glVertex3f( size, -size, -size)	 # back bottom right
		glVertex3f( size,  size, -size)	 # back top right
		glVertex3f(-size,  size, -size)	 # back top left
		glEnd()
		glBegin(GL_LINE_LOOP)
		glVertex3f( size, -size,  size)	 # front bottom right
		glVertex3f( size,  size,  size)	 # front top right
		glVertex3f( size,  size, -size)	 # back top right
		glVertex3f( size, -size, -size)	 # back bottom right
		glEnd()
		glPopMatrix()
