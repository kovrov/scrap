import random
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
		for i in xrange(numParticles):
			self.resetParticle(i)

	# moves the emission point
	def move(self, newEmitPoint):
		self.__emitPoint.set(newEmitPoint)

	# Changes the particle system's direction
	def redirect(self, dir):
		self.__dir.set(dir)
	
	#-----------------------------------
	# Resets the particle at index
	def resetParticle(self, index):
		p = self.__particles[index]
		# set the position
		p.pos = self.__emitPoint
		# reset the life
		p.life = self.__maxLife + random.randint(-5, 5)
		# Add some variety to the velocities
		factorX = random.uniform(0, 10) / 1.5
		factorY = random.uniform(0, 10) / 2.0
		factorZ = random.uniform(0, 10) / 1.5
		# Assign them in, alter the direction by the factor
		p.velocity.x = factorX * self.__dir.x
		p.velocity.y = factorY * self.__dir.y
		p.velocity.z = factorZ * self.__dir.z

	#-------------------------------
	# Draws the beast
	def render(self):
		glPushMatrix()
		# Turn of texturing, it would be too expensive
		glDisable(GL_TEXTURE_2D)
		# Attenuate the particle size based on distance
		glPointSizef(8.0)
		coefficients = (0.0, 0.05, 0.005)
		glPointParameterxv(GL_POINT_DISTANCE_ATTENUATION, coefficients)
		glVertexPointer(3, GL_FIXED, sizeof(Particle), self.__particles[0].pos.v)
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
			p[i].life -= 1
			# check for death
			if p[i].life < 0:
				# revive!
				self.resetParticle(i)
			# move the particle
			p[i].pos.x += p[i].velocity.x
			p[i].pos.y += p[i].velocity.y
			p[i].pos.z += p[i].velocity.z


class Particle:
	def __init__(self):
		self.pos = Vector3()
		self.velocity = Vector3()
		self.life = 0.0
