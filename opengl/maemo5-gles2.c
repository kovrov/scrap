/* gcc gles2.c -o gles2 -lEGL -lX11 -lGLESv2 */

#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xatom.h>
#include <GLES2/gl2.h>
#include <EGL/egl.h>
#include <math.h>
#include <sys/time.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>

const char* vertexSrc =
"attribute vec4 position;"
"varying mediump vec2 pos;"
"void main()"
"{"
	"gl_Position = position;"
	"pos = position.xy;"
"}";
const char* fragmentSrc =
"varying mediump vec2 pos;"
"uniform mediump float phase;"
"void main()"
"{"
	"gl_FragColor = vec4(1, 1, 1, 1) * sin((pos.x * pos.x + pos.y * pos.y) * 40.0 + phase);"
"}";
/*
const char* fragmentSrc =
"varying mediump vec2 pos;"
"uniform mediump float phase;"
"void main()"
"{"
	"gl_FragColor = vec4(1, 1, 1, 1) * step(pos.x * pos.x + pos.y * pos.y, phase * 0.2);"
"}";
*/

void log_shader_info(GLuint shader)
{
	GLint length;
	glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &length);
	if(length)
	{
		char* buffer = malloc(length * sizeof(char));
		glGetShaderInfoLog(shader, length, NULL, buffer);
		printf("%s", buffer);
		free(buffer);
		GLint success;
		glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
		if(success != GL_TRUE)
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


Window create_window(Display *display, const char *title)
{
	Window win;
	Atom wm_state, fullscreen, non_composited, portrait_mode_request, portrait_mode_support;

	XSetWindowAttributes swa;
	int one = 1;
	long on = 1;

	swa.event_mask = ExposureMask | PointerMotionMask;
	win = XCreateWindow(display, DefaultRootWindow(display),
			0, 0, 600, 400,
			0, CopyFromParent, InputOutput, CopyFromParent,
			CWEventMask, &swa);
	XStoreName(display, win, title);

	wm_state = XInternAtom(display, "_NET_WM_STATE", False);
	fullscreen = XInternAtom(display, "_NET_WM_STATE_FULLSCREEN", False);
	XChangeProperty(display, win, wm_state, XA_ATOM, 32, PropModeReplace, (unsigned char*)&fullscreen, 1);

	non_composited = XInternAtom(display, "_HILDON_NON_COMPOSITED_WINDOW", False);
	XChangeProperty(display, win, non_composited, XA_CARDINAL, 32, PropModeReplace, (unsigned char*)&one, 1);

	bool force_portrait = true;
	bool force_landscape = false;
	portrait_mode_request = XInternAtom(display, "_HILDON_PORTRAIT_MODE_REQUEST", False);
	portrait_mode_support = XInternAtom(display, "_HILDON_PORTRAIT_MODE_SUPPORT", False);
	if (force_portrait)
		XChangeProperty(display, win, portrait_mode_request, XA_CARDINAL, 32, PropModeReplace, (unsigned char *) &on, 1);
	else
		XDeleteProperty(display, win, portrait_mode_request);

	if (!force_landscape)
		XChangeProperty(display, win, portrait_mode_support, XA_CARDINAL, 32, PropModeReplace, (unsigned char *) &on, 1);
	else
		XDeleteProperty(display, win, portrait_mode_support);

	XMapWindow(display, win);
	XSync(display, False);

	return win;
}

EGLDisplay get_egl_display(Display *display)
{
	EGLDisplay egl_display;

	egl_display = eglGetDisplay((EGLNativeDisplayType)display);
	if(egl_display == EGL_NO_DISPLAY)
	{
		printf("Got no EGL display\n");
		exit(1);
	}

	if(!eglInitialize(egl_display, NULL, NULL))
	{
		printf("Unable to initialize EGL\n");
		exit(1);
	}

	return egl_display;
}

EGLConfig get_egl_config(EGLDisplay egl_display)
{
	EGLConfig ecfg;
	EGLint num_config;
	static EGLint attr[] =
		{
			EGL_BUFFER_SIZE, 16,
			EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
			EGL_NONE
		};

	if(!eglChooseConfig(egl_display, attr, &ecfg, 1, &num_config))
	{
		printf("Failed to choose config (%x)\n", eglGetError());
		exit(1);
	}

	if(num_config != 1)
	{
		printf("Didn't get exactly one config, but %d\n", num_config);
		exit(1);
	}

	return ecfg;
}

EGLContext create_context(EGLDisplay egl_display, EGLConfig egl_config)
{
	EGLContext egl_context;
	static EGLint ctxattr[] =
		{
			EGL_CONTEXT_CLIENT_VERSION, 2,
			EGL_NONE
		};

	egl_context = eglCreateContext(egl_display, egl_config, EGL_NO_CONTEXT, ctxattr);
	if(egl_context == EGL_NO_CONTEXT)
	{
		printf("Unable to create EGL context (%x)\n", eglGetError());
		exit(1);
	}

	return egl_context;
}

void render(int phase_location, EGLDisplay egl_display, EGLSurface egl_surface, XWindowAttributes *win_attrs)
{
	static float phase = 0;
	static const float vertexArray[] =
		{
			 0, -1, 0, 1,
			 1,  1, 0, 1,
			-1,  1, 0, 1
		};

	glViewport(0, 0, win_attrs->width, win_attrs->height);
	glClearColor(0, 1, 0, 1);
	glClear(GL_COLOR_BUFFER_BIT);

	glUniform1f(phase_location, phase);

	glVertexAttribPointer(0, 4, GL_FLOAT, false, 0, vertexArray);
	glEnableVertexAttribArray(0);
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 3);

	eglSwapBuffers(egl_display, egl_surface);

	phase = fmodf(phase + 0.2, 2 * 3.141f);
}

void run(Display *display, Window win, EGLDisplay egl_display, EGLSurface egl_surface)
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
	if(phase_location < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	XGetWindowAttributes(display, win, &win_attrs);

	while (!quit)
	{
		while (XPending(display))
		{
			XEvent xev;
			XNextEvent(display, &xev);

			if(xev.type == MotionNotify)
			{
				quit = true;
			}
		}

		render(phase_location, egl_display, egl_surface, &win_attrs);

		numFrames++;
		if(numFrames % 100 == 0)
		{
			struct timeval now;
			gettimeofday(&now, &tz);
			float delta = now.tv_sec - start_time.tv_sec + (now.tv_usec - start_time.tv_usec) * 0.000001f;
			printf("fps: %f\n", numFrames / delta);
		}
	}
}

int main()
{
	Display* display;
	Window win;
	EGLConfig egl_config;
	EGLDisplay egl_display;
	EGLContext egl_context;
	EGLSurface egl_drawable;

	display = XOpenDisplay(NULL);
	if(display == NULL)
	{
		printf("Failed to open X display\n");
		exit(1);
	}

	win = create_window(display, "GL test");
	egl_display = get_egl_display(display);
	egl_config = get_egl_config(egl_display);

	egl_drawable = eglCreateWindowSurface(egl_display, egl_config, (void*)win, NULL);
	if(egl_drawable == EGL_NO_SURFACE) {
		printf("Unable to create EGL surface (%x)\n", eglGetError());
		exit(1);
	}

	egl_context = create_context(egl_display, egl_config);
	eglMakeCurrent(egl_display, egl_drawable, egl_drawable, egl_context);

	run(display, win, egl_display, egl_drawable);

	eglDestroySurface(egl_display, egl_drawable);
	eglDestroyContext(egl_display, egl_context);
	eglTerminate(egl_display);
	XDestroyWindow(display, win);
	XCloseDisplay(display);

	return 0;
}
