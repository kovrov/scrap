import renderer
#include "island1.h"
#include "island2.h"
#include "ModelManager.h"
#include "Texture.h"
#include "boat2.h"
#include "boat1.h"
#include "checkpoint.h"

import data

BOAT1, BOAT2 = xrange(2)

class Info:
	def __init__(self):
		self.mm = None  # ModelManager
		self.math = None  # Math



class ModelManager:
	def __init__(self):
		self.boat1 = None
		self.boat2 = None
		self.chest = None
		self.island1 = None
		self.island2 = None
		self.checkPoint = None

	# These return RenderData's with the requested model

	def getIsland1(self):
		if not self.island1:
			tex = Texture()
			tex.load(ISLAND1)
			self.island1 = Getisland1()
			self.island1.texture = tex
		return self.island1


	def getIsland2(self):
		if not self.island2:
			tex = Texture()
			tex.load(ISLAND2)
			self.island2 = Getisland2()
			self.island2.texture = tex
		return self.island2;


	def getBoat2(self):
		if not self.boat2:
			d = data.loadBoat2()
			self.boat2 = renderer.RenderData(d['vertices'], d['indices'], d['uvmap'], d['texture'])
		return self.boat2


	def getBoat1(self):
		if not self.boat1:
			d = data.loadBoat1()
			self.boat1 = renderer.RenderData(d['vertices'], d['indices'], d['uvmap'], d['texture'])
		return self.boat1


	def getRandomSeascapeModel(self):
		# Generate a random number
		if rand() % 2:
			return self.getIsland1()
		else:
			return self.getIsland2()


	def getCheckPoint(self):
		if not self.checkPoint:
			self.checkPoint = getcheckpoint() #WTF?
		return self.checkPoint
