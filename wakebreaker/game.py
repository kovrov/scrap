
#include "Base.h"
#include "Texture.h"
#include "Seascape.h"

from util import Vector3

import models
import renderer
import camera
import scene

G_UP, G_DOWN, G_RIGHT, G_LEFT, G_OK, G_DEVICE1, G_DEVICE2 = xrange(7)

class Game:
	def __init__(self):
		self.renderer = renderer.Renderer()
		self.camera = camera.Camera()
		self.modelManager = scene.ModelManager()
		self.currentScrren = None  # The current screen texture.
		self.splash = None  # The opening screen texture.
		self.victory = None  # The victory screen texture.
		self.defeat = None  # The defeat screen texture.
		self.seascape = None  # the ocean environment
		self.racers = None  # the racers
		self.numRacers = 0
		self.raceCourse = None  # the course they race on
		self.playing = False  # are we racing
		# window dimensions
		self.width = 0
		self.height = 0
		self.keysDown = (False,)*7  # we only test for 4 keys
		self.hasWon = False  # did we win?


	def menu(self):
		# swap it all to the screen
		self.renderer.SwapBuffers()
		if self.playing:
			self.tick(0)
		else:
			# If the user has won the game:
			if self.hasWon:
				self.currentScrren = self.victory
			else:
				self.currentScrren = self.defeat
			# If we should display the opening splash screen:
			if (self.racers[0].CurrLap() == 0) and (self.racers[0].NextCheckPoint() == 0):
				# Yaki - start playing automatically:
				self.playing = True
				self.currentScrren = self.splash
				for i in xrange(5): #FIXME:
					if self.keysDown[i]:
						self.playing = True
			self.renderer.Draw2DQuad(self.currentScrren)


	def create(self, w, h, hWnd):
		self.playing = False
		# seed the random number generator
		#srand((unsigned)time(None))
		self.width = w
		self.height = h
		# Create and initialize the OpenGL ES renderer
		self.renderer.initialize(self.width, self.height)
		# Set up the player
		self.racers = (models.Racer(), models.Racer())
		self.racers[0].initialize(self.modelManager, scene.BOAT2)
		self.racers[1].initialize(self.modelManager, scene.BOAT1)
		# Generate the race course first
		self.raceCourse = models.RaceCourse(Vector3(models.WORLD_WIDTH / 2.0, 0.0, models.WORLD_HEIGHT / 2.0),
		                                    58, 60, self.racers, self.modelManager)
		# set up the environment
		self.seascape = Seascape()
		self.seascape.generate(self.modelManager)
		# put the camera at an initial positiong
		eye = Vector3(-ITOX(0),ITOX(15),FTOX(-59.0))
		center = Vector3(ITOX(WORLD_WIDTH / 2),0,ITOX(WORLD_HEIGHT / 2))
		up = Vector3(ITOX(0),ITOX(1),ITOX(0))
		self.camera.lookAt(eye, center, up)
		# Load textures:
		self.splash = Texture()
		if self.splash:
			self.splash.load(SPLASH)
		self.victory = Texture()
		if self.victory:
			self.victory.load(VICTORY)
		self.defeat = Texture()
		if self.defeat:
			self.defeat.load(DEFEAT)
		self.currentScrren = None
		return True


	def destroy(self):
		SAFE_DELETE(self.raceCourse)
		SAFE_ARRAY_DELETE(self.racers)
		SAFE_DELETE(self.seascape)
		self.currentScrren = None
		SAFE_DELETE(self.splash)
		SAFE_DELETE(self.victory)
		SAFE_DELETE(self.defeat)
		self.renderer.destroy()


	def tick(self, time_elapsed):
		# clear screen
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		# set up the camera to follow the player
		eye = Vector3(self.racers[0].Position().x - (MULX(ITOX(25), MULX(self.racers[0].dir.x,FTOX(0.7))  )),
					ITOX(7),
					self.racers[0].Position().z - (MULX(ITOX(25),-MULX(self.racers[0].dir.z,FTOX(0.7)) )))
		up = Vector3(ITOX(0),ITOX(1),ITOX(0))
		self.camera.LookAt(eye,self.racers[0].Position(),up)
		self.camera.Update()
		# process input
		if self.keysDown[G_UP] == True:
			self.racers[0].IncreaseSpeed(6553)		
		if self.keysDown[G_DOWN] == True:
			self.racers[0].IncreaseSpeed(-6553)		
		if self.keysDown[G_RIGHT] == True:
			self.racers[0].rotate(-ITOX(5))
		if self.keysDown[G_LEFT] == True:
			self.racers[0].rotate(ITOX(5))
		if self.keysDown[G_DEVICE1]:
			self.renderer.EnableFog()
		if self.keysDown[G_DEVICE2]:
			self.renderer.DisableFog()
		# update all major game related classes
		self.raceCourse.update()
		self.racers[0].update()
		self.racers[1].updateAI(self.racers[0])
		if self.seascape.Collided(self.racers[0].ri.position(),ITOX(1)):
			self.racers[0].IncreaseSpeed(-ITOX(1))
		if self.seascape.Collided(self.racers[1].ri.position(),ITOX(1)):
			self.racers[1].IncreaseSpeed(-ITOX(1))
		if self.racers[0].IsFinished():
			self.hasWon = True
			self.playing = False
		if self.racers[1].IsFinished():
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
