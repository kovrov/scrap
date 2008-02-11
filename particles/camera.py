from pyglet.gl import *
from utils import addVectors, rotateVectorY
import math

# invariants
position  = (0.0, 0.0,  0.0)
direction = (0.0, 0.0, -1.0)

# pre cached properties
look_at   = (0.0, 0.0, -1.0)
yaw = 0.0
pitch = 0.0

def draw_task():
	while True:
		yield
		glLoadIdentity()
		gluLookAt(position[0], position[1], position[2],  # eye
		          look_at[0], look_at[1], look_at[2],  # center
		          0.0, 1.0, 0.0) # up vector

def rotate_horizontal(degrees):  # left/right
	global direction, look_at, yaw
	direction = rotateVectorY(direction, math.radians(-degrees))
	look_at = addVectors(position, direction)
	yaw += degrees  # temp hack!

def rotate_vertical(degrees):  # up/down
	pass

def move(amount, angle):
	global position, look_at
	# translation vector is final direction of movement
	translation_vect = rotateVectorY(direction, math.radians(-angle))
	position = (position[0] + translation_vect[0] * amount,
	            position[1] + translation_vect[1] * amount,
	            position[2] + translation_vect[2] * amount)
	look_at = addVectors(position, direction)
