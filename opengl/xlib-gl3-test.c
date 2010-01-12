/* gcc xlib-gl3-test.c game.c application.c scene.c queue.c -lGL -lm -o xlib-gl3-test -g -W -pedantic
 * http://opengl.org/wiki/Tutorial:_OpenGL_3.0_Context_Creation_(GLX) */

#include <stdlib.h>
#include <stdio.h>

#include "application.h"
#include "queue.h"
#include "game.h"
#include "scene.h"


int main(int argc, char **argv)
{
	Application *app;
	Scene *scene;
	GameState *game;
	ViewPort view_port;

	app = application_new("OpenGL application");
	scene = scene_new();  /* a gl context have to be created at this point! */
	game = game_new(application_tasks(app), scene);
	game_restart(game);

	view_port.self = scene;
	view_port.render = (RenderCB)&scene_render;
	view_port.resize = (ResizeCB)&scene_resize;

	application_run(app, &view_port);

	application_free(app);
	scene_free(scene);
	game_free(game);

	return 0;
}
