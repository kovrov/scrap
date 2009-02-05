import math
import pyglet
from pyglet.gl import *

def rotate_vector(vect, angle):
	x,y = vect
	theta = math.radians(angle)
	return (math.cos(theta)*x - math.sin(theta)*y,
			math.sin(theta)*x + math.cos(theta)*y)

def draw_circle(x,y,size):
	glPointSize(size)
	glEnable(GL_POINT_SMOOTH)
	pyglet.graphics.draw(1, GL_POINTS, ('v2i', (x,y)))

def draw_square(x,y,w,h):
	pyglet.graphics.draw(4, GL_QUADS, ('v2i', (x,y, x+w,y,  x+w,y+h, x,y+h)))

def collide(brick, ball):
	h_intersect = brick.x < ball.x+ball.size/2 and ball.x-ball.size/2 < brick.x+brick.w
	v_intersect = brick.y < ball.y+ball.size/2 and ball.y-ball.size/2 < brick.y+brick.h
	if not (h_intersect and v_intersect):
		return False
	if ball.dir[0] > 0:
		h_amount = ball.x+ball.size/2 - brick.x
	else:
		h_amount = brick.x+brick.w - ball.x-ball.size/2
	if ball.dir[1] > 0:
		v_amount = ball.y+ball.size/2 - brick.y
	else:
		v_amount = brick.y+brick.h - ball.y-ball.size/2
	if h_amount < v_amount:
		ball.dir = -ball.dir[0], ball.dir[1]
	else:
		ball.dir = ball.dir[0], -ball.dir[1]
	return True

class Paddle:
	def __init__(self):
		self.pos = 0; self.width = 48
	def draw(self):
		draw_square(self.pos - self.width/2,10, self.width,16)

class Ball:
	def __init__(self):
		self.x = 100.; self.y = 100.
		self.speed = 150.
		self.size = 9.
		self.dir = rotate_vector([0.,1.], -45)  # 45 degrees
		self.attached = True
	def draw(self):
		draw_circle(int(self.x), int(self.y), self.size)

class Brick:
	def __init__(self, x,y,w,h):
		self.x = x; self.y = y; self.w = w; self.h = h
	def draw(self):
		draw_square(self.x,self.y,self.w,self.h)

def main():
	paddle = Paddle()
	ball = Ball()
	brics = [
		Brick(100,432, 32,16), Brick(200,432, 32,16), Brick(300,432, 32,16), Brick(400,432, 32,16), Brick(500,432, 32,16),
		Brick(100,368, 32,16), Brick(200,368, 32,16), Brick(300,368, 32,16), Brick(400,368, 32,16), Brick(500,368, 32,16),
		Brick(100,304, 32,16), Brick(200,304, 32,16), Brick(300,304, 32,16), Brick(400,304, 32,16), Brick(500,304, 32,16)]
	window = pyglet.window.Window()
	@window.event
	def on_draw():
		window.clear()
		paddle.draw()
		ball.draw()
		for br in brics:
			br.draw()
	@window.event
	def on_mouse_press(x, y, button, modifiers):
		ball.attached = False
	@window.event
	def on_mouse_motion(x, y, dx, dy):
		paddle.pos =  x
		if ball.attached:
			ball.x = x
			ball.y = 10+16 + ball.size/2
	def update(dt):
		if ball.attached:
			return
		ball.x += ball.speed * dt * ball.dir[0]
		ball.y += ball.speed * dt * ball.dir[1]
		# world boundary collisions
		if ball.x - ball.size/2. <= 0.:  # left
			ball.dir = (abs(ball.dir[0]), ball.dir[1])
		if ball.x + ball.size/2. >= window.width:  # right
			ball.dir = (-abs(ball.dir[0]), ball.dir[1])
		if ball.y + ball.size/2 >= window.height:  # top
			ball.dir = (ball.dir[0], -abs(ball.dir[1]))
		if ball.y + ball.size/2. <= 0.:  # bottom
			ball.attached = True # TODO: ball lost
			ball.dir = rotate_vector([0.,1.], -45)
		# paddle collisions
		if ball.y-ball.size/2. <= 10+16 and ball.dir[1] < 0:  # TEMP: paddle top plane
			if paddle.pos-paddle.width/2 <= ball.x+ball.size/2 and paddle.pos+paddle.width/2 >= ball.x-ball.size/2:
				refl_k = 1. / (paddle.width/2.) * (ball.x - paddle.pos)
				if refl_k > 1.: refl_k = 1.
				if refl_k < -1.: refl_k = -1.
				ball.dir = rotate_vector([0.,1.], refl_k * -75)
		# bricks collisions
		for br in brics[:]:
			if collide(br, ball):
				brics.remove(br)
	pyglet.clock.schedule_interval(update, 1/60.0)  # 60fps
	pyglet.app.run()

if __name__ == "__main__": main()
