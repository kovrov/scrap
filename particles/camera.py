from pyglet.gl import *
from utils import normalizeVector, addVectors

position  = [0.0, 0.0, 0.0]
direction = [0.0, 0.0, 0.0]

def draw_task():
	while True:
		yield
		glLoadIdentity()
		#glRotatef(-RotatedX , 1.0, 0.0, 0.0);
		#glRotatef(-RotatedY , 0.0, 1.0, 0.0);
		#glRotatef(-RotatedZ , 0.0, 0.0, 1.0);
		glTranslatef(-position[0], -position[1], -position[2])

def rotate_horizontal(degrees):  # left/right
	direction = rotateVector(direction, degrees)

def rotate_vertical(degrees):  # up/down
	pass

def move(amount, vect):
	direction[0] + vect[0]
	direction[1] + vect[1]
	direction[2] + vect[2]
	move_vect = normalizeVector(addVectors(direction, vect))
	position[0]  += move_vect[0] * amount
	position[1]  += move_vect[1] * amount
	position[2]  += move_vect[2] * amount
