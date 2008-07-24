/* bla bla */

module renderer;

static import gl = opengl.gl;
static import glu = opengl.glu;


private bool _initialized = false;

// init/shutdown is platform-specific...
version (Windows)
{
	static import win32 = win32.windows;

	private win32.HGLRC _rendering_context;
	private win32.HANDLE _device_context;

	void init(win32.HWND wnd_handle, int bits)
	in { assert (!_initialized, "renderer can not be initialized twice!"); }
	out
	{
		assert (_initialized, "initialized flag must be set!"); 
		assert (_device_context, "device context must be acquired!"); 
		assert (_rendering_context, "rendering context must be created!"); 
	}
	body
	{
		// pixel format of drawing surface is part of win32 opengl interface
		static win32.PIXELFORMATDESCRIPTOR pfd;
		pfd.nSize = pfd.sizeof;  // size of this data structure
		pfd.nVersion = 1;  // version of this data structure
		pfd.dwFlags = win32.PFD_DRAW_TO_WINDOW | win32.PFD_SUPPORT_OPENGL | win32.PFD_DOUBLEBUFFER;
		pfd.iPixelType = win32.PFD_TYPE_RGBA;
		pfd.cColorBits = bits;  // color depth
		pfd.cDepthBits = 16;  // 16 bit z-buffer (depth buffer)

		_device_context = win32.GetDC(wnd_handle);
		if (!_device_context) throw new Exception("Can't create a GL device context");
		scope (failure) win32.wglMakeCurrent(_device_context, null);  // release

		// choose the closest pixel format available
		int pixel_format = win32.ChoosePixelFormat(_device_context, &pfd);
		if (!pixel_format) throw new Exception("Can't find a suitable pixel format");

		if (!win32.SetPixelFormat(_device_context, pixel_format, &pfd))
			throw new Exception("Can't set the pixel format");

		_rendering_context = win32.wglCreateContext(_device_context);
		if (!_rendering_context) throw new Exception("Can't create a GL rendering context");
		scope (failure) win32.wglDeleteContext(_rendering_context);

		if (!win32.wglMakeCurrent(_device_context, _rendering_context))
			throw new Exception("Can't activate the GL rendering context");

		_initialized = true;
	}


	void shutdown()
	in { assert (_initialized, "renderer must be initialized!"); }
	out { assert (!_initialized, "initialized flag must be cleared!"); }
	body
	{
		win32.wglMakeCurrent(_device_context, null);  // release
		win32.wglDeleteContext(_rendering_context);
		_initialized = false;
	}

	void swapBuffers()
	in { assert (_initialized, "renderer must be initialized!"); }
	body
	{
		win32.SwapBuffers(_device_context);
	}
}

void resizeViewport(int width, int height)
in { assert (_initialized, "renderer must be initialized!"); }
body
{
	if (height == 0) height = 1;  // Prevent A Divide By Zero By

	gl.glViewport(0, 0, width, height);  // Reset The Current Viewport
	gl.glMatrixMode(gl.GL_PROJECTION);  // Select The Projection Matrix
	gl.glLoadIdentity();  // Reset The Projection Matrix

	// Calculate The Aspect Ratio Of The Window
	glu.gluPerspective(45.0, cast(gl.GLfloat)width / cast(gl.GLfloat)height, 0.1, 100.0);

	gl.glMatrixMode(gl.GL_MODELVIEW);  // Select The Modelview Matrix
	gl.glLoadIdentity();  // Reset The Modelview Matrix
}


void clearBuffers()
in { assert (_initialized, "renderer must be initialized!"); }
body
{
	gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT);
}

void resetView()
in { assert (_initialized, "renderer must be initialized!"); }
body
{
	gl.glLoadIdentity();
}


void drawStone(float[] color)
in { assert (color.length == 3); }
body
{
	gl.glColor3fv(color.ptr);
	gl.glBegin(gl.GL_QUADS);
		gl.glVertex2f(-0.9, -0.9);
		gl.glVertex2f( 0.9, -0.9);
		gl.glVertex2f( 0.9,  0.9);
		gl.glVertex2f(-0.9,  0.9);
	gl.glEnd();
}
