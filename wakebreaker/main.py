"""
Peter Angstadt
http://pete.nextraztus.com/
"""
if __name__ == '__main__':
	import pyglet
	from pyglet.window import key

	from game import Game

	WINDOW_WIDTH  = 320
	WINDOW_HEIGHT = 240

	win = pyglet.window.Window(caption="Wake Breaker")
	game = Game()

	@win.event
	def on_key_press(symbol, modifiers):
		if symbol == key.LEFT:
			game.KeyDown(G_LEFT)
		if symbol == key.UP:         
			game.KeyDown(G_UP)
		if symbol == key.RIGHT:
			game.KeyDown(G_RIGHT)
		if symbol == key.DOWN:
			game.KeyDown(G_DOWN)
		if symbol == key.RETURN:
			game.KeyDown(G_OK)
		if symbol == key.NUMPAD1:
			game.KeyDown(G_DEVICE1)
		if symbol == key.NUMPAD2:
			game.KeyDown(G_DEVICE2)

	@win.event
	def on_key_release(symbol, modifiers):
		if symbol == key.LEFT:
			game.KeyUp(G_LEFT)
		if symbol == key.UP:         
			game.KeyUp(G_UP)
		if symbol == key.RIGHT:
			game.KeyUp(G_RIGHT)
		if symbol == key.DOWN:
			game.KeyUp(G_DOWN)
		if symbol == key.RETURN:
			game.KeyUp(G_OK)
		if symbol == key.NUMPAD1:
			game.KeyUp(G_DEVICE1)
		if symbol == key.NUMPAD2:
			game.KeyUp(G_DEVICE2)

	game.create(WINDOW_WIDTH, WINDOW_HEIGHT, win)

	while not win.has_exit:
		win.dispatch_events()
		frame_time = pyglet.clock.tick()
		#win.clear()
		# draw ...
		game.menu()
		win.flip()

	game.Destroy()
