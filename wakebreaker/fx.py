import random
from pyglet.gl import *
from util import Vector3

class ParticleSystem:
	def __init__(self, numParticles, maxLife, pos, dir):
		# assign in the particle system properties
		self.__emitPoint = Vector3(pos)
		self.__dir = Vector3(dir)
		self.__numParticles = numParticles
		self.__maxLife = maxLife
		# build the new array of particles
		self.__particles = [Particle() for i in xrange(numParticles)]
		# initialize all the particles
		for p in self.__particles:
			self.resetParticle(p)

	# moves the emission point
	def move(self, newEmitPoint):
		self.__emitPoint.set(newEmitPoint)

	# Changes the particle system's direction
	def redirect(self, dir):
		self.__dir.set(dir)
	
	#-----------------------------------
	# Resets the particle at index
	def resetParticle(self, particle):
		# set the position
		particle.pos = self.__emitPoint
		# reset the life
		particle.life = self.__maxLife + random.uniform(-5.0, 5.0)
		# Add some variety to the velocities
		# Assign them in, alter the direction by the factor
		particle.velocity.x = random.uniform(0.0, 6.5) * self.__dir.x
		particle.velocity.y = random.uniform(0.0, 5.0) * self.__dir.y
		particle.velocity.z = random.uniform(0.0, 6.5) * self.__dir.z

	#-------------------------------
	# Draws the beast
	def render(self):
		glPushMatrix()
		# Turn of texturing, it would be too expensive
		glDisable(GL_TEXTURE_2D)
		# Attenuate the particle size based on distance
		glPointSize(8.0)
		glPointParameterfv(GL_POINT_DISTANCE_ATTENUATION, (GLfloat*3)(0.0, 0.05, 0.005))
		particles_gl = (GLfloat * len(self.__particles))(*self.__particles)
		glVertexPointer(3, GL_FLOAT, sizeof(Particle), particles_gl)
		# Draw
		glDrawArrays(GL_POINTS, 0, self.__numParticles)
		glEnable(GL_TEXTURE_2D)
		glPopMatrix()	
	
	#-------------------------------
	# Updates particle position and life, 
	# resets them if they need to be
	def update(self):
		# loop through all the particles
		for p in self.__particles:
			# decrease life
			p.life -= 1
			# check for death
			if p.life < 0:
				# revive!
				self.resetParticle(p)
			# move the particle
			p.pos.x += p.velocity.x
			p.pos.y += p.velocity.y
			p.pos.z += p.velocity.z


class Particle:
	def __init__(self):
		self.pos = Vector3()
		self.velocity = Vector3()
		self.life = 0.0


if __name__ == '__main__':
	import ctypes

	class POS(ctypes.Structure):
		_fields_ = [("x", GLfloat), ("y", GLfloat), ("z", GLfloat)]

	class Vector3(ctypes.Union):
		_fields_ = [("__pos", POS), ("vect", GLfloat*3)]
		_anonymous_ = ("__pos",)

		def __init__(self, *args):
			print type(self.vect)
			self.vect = args
			print type(self.vect)


	v = Vector3(1,2,3)
	#v2 = Vector3(v)
	v.x = 1.5
	print v.vect
