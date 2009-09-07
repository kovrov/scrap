#!/usr/bin/python

import random
import pyglet
from pyglet.gl import *

class Slot:
	def __init__(self, pos):
		self.pos = pos
		self.tile = None

def blockify(slots):
	for slot in slots:
		x,y,z = slot.pos
		slot.above_blockers = tuple(i for i in slots if i.pos in ((x, y, z+1), (x, y+1, z+1), (x, y-1, z+1),
		                                                          (x-1, y, z+1), (x-1, y+1, z+1), (x-1, y-1, z+1),
		                                                          (x+1, y, z+1), (x+1, y+1, z+1), (x+1, y-1, z+1)))
		slot.left_blockers  = tuple(i for i in slots if i.pos in ((x-2, y, z), (x-2, y-1, z), (x-2, y+1, z)))
		slot.right_blockers = tuple(i for i in slots if i.pos in ((x+2, y, z), (x+2, y-1, z), (x+2, y+1, z)))
	return slots

layouts = {'dragon': blockify(tuple(Slot(i) for i in (
		(24, 14, 0), (22, 14, 0), (20, 14, 0), (18, 14, 0), (16, 14, 0), (14, 14, 0), (12, 14, 0), (10, 14, 0),
		( 8, 14, 0), ( 6, 14, 0), ( 4, 14, 0), ( 2, 14, 0), (20, 12, 0), (18, 12, 0), (16, 12, 0), (14, 12, 0),
		(12, 12, 0), (10, 12, 0), ( 8, 12, 0), ( 6, 12, 0), (22, 10, 0), (20, 10, 0), (18, 10, 0), (16, 10, 0),
		(14, 10, 0), (12, 10, 0), (10, 10, 0), ( 8, 10, 0), ( 6, 10, 0), ( 4, 10, 0), (28,  7, 0), (26,  7, 0),
		(24,  8, 0), (22,  8, 0), (20,  8, 0), (18,  8, 0), (16,  8, 0), (14,  8, 0), (12,  8, 0), (10,  8, 0),
		( 8,  8, 0), ( 6,  8, 0), ( 4,  8, 0), ( 2,  8, 0), (24,  6, 0), (22,  6, 0), (20,  6, 0), (18,  6, 0),
		(16,  6, 0), (14,  6, 0), (12,  6, 0), (10,  6, 0), ( 8,  6, 0), ( 6,  6, 0), ( 4,  6, 0), ( 2,  6, 0),
		( 0,  7, 0), (22,  4, 0), (20,  4, 0), (18,  4, 0), (16,  4, 0), (14,  4, 0), (12,  4, 0), (10,  4, 0),
		( 8,  4, 0), ( 6,  4, 0), ( 4,  4, 0), (20,  2, 0), (18,  2, 0), (16,  2, 0), (14,  2, 0), (12,  2, 0),
		(10,  2, 0), ( 8,  2, 0), ( 6,  2, 0), (24,  0, 0), (22,  0, 0), (20,  0, 0), (18,  0, 0), (16,  0, 0),
		(14,  0, 0), (12,  0, 0), (10,  0, 0), (8,   0, 0), ( 6,  0, 0), ( 4,  0, 0), ( 2,  0, 0), (18, 12, 1),
		(16, 12, 1), (14, 12, 1), (12, 12, 1), (10, 12, 1), ( 8, 12, 1), (18, 10, 1), (16, 10, 1), (14, 10, 1),
		(12, 10, 1), (10, 10, 1), ( 8, 10, 1), (18,  8, 1), (16,  8, 1), (14,  8, 1), (12,  8, 1), (10,  8, 1),
		( 8,  8, 1), (18,  6, 1), (16,  6, 1), (14,  6, 1), (12,  6, 1), (10,  6, 1), ( 8,  6, 1), (18,  4, 1),
		(16,  4, 1), (14,  4, 1), (12,  4, 1), (10,  4, 1), ( 8,  4, 1), (18,  2, 1), (16,  2, 1), (14,  2, 1),
		(12,  2, 1), (10,  2, 1), ( 8,  2, 1), (16, 10, 2), (14, 10, 2), (12, 10, 2), (10, 10, 2), (16,  8, 2),
		(14,  8, 2), (12,  8, 2), (10,  8, 2), (16,  6, 2), (14,  6, 2), (12,  6, 2), (10,  6, 2), (16,  4, 2),
		(14,  4, 2), (12,  4, 2), (10,  4, 2), (14,  8, 3), (12,  8, 3), (14,  6, 3), (12,  6, 3), (13,  7, 4)))),}

board = layouts['dragon']

pyglet.resource.path.append('res')
pyglet.resource.reindex()
background_board = pyglet.resource.image('Background_board.jpg')
tiles_normal = pyglet.resource.image('tiles_normal.png')
tiles_normal_seq = pyglet.image.ImageGrid(tiles_normal, 6, 7)
tiles_tex_grid = pyglet.image.TextureGrid(tiles_normal_seq)
off = 8  # "height offset" value - hardcoded into bitmap

#       ball tiles,             bamboo tiles,            characters tiles,         seasons tiles,          wind tiles,               flowers tiles,          dragons tiles
tiles = tiles_tex_grid[0:9]*4 + tiles_tex_grid[9:18]*4 + tiles_tex_grid[18:27]*4 + tiles_tex_grid[27:31] + tiles_tex_grid[31:35]*4 + tiles_tex_grid[35:39] + tiles_tex_grid[39:42]*4
random.shuffle(tiles)
for i in range(len(board)):
	board[i].tile = tiles[i]

window = pyglet.window.Window((tiles_tex_grid.item_width-off) * 16, (tiles_tex_grid.item_height-off) * 9)  # 16x9 tiles
@window.event
def on_draw():
	background_board.blit(0, 0)
	for i in board:
		if i.tile is None:
			continue
		x,y,z = i.pos
		real_x = x * (tiles_tex_grid.item_width-8)/2  + z * 8
		real_y = y * (tiles_tex_grid.item_height-8)/2 + z * 8
		i.tile.blit(real_x, real_y)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
pyglet.app.run()
