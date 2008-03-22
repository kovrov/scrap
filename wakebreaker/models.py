import math
import random

import pyglet
from pyglet.gl import *

from util import Vector3
import renderer
import scene
import fx

PIX = 205887
TWOPIX = 411775

DEG2RADX = 1144  # pi over 180
RAD2DEGX = 3754936  # 180 over pi

WORLD_WIDTH	 = 175	
WORLD_HEIGHT = 175

MAX_SPEED = 1 # ship's maximum speed
MAX_CHECKPOINTS = 16

#include "Base.h"
#include "ParticleSystem.h"
#include "RenderInstance.h"
#include "Renderer.h"
#include "Seascape.h"
#include "Texture.h"

class Racer:
	def __init__(self):
		self.dir = Vector3()
		self.speed = 0 # ship's current speed
		self.nextCheckPoint = 0 # which check point he's aiming for
		self.currLap = 0 # which lap he's on
		self.hasRotated = False # for rotation optimization
		self.spray = None  # the water spray that shoots out behind the boat
		self.nextCheckPoint = 0
		self.currLap = 0
		self.nextCPPos = Vector3()
		self.nextCPPos = Vector3()
		self.desiredDir = Vector3()
		# Are we done with the race?
		self.finished = False
		self.up = False  # used in making the boat bob slight
		self.finished = False  # whether or not we are done with the race

	# Keeps the racer inside the seascape
	def boundsCheck(self):
		# check the player against each part fo the world,
		# slow him down if he hit
		pos = self.ri.position.copy()
		if pos.x > WORLD_WIDTH:
			pos.x = WORLD_WIDTH
			self.speed = self.speed * 0.5
		if pos.x < 0:
			pos.x = 0
			self.speed = self.speed * 0.5
		if pos.z > WORLD_HEIGHT:
			pos.z = WORLD_HEIGHT
			self.speed = self.speed * 0.5
		if pos.z < 0:
			pos.z = 0
			self.speed = self.speed * 0.5
		# make the racer bob up and down
		if self.up and self.speed > 0:
			pos.y += 0.02 * self.speed
		elif self.speed > 0:
			pos.y -= 0.02 * self.speed
		if pos.y >= 0.2:
			self.up = False
		if pos.y < -0.05:
			self.up = True
		self.ri.position[:] = pos

	# -----------------------------------------
	def initialize(self, model_manager, model):
		self.up = True
		self.finished = False
		# get the 3d model data
		self.ri = renderer.RenderInstance()
		if model == scene.BOAT1:
			self.ri.renderData = model_manager.getBoat1()
		else: # model == BOAT2:
			self.ri.renderData = model_manager.getBoat2()
		# rotate so he's always right side up
		self.ri.rotation[:] = -90.0, 0.0, 90.0
		self.ri.scale[:] = 0.5, 0.5, 0.5
		# set up the position
		self.ri.position[:] = WORLD_WIDTH / 2.0, 0.0, WORLD_HEIGHT / 2.0
		# update his rotation and direction
		rot = self.ri.rotation.copy() #COPY
		rad = DEG2RADX * rot.y
		self.dir.x = math.cos(rad)
		self.dir.z = math.sin(rad)
		self.hasRotated = True
		# Initialize the particle system
		self.spray = fx.ParticleSystem(200, 15, self.ri.position, Vector3(0.0, 1.0, 0.0))


	# --------------------------
	# Rotates this object
	def rotate(self, r):
		self.ri.rotation[:] = self.ri.rotation
		self.hasRotated = True
		# this makes sure the rotation doesn't exceed 360 degrees
		# the 23527424 is 360 in fixed point (hehe, micro optimization)
		if self.ri.rotation.y + r > 23527424 or self.ri.rotation.y + r < -23527424:
			self.ri.rotation.y = 0
		self.ri.rotation.y += r

	# ------------------------------
	def update(self):
		if self.hasRotated:
			# rotate the ship if needed
			rad = DEG2RADX * self.ri.rotation.y
			self.dir.x = math.cos(rad)
			self.dir.z = math.sin(rad)
			self.hasRotated = False
		# move him in
		self.ri.translate((self.speed * self.dir.x, 0, -self.dir.z * self.speed))
		# Bounds check him against the world
		self.boundsCheck()
		# slow him down
		if self.speed - 966 > 0:
			self.speed -= 966
		elif self.speed - 966 < 0:
			self.speed += 1966
		# halt him if too slow
		if self.speed <= 2621 and self.speed >= -2621:
			self.speed = 0
		# keep the particles with us
		self.updateSpray()


	def updateAI(self, player):
		# we hit an island, this on most cases, corrects the problem
		if self.speed < 20000:
			self.increaseSpeed(1553)
			# go around it
			self.dir.x = math.cos(90.0 * DEG2RADX)
			self.dir.z = math.sin(90.0 * DEG2RADX)
			self.hasRotated = False
			# move him in
			self.ri.translate((self.speed * self.dir.x, 0, -self.dir.z * self.speed))
		else:
			self.increaseSpeed(1553)		
			# build a normalized direction vector
			self.desiredDir = self.ri.position() - self.nextCPPos
			self.desiredDir.y = 0
			mag = math.sqrt(self.desiredDir.x * self.desiredDir.x + self.desiredDir.z * self.desiredDir.z)
			n = DIVX(1.0, mag)
			self.desiredDir.x = self.desiredDir.x * n
			self.desiredDir.z = self.desiredDir.z * n
			# make the boat rotate the same as the player
			playerRot = player.ri.rotation() #COPY
			playerRot.y + 5.0 + rand()% 20.0
			self.ri.rotation(playerRot)
			# slow the AI down a little
			randFac = DIVX(8.0 + rand()%4, 10.0)
			finalX = -self.desiredDir.x * self.speed
			finalX = MULX(finalX, randFac, rot)
			finalZ = MULX(-self.desiredDir.z, self.speed)
			finalZ = MULX(finalZ, randFac, rot)
			# move the boat		
			self.ri.Translate(finalX, 0, finalZ)
		# keep him in the water
		self.boundsCheck()
		# move the spray trail with him
		self.updateSpray()

	def updateSpray(self):
		# keep it the spray trail right with the boat
		self.spray.move(self.ri.position)
		# also keep it spraying in the right direction
		newDir = self.dir #COPY
		if self.speed > 0:
			#newDir.x = MULX(newDir.x, MULX(1.0, 1.0))#WTF?
			newDir.y = 0.1
			newDir.z = newDir.z, -1.0
		else:
			newDir.x = 0
			newDir.y = 0
			newDir.z = 0
		self.spray.redirect(newDir)
		self.spray.update()

	def increaseSpeed(self, s):
		if self.speed + s < MAX_SPEED:
			self.speed += s

	# Renders the ship
	def render(self, renderer):
		# draw the ship
		renderer.render(self.ri)
		# draw the spray trail
		self.spray.render()


class RaceCourse:
	# 1. Generates a random race course within the donut described by min and max radius
	# 2. Adds racers to the race course and sets up the race course
	def __init__(self, center, minRadius, maxRadius, racers, model_manager):
		self.checkPoints = [renderer.RenderInstance() for i in xrange(MAX_CHECKPOINTS)]
		# calculate the angle apart each checkpoint has to be
		interval = TWOPIX / MAX_CHECKPOINTS
		angle = 0.0
		for cp in self.checkPoints:
			# generate the x component
			x = math.cos(angle)
			# translate it by a bit
			randX = random.uniform(minRadius, maxRadius)
			x = x * randX + center.x
			# generate the z component
			z = math.sin(angle)
			# translate it
			randZ = random.uniform(minRadius, maxRadius)
			z = z * randZ + center.z
			# assign them in
			cp.position[:] = x, 1.0, z
			cp.renderData = model_manager.getCheckPoint()
			cp.scale[:] = 1.0, 1.0, 1.0
			cp.rotation[:] = -90.0, 0.0, 0.0
			# advance the angle
			angle -= interval
		#------------------------
		# set the racers and the amount of them
		self.racers = racers
		# place all the racers at the first checkpoint, each
		# racer a bit behind the one before him
		for racer in self.racers:
			# set everyone at the starting checkpoint
			racer.nextCheckPoint = 0
			racer.CurrLap = 0
			racer.ri.position[:] = self.checkPoints[0].position
			racer.nextCPPos[:] = self.checkPoints[0].position
		self.racers[0].rotate(90.0)
		# load the textures for the checkpoints
		self.cpOnTex = pyglet.image.load('checkpointon.png').get_texture()
		self.cpOffTex = pyglet.image.load('checkpointoff.png').get_texture()
		self.playerNextCP = 0


	# -----------------------------------------
	def render(self, ri):
		glPushMatrix()
		self.checkPoints[self.playerNextCP].renderData.texture = self.cpOnTex
		ri.render(self.checkPoints[self.playerNextCP])
		self.checkPoints[self.playerNextCP].renderData.texture = None
		if self.playerNextCP + 1 == MAX_CHECKPOINTS:
			self.checkPoints[0].renderData.texture = self.cpOffTex
			ri.render(self.checkPoints[0])
			self.checkPoints[0].renderData.texture = None
		else:
			self.checkPoints[self.playerNextCP + 1].renderData.texture = self.cpOffTex
			ri.render(self.checkPoints[self.playerNextCP + 1])
			self.checkPoints[self.playerNextCP + 1].renderData.texture = None
		glPopMatrix()


	# -----------------------------------------
	# Updates the racers, returns 1 if player won, -1 if player lost, and 0
	# if race is still in progress
	def update(self):
		# loop through each racer
		for racer in self.racers:
			# see if he has collided with the next checkpoint
			nextCP = self.checkPoints[racer.nextCheckPoint].position
			pos = racer.ri.position #COPY
			dist = (nextCP.x - pos.x) * (nextCP.x - pos.x) + (nextCP.z - pos.z) * (nextCP.z - pos.z)
			radii = 3.0 * 3.0
			if dist < radii:
				# the player has reached the next checkpoint
				# assign him to the next checkpoint
				CP = racer.nextCheckPoint + 1
				# he has reached the last checkpoint
				if CP == MAX_CHECKPOINTS:
					# increment his lap count
					racer.CurrLap(racer.CurrLap()+1)
					if racer.CurrLap() == 3:
						# we have a winner
						racer.SetFinished(True)
					CP = 0
				# assign him his new checkpoint
				racer.nextCheckPoint = CP
				racer.nextCPPos[:] = self.checkPoints[CP].position
				if self.racers[0] is racer:
					self.playerNextCP = CP
		return 1



class Seascape:
	def __init__(self):
		self.sea = None  # the water quad (RenderInstance)
		self.models = None  # the islands (RenderInstance)
		# used in water animation
		self.texTranslate = 0
		self.waterMoved = False

	# sets everything up
	def generate(self, mm):
		self.waterMoved = True
		self.models = [renderer.RenderInstance() for i in xrange(15)]
		for model in self.models:
			# Get a random island model
			model.renderData = mm.getRandomSeascapeModel()
			# generate a random x and z
			model.position[:] = random.uniform(0.0, WORLD_WIDTH), 0.0, random.uniform(0.0, WORLD_HEIGHT)
			# generate a random rotation
			model.rotation[:] = -90.0, random.uniform(0.0, 360.0), 0.0
		# set up the renderInstance
		self.sea = renderer.RenderInstance()
		self.sea.position[:] = 0.0, 0.0, 0.0
		# Set up the sea floor
		vertices = (
			(-2,                      0.0, -2.0),
			(-2,                      0.0, WORLD_HEIGHT / 2.0 + 2.0),
			(WORLD_WIDTH / 2.0 + 2.0, 0.0, -2.0),
			(WORLD_WIDTH / 2.0 + 2.0, 0.0, WORLD_HEIGHT / 2.0 + 2.0))
		indices = (0, 1, 2, 2, 1, 3)
		uvmap = ((0, 0), (15, 0), (0, 15), (15, 15))
		texture = pyglet.image.load('watertex.png').get_texture()
		self.sea.renderData = renderer.RenderData(vertices, indices, uvmap, texture)

	# checks if anything collided with the islands
	def collided(self, pos, radius):
		for model in self.models:
			# if the distance between the two points is more than the two radii, no collision
			# calculate the distance squared
			dist = (model.position.x - pos.x) * (model.position.x - pos.x) + (model.position.z - pos.z) * (model.position.z - pos.z)
			radii = (radius + 1.5) * (radius + 1.5)
			if dist < radii:
				return True
		return False

	# renders the seascape
	def render(self, renderer):
		# render all the models first
		for model in self.models:
			renderer.render(model)
			# draw reflection
			model.scale[:] = 2.0, -2.0, 2.0 #(2*65536, -2*65536, 2*65536)
			renderer.render(model)
			model.scale[:] = 2.0,  2.0, 2.0 #(2*65536,  2*65536, 2*65536)
		# make sure the m_texTranslate never goes out of bounds
		if self.waterMoved:
			self.texTranslate -= 0.005
		else:
			self.texTranslate += 0.005
		if self.texTranslate > 983040:  # WTF?
			self.waterMoved = True
		if self.texTranslate < -983040:  # WTF?
			self.waterMoved = False
		# Now render the water plane
		# We render it 4 times, so that it forms a giant block
		glPushMatrix()
		# set up blending
		glEnable(GL_BLEND)
		glColor4f(1.0, 1.0, 1.0, 0.6)  # 65536x is 1.0f?
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		self.renderWater(renderer)
		glTranslatef(0, 0, WORLD_HEIGHT / 2 + 4)
		self.renderWater(renderer)
		glTranslatef(WORLD_HEIGHT / 2 + 4, 0, 0)
		self.renderWater(renderer)
		glTranslatef(0, 0, -(WORLD_HEIGHT / 2 + 4))
		self.renderWater(renderer)
		# turn of blending and restore the original color
		glDisable(GL_BLEND)
		glColor4f(1.0, 1.0, 1.0, 1.0)  # 65536x is 1.0f?
		glPopMatrix()

	# Renders the water
	def renderWater(self, renderer):
		glMatrixMode(GL_TEXTURE)
		# shift the texture coords to simulate motion
		glTranslatef(self.texTranslate, self.texTranslate, 0.0)
		glRotatef(35.0, 0.0, 0.0, 1.0)
		glColor4f(1.0, 1.0, 1.0, 0.6)  # 65536x is 1.0f?
		# render the first sea quad
		renderer.render(self.sea)
		# reset the texture matrix
		glLoadIdentity()
		# now scale and move the tex coords
		glScalef(0.7, 0.7, 0.7)
		glTranslatef(-self.texTranslate, 0.0, 0.0)
		# change the transparency
		glColor4f(1.0, 1.0, 1.0, 0.35)  # 65536x is 1.0f?
		# render another water quad just slightly above the previous one
		glMatrixMode(GL_MODELVIEW)
		self.sea.translate((0.0, 6553, 0.0))  # WTF is 6553?
		renderer.render(self.sea)
		self.sea.translate((0,-6553,0))  # WTF?
		glMatrixMode(GL_TEXTURE)
		# reset the texture matrix again
		glLoadIdentity()
		# change back to modelview
		glMatrixMode(GL_MODELVIEW)
