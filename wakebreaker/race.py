from copy import copy
from util import Vector3

import renderer
import scene

MAX_SPEED = 1 # ship's maximum speed
MAX_CHECKPOINTS = 16

#include "Base.h"
#include "Info.h"
#include "Math.h"
#include "ParticleSystem.h"
#include "RaceCourse.h"
#include "Racer.h"
#include "RenderInstance.h"
#include "Renderer.h"
#include "Seascape.h"
#include "Texture.h"
#include "Vector3.h"
#include "renderer.h"

class Racer:
	def __init__(self):
		self.speed = 0 # ship's current speed
		self.info = None  # info class containing a math and modelmanager pointer
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
		pos = self.ri.position() #COPY
		if pos.x > ITOX(WORLD_WIDTH):
			pos.x = ITOX(WORLD_WIDTH)
			self.speed = MULX(self.speed, FTOX(0.5))
		if pos.x < 0:
			pos.x = 0
			self.speed = MULX(self.speed, FTOX(0.5))
		if pos.z > ITOX(WORLD_HEIGHT):
			pos.z = ITOX(WORLD_HEIGHT)
			self.speed = MULX(self.speed, FTOX(0.5))
		if pos.z < 0:
			pos.z = 0
			self.speed = MULX(self.speed, FTOX(0.5))
		# make the racer bob up and down
		if self.up and self.speed > 0:
			pos.y += MULX(FTOX(0.02), self.speed)
		elif self.speed > 0:
			pos.y -= MULX(FTOX(0.02), self.speed)
		if pos.y >= FTOX(0.2):
			self.up = False
		if pos.y < FTOX(-0.05):
			self.up = True
		self.ri.position(pos)

	# -----------------------------------------
	def initialize(self, info, model):
		self.up = True
		self.finished = False
		# get the 3d model data
		self.info = info
		self.ri = renderer.RenderInstance()
		if model == scene.BOAT1:
			self.ri.renderData(info.mm.getBoat1())
		else: # model == BOAT2:
			self.ri.renderData(info.mm.getBoat2())
		# rotate so he's always right side up
		vec = Vector3(-ITOX(90), 0, ITOX(90))
		self.ri.rotation(vec)
		self.ri.scale(FTOX(0.5), FTOX(0.5), FTOX(0.5))
		# set up the position
		self.ri.position(FTOX(WORLD_WIDTH / 2), 0, FTOX(WORLD_HEIGHT / 2))
		# update his rotation and direction
		rot = self.ri.rotation() #COPY
		rad = MULX(DEG2RADX, rot.y)
		self.dir.x = info.math.fcosf(rad)
		self.dir.z = info.math.fsinf(rad)
		self.hasRotated = True
		# Initialize the particle system
		self.spray = ParticleSystem()
		self.spray.initialize(200, 15, self.ri.position(), Vector3(ITOX(0), ITOX(1), ITOX(0)))


	# --------------------------
	# Rotates this object
	def rotate(self, r):
		vec = self.ri.rotation() #COPY
		# this makes sure the rotation doesn't exceed 360 degrees
		# the 23527424 is 360 in fixed point (hehe, micro optimization)
		if vec.y + r > 23527424 or vec.y + r < -23527424:
			vec.y = 0
		vec.y += r
		self.ri.rotation(vec)
		self.hasRotated = True

	# ------------------------------
	def update(self, math):
		if self.hasRotated:
			# rotate the ship if needed
			rot = self.ri.rotation() #COPY
			rad = MULX(DEG2RADX, rot.y)
			self.dir.x = math.fcosf(rad)
			self.dir.z = math.fsinf(rad)
			self.hasRotated = False
		# move him in
		self.ri.Translate(MULX(self.speed, self.dir.x), 0, MULX(-self.dir.z, self.speed))
		# Bounds check him against the world
		BoundsCheck()
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


	def updateAI(self, math, player):
		# we hit an island, this on most cases, corrects the problem
		if self.speed < 20000:
			IncreaseSpeed(1553)
			# go around it
			self.dir.x = math.fcosf(MULX(ITOX(90), DEG2RADX))
			self.dir.z = math.fsinf(MULX(ITOX(90), DEG2RADX))
			self.hasRotated = False
			# move him in
			self.ri.Translate(MULX(self.speed, self.dir.x), 0, MULX(-self.dir.z, self.speed))
		else:
			IncreaseSpeed(1553)		
			# build a normalized direction vector
			self.desiredDir = self.ri.position() - self.nextCPPos
			self.desiredDir.y = 0
			mag = sqrtx(int(MULX(self.desiredDir.x, self.desiredDir.x) + int(MULX(self.desiredDir.z, self.desiredDir.z))))
			n = DIVX(ITOX(1), mag)
			self.desiredDir.x = MULX(self.desiredDir.x, n)
			self.desiredDir.z = MULX(self.desiredDir.z, n)
			# make the boat rotate the same as the player
			playerRot = player.ri.rotation() #COPY
			playerRot.y + ITOX(5) + rand()%ITOX(20)
			self.ri.rotation(playerRot)
			# slow the AI down a little
			randFac = DIVX(ITOX(8) + rand()%4, ITOX(10))
			finalX = MULX(-self.desiredDir.x, self.speed)
			finalX = MULX(finalX, randFac, rot)
			finalZ = MULX(-self.desiredDir.z, self.speed)
			finalZ = MULX(finalZ, randFac, rot)
			# move the boat		
			self.ri.Translate(finalX, 0, finalZ)
		# keep him in the water
		BoundsCheck()
		# move the spray trail with him
		self.updateSpray()

	def updateSpray(self):
		# keep it the spray trail right with the boat
		self.spray.Move(self.ri.position())
		# also keep it spraying in the right direction
		newDir = self.dir #COPY
		if self.speed > 0:
			newDir.x = MULX(newDir.x, MULX(FTOX(1), FTOX(1)))
			newDir.y = FTOX(0.1)
			newDir.z = MULX(newDir.z, MULX(-FTOX(1), FTOX(1)))
		else:
			newDir.x = 0
			newDir.y = 0
			newDir.z = 0
		self.spray.Redirect(newDir)
		self.spray.Update()




class RaceCourse:
	def __init__(self):
		self.racers = None  # the racers
		self.numRacers = 0 # number of racers
		self.checkPoints = None  # checkpoints
		self.cpOnTex = None
		self.cpOffTex = None  # the on and off checkpoint textures
		self.playerNextCP = 0  # the player's destination checkpoint

	# Adds racers to the race course and sets up the race course
	def initialize(self, racers, numRacers):
		# set the racers and the amount of them
		self.numRacers = numRacers
		self.racers = racers
		# place all the racers at the first checkpoint, each
		# racer a bit behind the one before him
		for i in xrange(self.numRacers):
			# set everyone at the starting checkpoint
			self.racers[i].NextCheckPoint(0)
			self.racers[i].CurrLap(0)
			startPos = Vector3(self.checkPoints[0].position())
			self.racers[i].ri.position(startPos)
			self.racers[i].NextCPPos(startPos)
		self.racers[0].Rotate(ITOX(90))
		# load the textures for the checkpoints
		self.cpOnTex = Texture()
		self.cpOnTex.Load(CHECKPOINTON)
		self.cpOffTex = Texture()
		self.cpOffTex.Load(CHECKPOINTOFF)
		self.playerNextCP = 0

	# -------------------------------------------------------------------
	# Generates a random race course within the donut described by min and max radius
	def generate(self, center, minRadius, maxRadius, info):
		# allocate space for the checkpoints
		self.checkPoints = [RenderInstance() for i in xrange(MAX_CHECKPOINTS)]
		# calculate the angle apart each checkpoint has to be
		interval = DIVX( TWOPIX , ITOX(MAX_CHECKPOINTS) )
		angle = 0
		for i in xrange(MAX_CHECKPOINTS):
			# generate the x component
			x = info.math.fcosf(angle)
			# translate it by a bit
			randX = (rand()%(maxRadius - minRadius)) + minRadius
			x = MULX(x, ITOX(randX)) + center.x
			# generate the z component
			z = info.math.fsinf(angle)
			# translate it
			randZ = (rand()%(maxRadius - minRadius)) + minRadius
			z = MULX(z, ITOX(randZ)) + center.z
			# assign them in
			self.checkPoints[i].position(x, ITOX(1), z)
			self.checkPoints[i].renderData(info.mm.GetCheckPoint())
			self.checkPoints[i].scale(ITOX(1), ITOX(1), ITOX(1))
			rot = Vector3(FTOX(-90), 0, 0)
			self.checkPoints[i].rotation(rot)
			# advance the angle
			angle -= interval

	# -----------------------------------------
	def render(self, renderer):
		glPushMatrix()
		self.checkPoints[self.playerNextCP].renderData().texture = self.cpOnTex
		renderer.Render(self.checkPoints[self.playerNextCP])
		self.checkPoints[self.playerNextCP].renderData().texture = None
		if self.playerNextCP + 1 == MAX_CHECKPOINTS:
			self.checkPoints[0].renderData().texture = self.cpOffTex
			renderer.Render(self.checkPoints[0])
			self.checkPoints[0].renderData().texture = None
		else:
			self.checkPoints[self.playerNextCP + 1].renderData().texture = self.cpOffTex
			renderer.Render(self.checkPoints[self.playerNextCP + 1])
			self.checkPoints[self.playerNextCP + 1].renderData().texture = None
		glPopMatrix()


	# -----------------------------------------
	# Updates the racers, returns 1 if player won, -1 if player lost, and 0
	# if race is still in progress
	def update(self):
		# loop through each racer
		for i in xrange(self.numRacers):
			# see if he has collided with the next checkpoint
			nextCP = self.checkPoints[self.racers[i].NextCheckPoint()].position() #COPY
			pos = self.racers[i].ri.position() #COPY
			dist = MULX( (nextCP.x - pos.x), (nextCP.x - pos.x) ) + MULX( (nextCP.z - pos.z), (nextCP.z - pos.z) )
			radii = MULX(ITOX(3), ITOX(3))
			if dist < radii:
				# the player has reached the next checkpoint
				# assign him to the next checkpoint
				CP = self.racers[i].NextCheckPoint() + 1
				# he has reached the last checkpoint
				if CP == MAX_CHECKPOINTS:
					# increment his lap count
					self.racers[i].CurrLap(self.racers[i].CurrLap()+1)
					if self.racers[i].CurrLap() == 3:
						# we have a winner
						self.racers[i].SetFinished(True)
					CP = 0
				# assign him his new checkpoint
				self.racers[i].NextCheckPoint(CP)
				self.racers[i].NextCPPos(self.checkPoints[CP].position())
				if i == 0:
					self.playerNextCP = CP
		return 1
