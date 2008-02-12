
width = 0
height = 0

onChange = []

def update():
	for callback in onChange:
		callback()