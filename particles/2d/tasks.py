
g_tasks = list()

def append(task):
	if not g_tasks:
		pyglet.clock.schedule(update)
	task.next()  # init
	g_tasks.append(task)

def update(frame_time):
	# update game objects state
	ship.key_handler(keys, frame_time)
	# update view
	view.key_handler(keys, frame_time)
	# drawing tasks scheduler run
	for task in g_tasks[:]:
		try: task.send(frame_time)
		except StopIteration: g_tasks.remove(task)
	if not g_tasks:
		pyglet.clock.unschedule(update)
