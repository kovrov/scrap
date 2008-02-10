from pyglet.gl import *
from utils import normalizeVector, addVectors, rotateVectorY
import math

position  = (0.0, 0.0,  0.0)
direction = (0.0, 0.0, -1.0)
look_at   = (0.0, 0.0, -1.0)

def draw_task():
	while True:
		yield
		glLoadIdentity()
		gluLookAt(position[0], position[1], position[2],  # eye
		          look_at[0], look_at[1], look_at[2],  # center
		          0.0, 1.0, 0.0) # up
		#glRotatef(-RotatedX , 1.0, 0.0, 0.0);
		#glRotatef(-RotatedY , 0.0, 1.0, 0.0);
		#glRotatef(-RotatedZ , 0.0, 0.0, 1.0);
		#glTranslatef(-position[0], -position[1], -position[2])

def rotate_horizontal(degrees):  # left/right
	global direction, look_at
	direction = rotateVectorY(direction, math.radians(-degrees))
	look_at = addVectors(position, direction)

def rotate_vertical(degrees):  # up/down
	pass

def move(amount, vect):
	global position, look_at
	# move vector's angle
	dot = sum(x * y for x, y in zip((0.0, 0.0, -1.0), vect))  # dot product
	move_angle = math.acos(dot)
	# translation vector is final direction of movement
	translation_vect = rotateVectorY(direction, move_angle)
	position = (position[0] + translation_vect[0] * amount,
	            position[1] + translation_vect[1] * amount,
	            position[2] + translation_vect[2] * amount)
	look_at = addVectors(position, direction)
