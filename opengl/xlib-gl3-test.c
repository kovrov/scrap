/* gcc xlib-gl3-test.c application.c queue.c -lGL -lm -o xlib-gl3-test
 * http://opengl.org/wiki/Tutorial:_OpenGL_3.0_Context_Creation_(GLX) */

#include "application.h"
#include "queue.h"

#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#include <math.h>


#define GL_GLEXT_PROTOTYPES 1
#define GLX_GLXEXT_PROTOTYPES 1
#include <GL/gl.h>



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

Scene * scene_new()
{
	Scene *scene = NULL;
	GLuint shaderProgram;

	shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, create_shader(GL_VERTEX_SHADER, vertexSrc));
	glAttachShader(shaderProgram, create_shader(GL_FRAGMENT_SHADER, fragmentSrc));
	glLinkProgram(shaderProgram);

	scene = malloc(sizeof(Scene));
	glUseProgram(shaderProgram);
	scene->phase_location = glGetUniformLocation(shaderProgram, "phase");
	if(scene->phase_location < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}
	return scene;
}

void scene_free(Scene *scene)
{
	free(scene);
}

void render(void *data)
{
	static const float vertexArray[] =
		{
			 0,-1, 0, 1,
			 1, 1, 0, 1,
			-1, 1, 0, 1
		};
	Scene *scene = data;

	glClearColor(0, 1, 0, 1);
	glClear(GL_COLOR_BUFFER_BIT);

	glUniform1f(scene->phase_location, scene->phase);

	glVertexAttribPointer(0, 4, GL_FLOAT, false, 0, vertexArray);
	glEnableVertexAttribArray(0);
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 3);
}

bool gametick(int64_t time, Task *task)
{
	Scene *scene = task->ctx;

	scene->phase = fmodf(time * 0.000000015f, 2 * 3.141f);
	task->time = time + 1000000000 / 30;

	return false;
}

int main(int argc, char **argv)
{
	Application *app = NULL;
	Scene *scene = NULL;
	Task gametick_task;

	app = application_new("OpenGL application");
	scene = scene_new();  // a gl context have to be created at this point!

	gametick_task.time = 0;
	gametick_task.update = &gametick;
	gametick_task.ctx = scene;
	queue_insert(application_tasks(app), &gametick_task);

	application_run(app, &render, scene);

	application_free(app);
	scene_free(scene);

	return 0;
}
