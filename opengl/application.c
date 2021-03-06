#include <X11/Xlib.h>
#include <GL/gl.h>
#include <GL/glx.h>

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include <time.h>
#include <sys/time.h>
#include <sys/select.h>

#include "matrix.h"
#include "application.h"

struct application_tag
{
	Display *display;
	Window window;
	GLXContext gl_context;
	Queue *tasks;
};


#define GLX_CONTEXT_MAJOR_VERSION_ARB 0x2091
#define GLX_CONTEXT_MINOR_VERSION_ARB 0x2092
typedef GLXContext (*glXCreateContextAttribsARBProc)(Display*, GLXFBConfig, GLXContext, Bool, const int*);


/* Get a matching FB config/visual with the most samples per pixel */
GLXFBConfig get_fb_config(Display *display)
{
	GLXFBConfig fb_config;
	int best_fbc = -1, best_num_samp = -1;
	int fbcount, i;
	GLXFBConfig *fbc = NULL;
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
			/*GLX_SAMPLE_BUFFERS , 1, */
			/*GLX_SAMPLES        , 4, */
			None
		};

	if (!(fbc = glXChooseFBConfig(display, DefaultScreen(display), visual_attribs, &fbcount)))
	{
		printf("Failed to retrieve a framebuffer config\n");
		exit(1);
	}

	/* Pick the FB config/visual with the most samples per pixel */
	for (i = 0; i < fbcount; i++)
	{
		int samp_buf, samples;
		XVisualInfo *vi = glXGetVisualFromFBConfig(display, fbc[i]);
		if (!vi)
			continue;

		glXGetFBConfigAttrib(display, fbc[i], GLX_SAMPLE_BUFFERS, &samp_buf);
		glXGetFBConfigAttrib(display, fbc[i], GLX_SAMPLES, &samples	);

		if (best_fbc < 0 || (samp_buf && samples > best_num_samp))
		{
			best_fbc = i;
			best_num_samp = samples;
		}

		XFree(vi);
	}

	fb_config = fbc[best_fbc];
	XFree(fbc);
	return fb_config;
}

GLXContext create_context(Display *display)
{
	GLXFBConfig fb_config;
	GLXContext ctx = 0;
	glXCreateContextAttribsARBProc glXCreateContextAttribsARB = NULL;

	fb_config = get_fb_config(display);

	/** FIXME: Create an old-style GLX context first, to get the correct function ptr. */
	glXCreateContextAttribsARB = (glXCreateContextAttribsARBProc)glXGetProcAddress((const GLubyte *) "glXCreateContextAttribsARB");
	if (glXCreateContextAttribsARB)
	{
		/* glXCreateContextAttribsARB does exist, try to get a GL 3.0 context... */
		static int context_attribs[] =
			{
				GLX_CONTEXT_MAJOR_VERSION_ARB, 3,
				GLX_CONTEXT_MINOR_VERSION_ARB, 0,
				/* GLX_CONTEXT_FLAGS_ARB GLX_CONTEXT_FORWARD_COMPATIBLE_BIT_ARB, */
				None
			};
		ctx = glXCreateContextAttribsARB(display, fb_config, 0, True, context_attribs);
	}

	/* fallback to 2.x GLX context */
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


Application * application_new(const char *title)
{
	Application *app = NULL;
	XSetWindowAttributes swa;

	app = malloc(sizeof(Application));
	app->tasks = queue_new();

	app->display = XOpenDisplay(NULL);
	if (app->display == NULL)
	{
		printf("Failed to open X display\n");
		exit(1);
	}

	swa.event_mask = ExposureMask | PointerMotionMask | StructureNotifyMask;
	app->window = XCreateWindow(app->display, DefaultRootWindow(app->display),
			0, 0, 800, 480,
			0, CopyFromParent, InputOutput, CopyFromParent,
			CWEventMask, &swa);
	if (!app->window)
	{
		printf("Failed to create window.\n");
		exit(1);
	}

	XStoreName(app->display, app->window, title);

	/* set_window_properties(app->display, app->window); */

	XMapWindow(app->display, app->window);
	/* FIXME: wait for MapNotify event */

	app->gl_context = create_context(app->display);
	glXMakeCurrent(app->display, app->window, app->gl_context);

	return app;
}

void application_free(Application *app)
{
	queue_free(app->tasks);
	app->tasks = NULL;
	glXMakeCurrent(app->display, 0, NULL);
	glXDestroyContext(app->display, app->gl_context);
	app->gl_context = NULL;
	XDestroyWindow(app->display, app->window);
	app->window = 0;
	XCloseDisplay(app->display);
	app->display = NULL;
}

void application_run(Application *app, ViewPort *view_port)
{
	bool quit = false;
	int64_t prev_time = 0;
	int num_frames = 0;

	int fd = XConnectionNumber(app->display);
	fd_set fdset;
	FD_ZERO(&fdset);

	while (!quit)
	{
		struct timespec ts;
		int64_t now;
		Task *task = NULL;

		while (XPending(app->display))
		{
			XEvent xev;
			XNextEvent(app->display, &xev);

			if (xev.type == MotionNotify)
			{
				quit = true;
			}
			else if (xev.type == ConfigureNotify)
			{
				XConfigureEvent *ev = (XConfigureEvent *)&xev;
				view_port->resize(view_port->self, ev->width, ev->height);
			}
		}

		if (queue_is_empty(app->tasks))
		{
			/** WAIT_FOR_EVENT */
			FD_SET(fd, &fdset);
			pselect(fd+1, &fdset, NULL, NULL, NULL, NULL);
			continue;
		}

		clock_gettime(CLOCK_MONOTONIC, &ts);
		now = ts.tv_sec * 1000000000 + ts.tv_nsec;

		if (now < queue_top(app->tasks)->time)
		{
			/** WAIT_FOR_EVENT_WITH_TIMEOUT */
			struct timespec timeout;
			int64_t diff = queue_top(app->tasks)->time - now;
			timeout.tv_sec = diff / 1000000000;
			timeout.tv_nsec = diff % 1000000000;
			FD_SET(fd, &fdset);
			pselect(fd+1, &fdset, NULL, NULL, &timeout, NULL);
			continue;
		}

		task = queue_pop(app->tasks);
		if (!task->update(task, now))
			queue_insert(app->tasks, task);

		if (view_port->render(view_port->self))
			glXSwapBuffers(app->display, app->window);

		num_frames++;
		if (now - prev_time > 1000000000)
		{
			int delta = (now - prev_time)/1000000000;
			printf("fps: %d (%d)\n", num_frames / delta, num_frames);
			num_frames = 0;
			prev_time = now;
		}
	}
}

Queue * application_tasks(Application *app)
{
	return app->tasks;
}
