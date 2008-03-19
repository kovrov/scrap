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
		particle.life = self.__maxLife + random.randint(-5, 5)
		# Add some variety to the velocities
		factorX = random.uniform(0, 10) / 1.5
		factorY = random.uniform(0, 10) / 2.0
		factorZ = random.uniform(0, 10) / 1.5
		# Assign them in, alter the direction by the factor
		particle.velocity.x = factorX * self.__dir.x
		particle.velocity.y = factorY * self.__dir.y
		particle.velocity.z = factorZ * self.__dir.z

	#-------------------------------
	# Draws the beast
	def render(self):
		glPushMatrix()
		# Turn of texturing, it would be too expensive
		glDisable(GL_TEXTURE_2D)
		# Attenuate the particle size based on distance
		glPointSize(8.0)
		glPointParameterfv(GL_POINT_DISTANCE_ATTENUATION, (GLfloat*3)(0.0, 0.05, 0.005))
		(GLfloat * len(self.__particles))(*self.__particles)
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
