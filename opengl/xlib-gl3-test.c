/* gcc xlib-gl3-test.c -lGL -lm -o xlib-gl3-test
 * http://opengl.org/wiki/Tutorial:_OpenGL_3.0_Context_Creation_(GLX) */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
//#include <sys/time.h>
#include <sys/select.h>

#define GL_GLEXT_PROTOTYPES 1
#define GLX_GLXEXT_PROTOTYPES 1
#include <X11/Xlib.h>
#include <GL/gl.h>
#include <GL/glx.h>

#define GLX_CONTEXT_MAJOR_VERSION_ARB 0x2091
#define GLX_CONTEXT_MINOR_VERSION_ARB 0x2092
typedef GLXContext (*glXCreateContextAttribsARBProc)(Display*, GLXFBConfig, GLXContext, Bool, const int*);

//-queue.h----------------------------------------------------------------------

typedef bool (*TaskCB)(int64_t, void *);

typedef struct
{
	int64_t time;
	TaskCB update;
	void* ctx;
} Task;

int task_cmp(Task *t1, Task *t2)
{
	return t1->time > t2->time ? 1 : t1->time < t2->time ? -1 : 0;
}

typedef struct
{
	Task **heap;
	size_t allocated;
	size_t length;
} Queue;

void queue_init(Queue *q);
void queue_enqueue(Queue *q, Task *task);
//void bheap_insert(Queue *q, Task *task);
Task * bheap_pop(Queue *q);
Task * bheap_top(Queue *q);
bool bheap_empty(Queue *q);

//-queue.c----------------------------------------------------------------------

void queue_init(Queue *q)
{
	q->heap = malloc(16*sizeof(Task *));
	q->allocated = 16;
	q->length = 1;
}

/* binary heap stuff */
void queue_enqueue(Queue *q, Task *task) // insert
{
	if (q->allocated < q->length + 1)
	{
		q->heap = realloc(q->heap, q->allocated * 2 * sizeof(Task *));
		q->allocated *= 2;
	}

	q->length += 1;
	int index = q->length - 1;
	while (index > 1 && task->time < q->heap[index / 2]->time)
	{
		q->heap[index] = q->heap[index / 2];
		index /= 2;
	}
	q->heap[index] = task;
}

Task * bheap_pop(Queue *q)
{
	//assert (q->length - 1 > 0);
	Task * first = q->heap[1];
	Task * last = q->heap[1] = q->heap[q->length];
	q->length -= 1;
	if (q->length < 2) // no elements
		return first;
	int node_index = 1;
	while (node_index * 2 < q->length)  // until there is atleast one child
	{
		int child_index = node_index * 2;
		if (child_index + 1 < q->length && q->heap[child_index + 1] < q->heap[child_index])
			child_index++;
		if (q->heap[child_index] >= last)
			break;
		q->heap[node_index] = q->heap[child_index];
		node_index = child_index;
	}
	q->heap[node_index] = last;
	return first;
}

Task * bheap_top(Queue *q)
{
	return q->heap[1];
}

bool bheap_empty(Queue *q)
{
	return q->length < 2;
}

//-EOF-queue.c------------------------------------------------------------------

typedef struct
{
	float phase;
	int phase_location;
} Scene;


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

		if (best_fbc < 0 || (samp_buf && samples > best_num_samp))
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
	// FIXME: wait for MapNotify event

	return win;
}

void render(Scene *scene)
{
	static const float vertexArray[] =
		{
			 0,-1, 0, 1,
			 1, 1, 0, 1,
			-1, 1, 0, 1
		};

	glClearColor(0, 1, 0, 1);
	glClear(GL_COLOR_BUFFER_BIT);

	glUniform1f(scene->phase_location, scene->phase);

	glVertexAttribPointer(0, 4, GL_FLOAT, false, 0, vertexArray);
	glEnableVertexAttribArray(0);
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 3);
}

bool gametick(int64_t time, void *data)
{
	Task *task = data;
	task->time = time + 1000000000 / 30;
}

void run(Display *display, Window win)
{
	bool quit = false;
	GLuint shaderProgram;
	Scene scene;

	Queue tasks;
	queue_init(&tasks);
	Task gametick_task;
	gametick_task.time = 0;
	gametick_task.update = &gametick;
	gametick_task.ctx = NULL;
	queue_enqueue(&tasks, &gametick_task);

	int fd = XConnectionNumber(display);
	fd_set fdset;
	FD_ZERO(&fdset);

	shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, create_shader(GL_VERTEX_SHADER, vertexSrc));
	glAttachShader(shaderProgram, create_shader(GL_FRAGMENT_SHADER, fragmentSrc));
	glLinkProgram(shaderProgram);
	glUseProgram(shaderProgram);

	scene.phase_location = glGetUniformLocation(shaderProgram, "phase");
	if(scene.phase_location < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	int64_t prev_time = 0;
	int num_frames = 0;

	while (!quit)
	{
		struct timespec ts;
		int64_t now;
		Task *task;

		//bheap_empty(&tasks) || 
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

		if (bheap_empty(&tasks))
		{
			/// WAIT_FOR_EVENT
			FD_SET(fd, &fdset);
			pselect(fd+1, &fdset, NULL, NULL, NULL, NULL);
			continue;
		}

		clock_gettime(CLOCK_MONOTONIC, &ts);
		now = ts.tv_sec * 1000000000LL + ts.tv_nsec;

		if (now < bheap_top(&tasks)->time)
		{
			/// WAIT_FOR_EVENT_WITH_TIMEOUT
			struct timespec timeout;
			int64_t diff = bheap_top(&tasks)->time - now;
			timeout.tv_sec = diff / 1000000000LL;
			timeout.tv_nsec = diff % 1000000000LL;
			FD_SET(fd, &fdset);
			pselect(fd+1, &fdset, NULL, NULL, &timeout, NULL);
			continue;
		}

		task = bheap_pop(&tasks);
		if (!task->update(now, task))
		{
			queue_enqueue(&tasks, task);
		}

		scene.phase = fmodf(now*0.000000015f, 2 * 3.141f);
		render(&scene);
		glXSwapBuffers(display, win);

		num_frames++;
		if (now - prev_time > 1000000000LL)
		{
			int delta = (now - prev_time)/1000000000LL;
			printf("fps: %d (%d)\n", num_frames / delta, num_frames);
			num_frames = 0;
			prev_time = now;
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
