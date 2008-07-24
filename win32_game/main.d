/* cool name - "project scarcity" or "scarcity engine" */
/*
	http://en.wikipedia.org/wiki/Game_programming#The_game_loop
	http://www.mvps.org/directx/articles/writing_the_game_loop.htm
	http://msdn2.microsoft.com/library/bb203873
	http://msdn2.microsoft.com/library/microsoft.xna.framework.game.tick

	//initialize
	//update
	//draw
*/

module main;

static import system;
static import game;  // hm...


// game-tick callback
void gameTick()
{
	//global hotkeys
	if (system.input.keyboard[system.KEY.ESCAPE])
		system.exit();
	if (system.input.keyboard[system.KEY.ENTER] && system.input.keyboard[system.KEY.ALT])
	{
		system.input.keyboard[system.KEY.ENTER] = false;
		system.window.fullscreen = !system.window.fullscreen;
	}	

	//throw new Exception("not implemented");
	game.updateScene();
		// run AI
		// move enemies
		// resolve collisions
	game.drawScene();
	//play_sounds();
}


int main()
{
	// initail valuse
	system.window.title = "my stupid game";
	system.window.size(800, 600);
	system.window.fullscreen = false;
	system.window.resizable = true;
	system.window.trap_cursor= false;

	/* client api
	system.timer.total;
	system.timer.game;
	system.timer.frame;
	system.timer.pause;

	system.input.mouse;
	system.input.keyboard;

	system.active;
	system.exit(-1);
	*/

	return system.run(&gameTick);
}
