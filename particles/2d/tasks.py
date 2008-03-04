import pyglet

g_tasks = list()
g_reset_time = False

def append(task):
	global g_reset_time
	if not g_tasks:
		pyglet.clock.schedule(update)
		g_reset_time = False
	task.next()  # init generator
	g_tasks.append(task)

def update(frame_time):
	global g_reset_time
	if not g_reset_time:
		g_reset_time = True
		frame_time = 0.0
	for task in g_tasks[:]:  #NOTE: iterating over a copy
		try:
			task.send(frame_time)
		except StopIteration:
			g_tasks.remove(task)
			if not g_tasks:
				pyglet.clock.unschedule(update)
