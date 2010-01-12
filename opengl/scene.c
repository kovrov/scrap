#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>

#define GL_GLEXT_PROTOTYPES 1
#define GLX_GLXEXT_PROTOTYPES 1
#include <GL/gl.h>

#include "matrix.h"
#include "scene.h"


#define $_DBG_FN printf("### %s\n", __FUNCTION__);


const char* vertexSrc =
	"uniform mat4 u_matrix;"
	"uniform mat4 u_projection_matrix;"
	"attribute vec2 a_position;"
	"attribute vec3 a_color;"

	"varying vec3 color;"

	"void main()"
	"{"
		"vec4 position;"
		"position.xy = a_position;"
		"position.z = 0.0;"
		"position.w = 1.0;"
		"gl_Position = u_matrix * position;"
		"gl_Position = u_projection_matrix * gl_Position;"

		"color = a_color;"
	"}";
const char* fragmentSrc =
	"varying vec3 color;"
	"void main()"
	"{"
		"gl_FragColor.rgb = color;"
	"}";

int g_vertices_index;
int g_color_index;


static
void log_shader_info(GLuint shader)
{
	GLint length;
	glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &length);
	if (length)
	{
		GLint success;
		char* buffer = malloc(length * sizeof(char));
		glGetShaderInfoLog(shader, length, NULL, buffer);
		printf("ShaderInfoLog: %s\n", buffer);
		free(buffer);
		glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
		if (success != GL_TRUE)
		{
			printf("shader GL_COMPILE_STATUS fail\n");
			exit(1);
		}
	}
}

static
GLuint create_shader(GLenum type, const char* pSource)
{
	GLuint shader = glCreateShader(type);
	glShaderSource(shader, 1, &pSource, NULL);
	glCompileShader(shader);
	log_shader_info(shader);
	return shader;
}


static void scene_item_draw(SceneItem *);


struct Scene_tag
{
	SceneItem *block_item;
	SceneItem *grid_item;
	Matrix modelview_matrix;
	Matrix projection_matrix;
	int matrix_location;
	int projection_matrix_location;
};


Scene * scene_new()
{
	Scene *scene = NULL;
	GLuint shaderProgram;

	shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, create_shader(GL_VERTEX_SHADER, vertexSrc));
	glAttachShader(shaderProgram, create_shader(GL_FRAGMENT_SHADER, fragmentSrc));
	glLinkProgram(shaderProgram);
	glUseProgram(shaderProgram);

	scene = malloc(sizeof(Scene));
	scene->matrix_location = glGetUniformLocation(shaderProgram, "u_matrix");
	if(scene->matrix_location < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	scene->projection_matrix_location = glGetUniformLocation(shaderProgram, "u_projection_matrix");
	if(scene->projection_matrix_location < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	g_vertices_index = glGetAttribLocation(shaderProgram, "a_position");
	if(g_vertices_index < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	g_color_index = glGetAttribLocation(shaderProgram, "a_color");
	if(g_color_index < 0)
	{
		printf("Unable to get uniform location\n");
		exit(1);
	}

	scene->block_item = NULL;///scene_item_new();
	scene->grid_item = scene_item_new();

	// identity
	matrix_init_identity(&scene->modelview_matrix);
	printf("* BEFORE!\n");

	return scene;
}


void scene_free(Scene *scene)
{
	///scene_item_free(scene->block_item);
	scene_item_free(scene->grid_item);
	free(scene);
}

void scene_resize(Scene *scene, int width, int height)
{
	//scene->world_scale = 1.0 / (width > height ? width : height);

	glViewport(0, 0, width, height);

	matrix_init_ortho(&scene->projection_matrix, 0.0, width, 0.0, height, -1.0, 1.0);
	//matrix_init_identity(&scene->projection_matrix);
	printf("* AFTER?!\n");

	//matrix_op_mul(&scene->projection_matrix, &scene->projection_matrix, &scene->modelview_matrix);
}

bool scene_render(Scene *scene)
{ $_DBG_FN
	glClearColor(0, 1, 0, 1);
	glClear(GL_COLOR_BUFFER_BIT);

	glUniformMatrix4fv(scene->matrix_location, 1, GL_FALSE, (GLfloat*)&scene->modelview_matrix);
	glUniformMatrix4fv(scene->projection_matrix_location, 1, GL_FALSE, (GLfloat*)&scene->projection_matrix);

	scene_item_draw(scene->block_item);

	return true;
}

void scene_add_item(Scene *scene, SceneItem *item)
{
	///TEMP!!!
	scene->block_item = item;
}

void scene_scale(Scene *scene, float scale)
{
	//glScalef(scale, scale, scale);
	matrix_mul_f(&scene->modelview_matrix, &scene->modelview_matrix, scale);
}


/* Scene Item */

#define VERTEX_POS_SIZE        2   // x, y
#define VERTEX_COLOR_SIZE      3   // r, g, b

struct Vertex_tag { float x,y, r,g,b; };

struct SceneItem_tag
{
	struct Vertex_tag *vertices;
	int vertices_size;
	int vertices_preallocated;
};

SceneItem * scene_item_new()
{
	SceneItem *item = malloc(sizeof(SceneItem));
	// TODO: guess reasonable defaults
	item->vertices = NULL;
	item->vertices_preallocated = 0;
	scene_item_reset(item);
	return item;
}

void scene_item_free(SceneItem *item)
{
	free(item->vertices);
	free(item);
}

void scene_item_reset(SceneItem *item)
{
	item->vertices_size = 0;
}

void scene_item_add_rect(SceneItem *item, float x, float y, float w, float h, RGBA color)
{ $_DBG_FN
	int size = 6;

printf("    x:%g y:%g w:%g h:%g\n", x, y, w, h);

	if (item->vertices_preallocated < item->vertices_size + size)
	{
		item->vertices = realloc(item->vertices, sizeof(struct Vertex_tag)*(item->vertices_size + size));
		item->vertices_preallocated = item->vertices_size + size;
	}

	float r = (color & 0xFF) / 255.0;
	float g = (color & 0xFF << 8 >> 8) / 255.0;
	float b = (color & 0xFF << 16 >> 16) / 255.0;
//printf("    r:%g g:%g b:%g\n", r, g, b);

	item->vertices[item->vertices_size + 0].x = x;
	item->vertices[item->vertices_size + 0].y = y;
	item->vertices[item->vertices_size + 0].r = r;
	item->vertices[item->vertices_size + 0].g = g;
	item->vertices[item->vertices_size + 0].b = b;

	item->vertices[item->vertices_size + 1].x = x + w;
	item->vertices[item->vertices_size + 1].y = y;
	item->vertices[item->vertices_size + 1].r = r;
	item->vertices[item->vertices_size + 1].g = g;
	item->vertices[item->vertices_size + 1].b = b;

	item->vertices[item->vertices_size + 2].x = x;
	item->vertices[item->vertices_size + 2].y = y + h;
	item->vertices[item->vertices_size + 2].r = r;
	item->vertices[item->vertices_size + 2].g = g;
	item->vertices[item->vertices_size + 2].b = b;

	item->vertices[item->vertices_size + 3].x = x;
	item->vertices[item->vertices_size + 3].y = y + h;
	item->vertices[item->vertices_size + 3].r = r;
	item->vertices[item->vertices_size + 3].g = g;
	item->vertices[item->vertices_size + 3].b = b;

	item->vertices[item->vertices_size + 4].x = x + w;
	item->vertices[item->vertices_size + 4].y = y;
	item->vertices[item->vertices_size + 4].r = r;
	item->vertices[item->vertices_size + 4].g = g;
	item->vertices[item->vertices_size + 4].b = b;

	item->vertices[item->vertices_size + 5].x = x + w;
	item->vertices[item->vertices_size + 5].y = y + h;
	item->vertices[item->vertices_size + 5].r = r;
	item->vertices[item->vertices_size + 5].g = g;
	item->vertices[item->vertices_size + 5].b = b;

	item->vertices_size += size;
}

static
void scene_item_draw(SceneItem *item)
{ $_DBG_FN
	assert(item->vertices_size > 0);

	// position is vertex attribute 0
	glVertexAttribPointer(g_vertices_index, VERTEX_POS_SIZE, GL_FLOAT, GL_FALSE,
						  sizeof(struct Vertex_tag), &item->vertices->x);
	// color is vertex attribute 1
	glVertexAttribPointer(g_color_index, VERTEX_COLOR_SIZE, GL_FLOAT, GL_FALSE,
						  sizeof(struct Vertex_tag), &item->vertices->r);

	glEnableVertexAttribArray(g_vertices_index);
	glEnableVertexAttribArray(g_color_index);

	glDrawArrays(GL_TRIANGLES, 0, item->vertices_size);
}
