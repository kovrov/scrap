import pyglet

window = pyglet.window.Window(vsync=False)
fps_display = pyglet.clock.ClockDisplay()

def update(dt):
	pass

def on_draw():
	window.clear()
	fps_display.draw()

if (0):
	print "new-style loop..."
	window.set_handlers(on_draw)
	pyglet.clock.schedule(update)
	pyglet.app.run()
else:
	print "old-style loop..."
	while not window.has_exit:
		window.dispatch_events()
		update(pyglet.clock.tick())
		on_draw()
		window.flip() 
