module game;

static import renderer;
import std.c.stdlib;

static import gl = opengl.gl;
debug import std.stdio;

float[3][7] _colors = [
		[1.0f, 0.4f, 0.4f],
		[0.4f, 0.9f, 0.4f],
		[0.4f, 0.4f, 0.9f],
		[1.0f, 0.9f, 0.4f], // yellow
		[0.8f, 0.4f, 1.0f], // violet
		[0.4f, 0.9f, 0.9f],
		[0.7f, 0.7f, 0.7f]];
float[3][8*8] _stones;


static this()
{
	foreach (i, stone; _stones)
	{
		uint stone_idx = rand() % 7;
		_stones[i][0] = _colors[stone_idx][0];
		_stones[i][1] = _colors[stone_idx][1];
		_stones[i][2] = _colors[stone_idx][2];
	}
}



void updateScene()
{
}



void drawScene()
in
{
	gl.GLint params;
	gl.glGetIntegerv(gl.GL_MATRIX_MODE, &params);
	assert (params == gl.GL_MODELVIEW, "current matrix mode must be GL_MODELVIEW!");
}
body
{
	/*
		draw level.background
		draw level.board
		draw each level.board.stones
		draw fx_stack
		draw level.UI
	*/
	renderer.clearBuffers();
	renderer.resetView();

	gl.glTranslatef(-2f*4 + 1f, -2f*4 + 1f, -20f);

	for (int i=0; i < 8; i++)
	{
		for (int j=0; j < 8; j++)
		{
			renderer.drawStone(_stones[i*8+j]);
			gl.glTranslatef(2f, 0f, 0f);
		}
		gl.glTranslatef(-2f * 8, 2f, 0f);
	}
}



void init()
{
	//LoadGLTextures();  // Jump To Texture Loading Routine
	gl.glEnable(gl.GL_TEXTURE_2D);  // Enable Texture Mapping
	gl.glShadeModel(gl.GL_SMOOTH);  // Enables Smooth Shading
	gl.glClearColor(0.0, 0.0, 0.0, 0.0);  // Black Background
	gl.glClearDepth(1.0);  // Depth Buffer Setup
	gl.glEnable(gl.GL_DEPTH_TEST);  // Enables Depth Testing
	gl.glDepthFunc(gl.GL_LEQUAL);  // The Type Of Depth Test To Do
	gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST);  // Really Nice Perspective Calculations

	gl.GLfloat[] g_light_ambient =  [ 0.5, 0.5, 0.5, 1.0 ];
	gl.GLfloat[] g_light_diffuse =  [ 1.0, 1.0, 1.0, 1.0 ];
	gl.GLfloat[] g_light_position = [ 0.0, 0.0, 2.0, 1.0 ];
	gl.glLightfv(gl.GL_LIGHT1, gl.GL_AMBIENT, g_light_ambient.ptr);  // Setup The Ambient Light
	gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, g_light_diffuse.ptr);  // Setup The Diffuse Light
	gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, g_light_position.ptr);  // Position The Light
	gl.glEnable(gl.GL_LIGHT1);  // Enable Light One

	gl.glColor4f(1.0, 1.0, 1.0, 0.5);  // Full Brightness.  50% Alpha ( NEW )
	/* Incoming (source) alpha is correctly thought of as a material opacity,
	 * ranging from 1.0 (K	), representing complete opacity, to 0.0 (0),
	 * representing complete transparency.*/
	gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE);  // Set The Blending Function For Translucency ( NEW )
}
