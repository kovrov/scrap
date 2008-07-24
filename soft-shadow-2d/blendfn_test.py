import math
import pyglet
from pyglet.window import key
from pyglet.gl import *

screen = pyglet.window.get_platform().get_default_display().get_default_screen()
template = pyglet.gl.Config(alpha_size=8, depth_size=24, double_buffer=True)
config = screen.get_best_config(template)
context = config.create_context(None)
win = pyglet.window.Window(resizable=True, vsync=True, context=context)

shadow_blend_factors = (GL_ZERO, GL_ZERO)
geometry_blend_factors = (GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA)
light_blend_factors = (GL_ZERO, GL_ZERO)

@win.event
def on_draw():
	#glClearColor(0., 0., 0., 0.2)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(win.width/2, win.height/2, 0.)

	glEnable(GL_BLEND)
	glBlendFunc(*shadow_blend_factors)
	glColorMask(False, False, False, True)  # disable color buffer
	draw_light( 50,  50, 200)
	draw_light(-50, -50, 200)
	glColorMask(True, True, True, True)  # enable color buffer

	glBlendFunc(*geometry_blend_factors)#GL_ONE_MINUS_DST_COLOR, GL_ONE_MINUS_SRC_COLOR
	draw_scene()

	# apply light color
	glBlendFunc(*light_blend_factors)
	draw_light( 50,  50, 200, (1.,0.,0.))
	draw_light(-50, -50, 200, (0.,0.,1.))


def draw_light(x, y, radius, color=(1., 1., 1.), intensity=1., numSubdivisions=32):
	increment = math.pi*2 / numSubdivisions
	glBegin(GL_TRIANGLE_FAN)
	glColor4f(color[0], color[1], color[2], intensity)
	glVertex2f(x, y)
	glColor4f(color[0], color[1], color[2], 0.)
	for i in xrange(numSubdivisions+1):
		glVertex2f(radius*math.cos(i*increment)+x, radius*math.sin(i*increment)+y)
	glEnd()

def draw_scene():
	glBegin(GL_TRIANGLES)
	glColor3f(0.3, 0.9, 0.3)
	glVertex2f( 200., -200.)
	glVertex2f( 200.,  200.)
	glVertex2f(-200.,  200.)
	glColor3f(0.3, 0.3, 0.3)
	glVertex2f(-200.,  200.)
	glVertex2f(-200., -200.)
	glVertex2f( 200., -200.)
	glEnd()

#@win.event
#def on_mouse_motion(x, y, dx, dy):
#	pass

gl_symbols = {	GL_CONSTANT_ALPHA: "GL_CONSTANT_ALPHA",
				GL_CONSTANT_COLOR: "GL_CONSTANT_COLOR",
				GL_DST_ALPHA: "GL_DST_ALPHA",
				GL_DST_COLOR: "GL_DST_COLOR",
				GL_ONE: "GL_ONE",
				GL_ONE_MINUS_CONSTANT_ALPHA: "GL_ONE_MINUS_CONSTANT_ALPHA",
				GL_ONE_MINUS_CONSTANT_COLOR: "GL_ONE_MINUS_CONSTANT_COLOR",
				GL_ONE_MINUS_DST_ALPHA: "GL_ONE_MINUS_DST_ALPHA",
				GL_ONE_MINUS_DST_COLOR: "GL_ONE_MINUS_DST_COLOR",
				GL_ONE_MINUS_SRC_ALPHA: "GL_ONE_MINUS_SRC_ALPHA",
				GL_ONE_MINUS_SRC_COLOR: "GL_ONE_MINUS_SRC_COLOR",
				GL_SRC_ALPHA: "GL_SRC_ALPHA",
				GL_SRC_ALPHA_SATURATE: "GL_SRC_ALPHA_SATURATE",
				GL_SRC_COLOR: "GL_SRC_COLOR",
				GL_ZERO: "GL_ZERO"}
sfactor = (	GL_ZERO,
			GL_ONE,
			GL_SRC_COLOR,
			GL_ONE_MINUS_SRC_COLOR,
			GL_DST_COLOR,
			GL_ONE_MINUS_DST_COLOR,
			GL_SRC_ALPHA,
			GL_ONE_MINUS_SRC_ALPHA,
			GL_DST_ALPHA,
			GL_ONE_MINUS_DST_ALPHA,
			#GL_CONSTANT_COLOR,
			#GL_ONE_MINUS_CONSTANT_COLOR,
			#GL_CONSTANT_ALPHA,
			#GL_ONE_MINUS_CONSTANT_ALPHA,
			GL_SRC_ALPHA_SATURATE)
dfactor = (	GL_ZERO,
			GL_ONE,
			GL_SRC_COLOR,
			GL_ONE_MINUS_SRC_COLOR,
			GL_DST_COLOR,
			GL_ONE_MINUS_DST_COLOR,
			GL_SRC_ALPHA,
			GL_ONE_MINUS_SRC_ALPHA,
			GL_DST_ALPHA,
			GL_ONE_MINUS_DST_ALPHA,
			#GL_CONSTANT_COLOR,
			#GL_ONE_MINUS_CONSTANT_COLOR,
			#GL_CONSTANT_ALPHA,
			#GL_ONE_MINUS_CONSTANT_ALPHA
			)
factors = [(s,d) for d in dfactor for s in sfactor]
geometry_factors = [(GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA),] #[(GL_DST_ALPHA, d) for d in dfactor]
shadow_factors = (	#(GL_ONE, GL_ONE), # weird add color
					(GL_ONE, GL_ONE_MINUS_SRC_COLOR), # add color
					(GL_ONE, GL_ONE_MINUS_SRC_ALPHA), # add color
					#(GL_SRC_COLOR, GL_ONE), # narrow add color
					#(GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR), # blend color
					#(GL_SRC_COLOR, GL_ONE_MINUS_SRC_ALPHA), # blend color
					#(GL_DST_COLOR, GL_ONE), # black
					(GL_ONE_MINUS_DST_COLOR, GL_ONE), # add color
					#(GL_ONE_MINUS_DST_COLOR, GL_ONE_MINUS_SRC_COLOR), # clamp color
					#(GL_ONE_MINUS_DST_COLOR, GL_ONE_MINUS_SRC_ALPHA), # clamp color
					#(GL_SRC_ALPHA, GL_ONE), # narrow add color
					#(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_COLOR), # blend color
					#(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA), # blend color
					(GL_ONE_MINUS_DST_ALPHA, GL_ONE), # add color
					#(GL_ONE_MINUS_DST_ALPHA, GL_ONE_MINUS_SRC_COLOR), # clamp color
					#(GL_ONE_MINUS_DST_ALPHA, GL_ONE_MINUS_SRC_ALPHA), # clamp color
					#(GL_SRC_ALPHA_SATURATE, GL_ONE), # weird add color
					(GL_SRC_ALPHA_SATURATE, GL_ONE_MINUS_SRC_COLOR), # add color
					(GL_SRC_ALPHA_SATURATE, GL_ONE_MINUS_SRC_ALPHA) # add color
					)
light_factors = factors
megafactors = [(s,l) for s in shadow_factors for l in light_factors]
megafactor_indices = range(len(megafactors))
megafactor_id = 0


@win.event
def on_key_press(symbol, modifiers):
	global megafactor_id
	global shadow_blend_factors, light_blend_factors

	if symbol == key.PAGEDOWN:
		megafactor_id += 1
		if len(megafactor_indices) < megafactor_id+1:
			megafactor_id = 0
			print "#"
	if symbol == key.PAGEUP:
		megafactor_id -= 1
		if 0 > megafactor_id:
			megafactor_id = len(megafactor_indices)-1
			print "#"

	if symbol == key.DELETE:
		print "<DEL"
		shadow_f, light_f = megafactors[megafactor_indices[megafactor_id]]
		print "  shadow", gl_symbols[shadow_f[0]], gl_symbols[shadow_f[1]]
		print "  geometry", gl_symbols[light_f[0]], gl_symbols[light_f[1]]
		print "/DEL>"
		del megafactor_indices[megafactor_id]
		if len(megafactor_indices) < megafactor_id+1:
			megafactor_id = 0
			print "#"

	if symbol == key.SPACE:
		for id in megafactor_indices:
			shadow_blend_factors, light_blend_factors = megafactors[id]
			print "shadow", gl_symbols[shadow_blend_factors[0]], gl_symbols[shadow_blend_factors[1]]
			print "light", gl_symbols[light_blend_factors[0]], gl_symbols[light_blend_factors[1]]
			print


	id = megafactor_indices[megafactor_id]
	shadow_blend_factors, light_blend_factors = megafactors[id]
	print id, "shadow", gl_symbols[shadow_blend_factors[0]], gl_symbols[shadow_blend_factors[1]]
	print id, "light", gl_symbols[light_blend_factors[0]], gl_symbols[light_blend_factors[1]]
	
pyglet.app.run()
