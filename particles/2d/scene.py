
import view
viewport = view

models = []

class Node:  # spatial
	def __init__(self, pos):
		self.origin = pos

def draw():
	viewport.draw()  # do we have viewport/camera here?
	for model in models:
		model.draw()


'''
for view in vews:
	set_viewport
	translate_camera
	for item in scene.solid:
		draw
	for item in scene.blended:
		draw

'''
