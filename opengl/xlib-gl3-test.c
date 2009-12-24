/* gcc xlib-gl3-test.c -lGL -lm -o xlib-gl3-test
 * http://opengl.org/wiki/Tutorial:_OpenGL_3.0_Context_Creation_(GLX) */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <sys/time.h>

#define GL_GLEXT_PROTOTYPES 1
#define GLX_GLXEXT_PROTOTYPES 1
#include <X11/Xlib.h>
#include <GL/gl.h>
#include <GL/glx.h>

#define GLX_CONTEXT_MAJOR_VERSION_ARB 0x2091
#define GLX_CONTEXT_MINOR_VERSION_ARB 0x2092
typedef GLXContext (*glXCreateContextAttribsARBProc)(Display*, GLXFBConfig, GLXContext, Bool, const int*);


const char* vertexSrc =
	"attribute vec4 position;"
	"varying vec2 pos;"
	"void main()"
	"{"
		"gl_Position = position;"
		"pos = position.xy;"
	"}";
const char* fragmentSrc =
	"varying vec2 pos;"
	"uniform float phase;"
	"void main()"
	"{"
		"gl_FragColor = vec4(1, 1, 1, 1) * sin((pos.x * pos.x + pos.y * pos.y) * 40.0 + phase);"
	"}";
/*
const char* fragmentSrc =
	"varying vec2 pos;"
	"uniform float phase;"
	"void main()"
	"{"
		"gl_FragColor = vec4(1, 1, 1, 1) * step(pos.x * pos.x + pos.y * pos.y, phase * 0.2);"
	"}";
*/

void log_shader_info(GLuint shader)
{
	GLint length;
	glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &length);
	if (length)
	{
		char* buffer = malloc(length * sizeof(char));
		glGetShaderInfoLog(shader, length, NULL, buffer);
		printf("ShaderInfoLog: %s\n", buffer);
		free(buffer);
		GLint success;
		glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
		if (success != GL_TRUE)
		{
			exit(1);
		}
	}
}

GLuint create_shader(GLenum type, const char* pSource)
{
	GLuint shader = glCreateShader(type);
	glShaderSource(shader, 1, &pSource, NULL);
	glCompileShader(shader);
	log_shader_info(shader);
	return shader;
}

// Get a matching FB config/visual with the most samples per pixel
GLXFBConfig get_fb_config(Display *display)
{
	int best_fbc = -1, best_num_samp = -1;
	int fbcount, i;
	GLXFBConfig *fbc;
	static int visual_attribs[] =
		{
			GLX_X_RENDERABLE   , True,
			GLX_DRAWABLE_TYPE  , GLX_WINDOW_BIT,
			GLX_RENDER_TYPE	   , GLX_RGBA_BIT,
			GLX_X_VISUAL_TYPE  , GLX_TRUE_COLOR,
			GLX_RED_SIZE       , 8,
			GLX_GREEN_SIZE     , 8,
			GLX_BLUE_SIZE      , 8,
			GLX_ALPHA_SIZE     , 8,
			GLX_DEPTH_SIZE     , 24,
			GLX_STENCIL_SIZE   , 8,
			GLX_DOUBLEBUFFER   , True,
			//GLX_SAMPLE_BUFFERS , 1,
			//GLX_SAMPLES        , 4,
			None
		};

	if (!(fbc = glXChooseFBConfig(display, DefaultScreen(display), visual_attribs, &fbcount)))
	{
		printf("Failed to retrieve a framebuffer config\n");
		exit(1);
	}

	// Pick the FB config/visual with the most samples per pixel
	for (i = 0; i < fbcount; i++)
	{
		int samp_buf, samples;
		XVisualInfo *vi = glXGetVisualFromFBConfig(display, fbc[i]);
		if (!vi)
			continue;

		glXGetFBConfigAttrib(display, fbc[i], GLX_SAMPLE_BUFFERS, &samp_buf);
		glXGetFBConfigAttrib(display, fbc[i], GLX_SAMPLES, &samples	);

		if (best_fbc < 0 || samp_buf && samples > best_num_samp)
		{
			best_fbc = i;
			best_num_samp = samples;
		}

		XFree(vi);
	}

	GLXFBConfig fb_config = fbc[best_fbc];
	XFree(fbc);
	return fb_config;
}

GLXContext create_context(Display *display)
{
	GLXFBConfig fb_config;
	GLXContext ctx = 0;
	glXCreateContextAttribsARBProc glXCreateContextAttribsARB = NULL;

	fb_config = get_fb_config(display);

	/// FIXME: Create an old-style GLX context first, to get the correct function ptr.
	glXCreateContextAttribsARB = (glXCreateContextAttribsARBProc)glXGetProcAddress((const GLubyte *) "glXCreateContextAttribsARB");
	if (glXCreateContextAttribsARB)
	{
		// glXCreateContextAttribsARB does exist, try to get a GL 3.0 context...
		static int context_attribs[] =
			{
				GLX_CONTEXT_MAJOR_VERSION_ARB, 3,
				GLX_CONTEXT_MINOR_VERSION_ARB, 0,
				//GLX_CONTEXT_FLAGS_ARB GLX_CONTEXT_FORWARD_COMPATIBLE_BIT_ARB,
				None
			};
		ctx = glXCreateContextAttribsARB(display, fb_config, 0, True, context_attribs);
	}

	// fallback to 2.x GLX context
	if (0 == ctx)
	{
		printf("Failed to create GL 3.0 context ... using old-style GLX context\n");
		ctx = glXCreateNewContext(display, fb_config, GLX_RGBA_TYPE, NULL, True);
	}

	if (!glXIsDirect(display, ctx))
	{
		printf("Indirect GLX rendering context obtained\n");
		exit(1);
	}

	return ctx;
}

Window create_window(Display *display, const char *title)
{
	Window win;
	XSetWindowAttributes swa;

	swa.event_mask = ExposureMask | PointerMotionMask | StructureNotifyMask;
	win = XCreateWindow(display, DefaultRootWindow(display),
			0, 0, 800, 480,
			0, CopyFromParent, InputOutput, CopyFromParent,
			CWEventMask, &swa);
	if (!win)
	{
		printf("Failed to create window.\n");
		exit(1);
	}

	XStoreName(display, win, title);

	//set_window_properties(display, win);

	XMapWindow(display, win);
	XSync(display, False);

	return win;
}

void render(int phase_location)
{
	static float phase = 0;
	static const float vertexArray[] =
		{
			 0,-1, 0, 1,
			 1, 1, 0, 1,
			-1, 1, 0, 1
		};

	glClearColor(0, 1, 0, 1);
	glClear(GL_COLOR_BUFFER_BIT);

	glUniform1f(phase_location, phase);

	glVertexAttribPointer(0, 4, GL_FLOAT, false, 0, vertexArray);
	glEnableVertexAttribArray(0);
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 3);

	phase = fmodf(phase + 0.2, 2 * 3.141f);
}

void run(Display *display, Window win)
{
	bool quit = false;
	int numFrames = 0;
	struct timeval start_time;
	struct timezone tz;
	GLuint shaderProgram;
	int phase_location;
	XWindowAttributes win_attrs;

	gettimeofday(&start_time, &tz);

	shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, create_shader(GL_VERTEX_SHADER, vertexSrc));
	glAttachShader(shaderProgram, create_shader(GL_FRAGMENT_SHADER, fragmentSrc));
	glLinkProgram(shaderProgram);
	glUseProgram(shaderProgram);

	phase_location = glGetUniformLocation(shaderProgram, "phase");
	if (phase_location < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	XGetWindowAttributes(display, win, &win_attrs);
	glViewport(0, 0, win_attrs.width, win_attrs.height);

	while (!quit)
	{
		while (XPending(display))
		{
			XEvent xev;
			XNextEvent(display, &xev);

			if (xev.type == MotionNotify)
			{
				quit = true;
			}
		}

		render(phase_location);
		glXSwapBuffers(display, win);

		numFrames++;
		if (numFrames % 100 == 0)
		{
			struct timeval now;
			gettimeofday(&now, &tz);
			float delta = now.tv_sec - start_time.tv_sec + (now.tv_usec - start_time.tv_usec) * 0.000001f;
			printf("fps: %f\n", numFrames / delta);
		}
	}
}

int main(int argc, char **argv)
{
	Display *display;
	Window win;
	GLXContext gl_context;

	display = XOpenDisplay(NULL);
	if (display == NULL)
	{
		printf("Failed to open X display\n");
		exit(1);
	}

	win = create_window(display, "GL 3.0 Window");

	gl_context = create_context(display);
	glXMakeCurrent(display, win, gl_context);

	run(display, win);

	// cleanup
	glXMakeCurrent(display, 0, 0);
	glXDestroyContext(display, gl_context);
	XDestroyWindow(display, win);
	XCloseDisplay(display);

	return 0;
}
