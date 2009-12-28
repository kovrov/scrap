/* gcc gles2.c -o gles2 -lEGL -lX11 -lGLESv2 -lrt */

#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xatom.h>
#include <GLES2/gl2.h>
#include <EGL/egl.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>

#include <math.h>
#include <time.h>
//#include <sys/time.h>

typedef struct
{
	EGLDisplay display;
	EGLSurface surface;
	EGLConfig config;
	EGLContext context;
} EGL;

typedef struct
{
	float phase;
	int phase_location;
} Scene;

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
			printf("shader GL_COMPILE_STATUS fail\n");
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

void set_window_properties(Display *display, Window win)
{
	Atom wm_state, fullscreen, non_composited, portrait_mode_request, portrait_mode_support;
	int one = 1;
	long on = 1;

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

	set_window_properties(display, win);

	XMapWindow(display, win);
	// FIXME: wait for MapNotify event

	return win;
}

EGLConfig egl_get_config(EGLDisplay egl_display)
{
	EGLConfig ecfg;
	EGLint num_config;
	static EGLint attr[] =
		{
			EGL_BUFFER_SIZE, 16,
			EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,
			EGL_NONE
		};

	if (!eglChooseConfig(egl_display, attr, &ecfg, 1, &num_config))
	{
		printf("Failed to choose config (%x)\n", eglGetError());
		exit(1);
	}

	if (num_config != 1)
	{
		printf("Didn't get exactly one config, but %d\n", num_config);
		exit(1);
	}

	return ecfg;
}

void egl_init(EGL *egl, Display *display, Window win)
{
	static EGLint ctxattr[] =
		{
			EGL_CONTEXT_CLIENT_VERSION, 2,
			EGL_NONE
		};

	egl->display = eglGetDisplay((EGLNativeDisplayType)display);
	if (egl->display == EGL_NO_DISPLAY)
	{
		printf("Got no EGL display\n");
		exit(1);
	}

	if (!eglInitialize(egl->display, NULL, NULL))
	{
		printf("Unable to initialize EGL\n");
		exit(1);
	}

	egl->config = egl_get_config(egl->display);
	egl->surface = eglCreateWindowSurface(egl->display, egl->config, (void*)win, NULL);
	if (egl->surface == EGL_NO_SURFACE)
	{
		printf("Unable to create EGL surface (%x)\n", eglGetError());
		exit(1);
	}

	egl->context = eglCreateContext(egl->display, egl->config, EGL_NO_CONTEXT, ctxattr);
	if (egl->context == EGL_NO_CONTEXT)
	{
		printf("Unable to create EGL context (%x)\n", eglGetError());
		exit(1);
	}

	eglMakeCurrent(egl->display, egl->surface, egl->surface, egl->context);
}

void egl_destroy(EGL *egl)
{
	eglMakeCurrent(egl->display, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT);
	eglDestroyContext(egl->display, egl->context);
	egl->surface = NULL;
	eglDestroySurface(egl->display, egl->surface);
	egl->surface = NULL;
	eglTerminate(egl->display);
	egl->display = NULL;
}


void render(Scene *scene, EGL *egl)
{
	static const float vertexArray[] =
		{
			 0, -1, 0, 1,
			 1,  1, 0, 1,
			-1,  1, 0, 1
		};

	glClearColor(0, 1, 0, 1);
	glClear(GL_COLOR_BUFFER_BIT);

	glUniform1f(scene->phase_location, scene->phase);

	glVertexAttribPointer(0, 4, GL_FLOAT, false, 0, vertexArray);
	glEnableVertexAttribArray(0);
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 3);
}

void run(Display *display, EGL *egl)
{
	bool quit = false;
	GLuint shaderProgram;
	Scene scene;

	int64_t prev_time = 0;
	int num_frames = 0;

	shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, create_shader(GL_VERTEX_SHADER, vertexSrc));
	glAttachShader(shaderProgram, create_shader(GL_FRAGMENT_SHADER, fragmentSrc));
	glLinkProgram(shaderProgram);
	glUseProgram(shaderProgram);

	scene.phase_location = glGetUniformLocation(shaderProgram, "phase");
	if (scene.phase_location < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	while (!quit)
	{
		struct timespec ts;
		int64_t time;

		while (XPending(display))
		{
			XEvent xev;
			XNextEvent(display, &xev);

			if (xev.type == MotionNotify)
			{
				quit = true;
			}
			else if (xev.type == ConfigureNotify)
			{
				XConfigureEvent *ev = (XConfigureEvent *)&xev;
				glViewport(0, 0, ev->width, ev->height);
			}
		}

		clock_gettime(CLOCK_MONOTONIC, &ts);
		time = ts.tv_sec * 1000000000LL + ts.tv_nsec;

		scene.phase = fmodf(time*0.000000015f, 2 * 3.141f);
		render(&scene, egl);
		eglSwapBuffers(egl->display, egl->surface);

		num_frames++;
		if (time - prev_time > 1000000000LL)
		{
			int delta = (time - prev_time)/1000000000LL;
			printf("fps: %d (%d)\n", num_frames / delta, num_frames);
			num_frames = 0;
			prev_time = time;
		}

		if (1)
		{
			struct timespec rqtp = ts;
			rqtp.tv_nsec += (1000000000LL/30);
			if (rqtp.tv_nsec >= 1000000000LL)
			{
				rqtp.tv_nsec %= 1000000000LL;
				rqtp.tv_sec++;
			}
			clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &rqtp, NULL);
		}
	}
}

int main(int argc, char **argv)
{
	Display *display;
	Window win;
	EGL egl;

	display = XOpenDisplay(NULL);
	if (display == NULL)
	{
		printf("Failed to open X display\n");
		exit(1);
	}

	win = create_window(display, "GL test");
	egl_init(&egl, display, win);

	run(display, &egl);

	// cleanup
	egl_destroy(&egl);
	XDestroyWindow(display, win);
	//XCloseDisplay(display); /// FIXME: why it crashes on maemo5?

	return 0;
}
