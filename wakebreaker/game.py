import pyglet
from pyglet.gl import *

from util import Vector3

import models
import renderer
import camera
import scene


G_UP, G_DOWN, G_RIGHT, G_LEFT, G_OK, G_DEVICE1, G_DEVICE2 = xrange(7)


class Game:
	def __init__(self):
		self.camera = camera.Camera()
		self.modelManager = scene.ModelManager()
		self.currentScreen = None  # The current screen texture.
		self.splash = None  # The opening screen texture.
		self.victory = None  # The victory screen texture.
		self.defeat = None  # The defeat screen texture.
		self.seascape = None  # the ocean environment
		self.racers = None  # the racers
		self.numRacers = 0
		self.raceCourse = None  # the course they race on
		self.playing = False  # are we racing
		# window dimensions
		self.keysDown = [False,]*7  # we only test for 4 keys
		self.hasWon = False  # did we win?


	def create(self):
		self.playing = False
		# seed the random number generator
		#srand((unsigned)time(None))
		# Create and initialize the OpenGL ES renderer
		self.renderer = renderer.Renderer()
		# Set up the player
		self.racers = (models.Racer(self.modelManager, scene.BOAT2),
		               models.Racer(self.modelManager, scene.BOAT1))
		# Generate the race course first
		self.raceCourse = models.RaceCourse(Vector3(models.WORLD_WIDTH / 2.0, 0.0, models.WORLD_HEIGHT / 2.0),
		                                    58, 60, self.racers, self.modelManager)
		# set up the environment
		self.seascape = models.Seascape()
		self.seascape.generate(self.modelManager)
		# put the camera at an initial positiong
		eye = Vector3(-0.0, 15.0, -59.0)
		center = Vector3(models.WORLD_WIDTH / 2.0, 0.0, models.WORLD_HEIGHT / 2.0)
		up = Vector3(0.0, 1.0, 0.0)
		self.camera.lookAt(eye, center, up)
		# Load textures:
		self.splash = pyglet.image.load('splash.png').get_texture()
		self.victory = pyglet.image.load('victory.png').get_texture()
		self.defeat = pyglet.image.load('defeat.png').get_texture()
		self.currentScreen = None
		return True


	def menu(self):
		if self.playing:
			self.tick(0)
		else:
			# If the user has won the game:
			if self.hasWon:
				self.currentScreen = self.victory
			else:
				self.currentScreen = self.defeat
			# If we should display the opening splash screen:
			if self.racers[0].currLap == 0 and self.racers[0].nextCheckPoint == 0:
				# Yaki - start playing automatically:
				self.playing = True
				self.currentScreen = self.splash
				for i in xrange(5): #FIXME:
					if self.keysDown[i]:
						self.playing = True
			self.renderer.draw2DQuad(self.currentScreen)


	def tick(self, time_elapsed):
		# clear screen
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		# set up the camera to follow the player
		eye = Vector3(self.racers[0].ri.position.x - 25.0 * self.racers[0].dir.x * 0.7,
		              7.0,
		              self.racers[0].ri.position.z - 25.0 * self.racers[0].dir.z * -0.7)
		center = self.racers[0].ri.position
		up = Vector3(0.0, 1.0, 0.0)
		self.camera.lookAt(eye, center, up)
		self.camera.update()
		# process input
		if self.keysDown[G_UP]:
			self.racers[0].increaseSpeed(0.1)
		if self.keysDown[G_DOWN]:
			self.racers[0].increaseSpeed(-0.1)
		if self.keysDown[G_RIGHT]:
			self.racers[0].rotate(-5.0)
		if self.keysDown[G_LEFT]:
			self.racers[0].rotate(5.0)
		if self.keysDown[G_DEVICE1]:
			self.renderer.EnableFog()
		if self.keysDown[G_DEVICE2]:
			self.renderer.disableFog()
		# update all major game related classes
		self.raceCourse.update()
		self.racers[0].update()
		self.racers[1].updateAI(self.racers[0])
		if self.seascape.collided(self.racers[0].ri.position, 1.0):
			self.racers[0].increaseSpeed(-1)
		if self.seascape.collided(self.racers[1].ri.position, 1.0):
			self.racers[1].increaseSpeed(-1.0)
		if self.racers[0].finished:
			self.hasWon = True
			self.playing = False
		if self.racers[1].finished:
			self.hasWon = False
			self.playing = False
		# render everything
		self.racers[0].render(self.renderer)
		self.racers[1].render(self.renderer)
		self.seascape.render(self.renderer)
		self.raceCourse.render(self.renderer)


	def keyDown(self, keyCode):
		self.keysDown[keyCode] = True


	def keyUp(self, keyCode):
		self.keysDown[keyCode] = False
