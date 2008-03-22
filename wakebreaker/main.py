"""
Peter Angstadt
http://pete.nextraztus.com/

It seems Opengl ES uses fixed-point numbers, see:
http://docs.python.org/lib/decimal-faq.html
http://pypi.python.org/pypi/Simple%20Python%20Fixed-Point%20Module
"""
if __name__ == '__main__':
	import pyglet
	from pyglet.window import key

	import game

	WINDOW_WIDTH  = 320
	WINDOW_HEIGHT = 240

	win = pyglet.window.Window(caption="Wake Breaker")
	g = game.Game()

	@win.event
	def on_key_press(symbol, modifiers):
		if symbol == key.LEFT:
			g.keyDown(game.G_LEFT)
		if symbol == key.UP:         
			g.keyDown(game.G_UP)
		if symbol == key.RIGHT:
			g.keyDown(game.G_RIGHT)
		if symbol == key.DOWN:
			g.keyDown(game.G_DOWN)
		if symbol == key.RETURN:
			g.keyDown(game.G_OK)
		if symbol == key.NUM_1:
			g.keyDown(game.G_DEVICE1)
		if symbol == key.NUM_2:
			g.keyDown(game.G_DEVICE2)

	@win.event
	def on_key_release(symbol, modifiers):
		if symbol == key.LEFT:
			g.keyUp(game.G_LEFT)
		if symbol == key.UP:         
			g.keyUp(game.G_UP)
		if symbol == key.RIGHT:
			g.keyUp(game.G_RIGHT)
		if symbol == key.DOWN:
			g.keyUp(game.G_DOWN)
		if symbol == key.RETURN:
			g.keyUp(game.G_OK)
		if symbol == key.NUM_1:
			g.keyUp(game.G_DEVICE1)
		if symbol == key.NUM_2:
			g.keyUp(game.G_DEVICE2)

	g.create(WINDOW_WIDTH, WINDOW_HEIGHT, win)

	while not win.has_exit:
		win.dispatch_events()
		frame_time = pyglet.clock.tick()
		#win.clear()
		# draw ...
		g.menu()
		win.flip()
