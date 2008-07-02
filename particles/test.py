#!/usr/bin/env python

import random, math
import pygame
from pygame.locals import *
import utils

SIZE = 640

class Test(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.group)
		self.image = pygame.Surface((SIZE, SIZE))
		self.rect = self.image.get_rect()
		self.angle = 0.0
		self.vect = (0.0, 0.0, 1.0)

	def update(self):
		self.image.fill((0x00,0x40,0x00))

		end_pos = (SIZE / 2 + SIZE / 2 * self.vect[0], SIZE / 2 - SIZE / 2 * self.vect[2])
		pygame.draw.line(self.image, (0x7F,0x7F,0x7F), (SIZE/2, SIZE/2), end_pos)
		self.vect = utils.rotateVectorY(self.vect, 15.0)

		x,y,z = utils.rotateVectorY((0.0, 0.0, 0.5), self.angle)
		self.angle = self.angle + 15.0
		if self.angle >= 360.0:
			self.angle = 0.0

		end_pos = (SIZE / 2 + SIZE / 2 * x, SIZE / 2 - SIZE / 2 * z)
		pygame.draw.line(self.image, (0xFF,0xFF,0xFF), (SIZE/2, SIZE/2), end_pos)


def main():
	pygame.init()
	window = pygame.display.set_mode((SIZE, SIZE))
	screen = pygame.display.get_surface()
	clock = pygame.time.Clock()

	g = pygame.sprite.Group()
	Test.group = g
	t = Test()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				return
		clock.tick(1)
		t.update()
		g.draw(screen)
		pygame.display.flip()


if __name__ == '__main__':
	#main()

	# 480.0, 63.375 => 0.05
	#  48.0, 63.375 => 0.5
	s = math.sqrt
	p = 63.375
	def t(i):
		return (1.0/i*p)*(1.0/i*p)
	print t(480.0)
	print t(48.0)
