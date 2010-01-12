#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <fcntl.h>
#include <unistd.h>
#include <time.h>

#include <assert.h>

#include "game.h"
#include "scene.h"

#define $_DBG_FN printf("### %s\n", __FUNCTION__);

#define GAME_GRID_HEIGHT 22
#define GAME_GRID_WIDTH 10


enum SHAPE {I, J, L, O, S, T, Z};
enum TASK { TASK_SPAWN_BLOCK, TASK_GRAVITY_TICK, TASK_LOCK_PIECE, TASKS_COUNT };

const int blocks_bits[] = {
	0x00F0, 0x4444, 0x2222, 0x0F00,  // I
	0x003C, 0x0093, 0x0078, 0x0192,  // J
	0x0039, 0x00D2, 0x0096, 0x0138,  // L
	0x000F, 0x000F, 0x000F, 0x000F,  // O
	0x0033, 0x005A, 0x0198, 0x00B4,  // S
	0x003A, 0x009A, 0x00B8, 0x00B2,  // T
	0x001E, 0x0099, 0x00F0, 0x0132}; // Z

static bool spawn_block(Task *, int64_t);
static bool gravity_tick(Task *, int64_t);
static bool lock_piece(Task *, int64_t);

typedef struct Tetromino_tag Tetromino;
struct Tetromino_tag
{
	enum SHAPE shape_id;
	int rotation_bits[4];
	int rotation_bits_size;
	int rotation_state;
	int x, y;
};

struct GameState_tag
{
	Tetromino *block;
	int next_shape;
	bool is_over;
	Task tasks[TASKS_COUNT];
	Queue *scheduler;

	Scene *scene;
	SceneItem *block_item;
	SceneItem *grid_item;

	int *grid; // width*height
};



static const TaskCB task_callbacks[TASKS_COUNT] = { &spawn_block, &gravity_tick, &lock_piece };

static
uint32_t random_uint()
{
	static unsigned long seed = 0;
	if (seed == 0)
	{
		int fd = open("/dev/urandom", 0);
		if (fd == -1 || read(fd,  &seed, sizeof(seed)) == -1)
			seed = time(0);
		if (fd >= 0)
			close(fd);
		srandom(seed);
	}

	return (uint32_t)random();
}

static
bool game_grid_collide(GameState *game, Tetromino *block)
{
	if (block->y < 0)
		return true;
	return false;
}

GameState *game_new(Queue *scheduler, Scene *scene)
{
	int i;
	GameState *game = malloc(sizeof(GameState));
	game->scheduler = scheduler;

	game->block = NULL;
	game->is_over = false;
	for (i=0; i<TASKS_COUNT; i++)
	{
		game->tasks[i].update = task_callbacks[i];
		game->tasks[i].ctx = game;
	}
	game->next_shape = random_uint() % 7;
	game->grid = malloc(GAME_GRID_WIDTH * GAME_GRID_HEIGHT);
	memset(game->grid, -1, GAME_GRID_WIDTH * GAME_GRID_HEIGHT);

	game->scene = scene;
	scene_scale(game->scene, 16.0);
	game->block_item = scene_item_new();
	scene_add_item(game->scene, game->block_item);
//	game->grid_item = scene_item_new();
//	scene_add_item(game->scene, game->grid_item);

	return game;
}

void game_free(GameState *game)
{
	free(game->grid);
	free(game);
}

void game_restart(GameState *game)
{
	//TODO: countdown
	Task *task = &game->tasks[TASK_SPAWN_BLOCK];
	task->time = 0;
	queue_insert(game->scheduler, task);
}

static
Tetromino * game_next_block(GameState *game)
{
	static Tetromino blocks[7] = {
		{I, {0x00F0, 0x4444, 0x2222, 0x0F00}, 4, 0, 5, 20},
		{J, {0x003C, 0x0093, 0x0078, 0x0192}, 3, 0, 5, 20},
		{L, {0x0039, 0x00D2, 0x0096, 0x0138}, 3, 0, 5, 20},
		{O, {0x000F, 0x000F, 0x000F, 0x000F}, 2, 0, 5, 20},
		{S, {0x0033, 0x005A, 0x0198, 0x00B4}, 3, 0, 5, 20},
		{T, {0x003A, 0x009A, 0x00B8, 0x00B2}, 3, 0, 5, 20},
		{Z, {0x001E, 0x0099, 0x00F0, 0x0132}, 3, 0, 5, 20}};
	Tetromino *block = &blocks[game->next_shape];
	game->next_shape = random_uint() % 7;

	block->x = GAME_GRID_WIDTH;
	block->y = GAME_GRID_HEIGHT;

	return block;
}

static
void game_update_block_item(SceneItem *item, Tetromino *block)
{ $_DBG_FN
	int i;
	scene_item_reset(item);
	for (i=0; i < block->rotation_bits_size * block->rotation_bits_size; i++)
	{
		int bit = block->rotation_bits[block->rotation_state] & 1 << i;
		if (!bit)
			continue;
		int x = i % block->rotation_bits_size;
		int y = i / block->rotation_bits_size;
		RGBA color = 0xFFFFFFFF;
		scene_item_add_rect(item, (float)block->x + x, (float)block->y + y, 1,1, color);
	}
}

/* tasks */
static
bool spawn_block(Task *task, int64_t now)
{ $_DBG_FN
	GameState *game = task->ctx;

	assert (game->block == NULL);
	game->block = game_next_block(game);

	if (game_grid_collide(game, game->block))
	{
		printf("    [ game over ]\n");
		return true;
	}

	game_update_block_item(game->block_item, game->block);

	Task *gravity_task = &game->tasks[TASK_GRAVITY_TICK];
	gravity_task->time = now + 1000000000;
	queue_insert(game->scheduler, gravity_task);
	return true;
}

static
bool gravity_tick(Task *task, int64_t now)
{ $_DBG_FN
	GameState *game = task->ctx;
	game->block->y--;

	game_update_block_item(game->block_item, game->block);

	if (game_grid_collide(game, game->block))
	{
		Task *lock_task = &game->tasks[TASK_LOCK_PIECE];
		lock_task->time = now + 1000000000;
		queue_insert(game->scheduler, lock_task);
		return true;
	}
	else
	{
		task->time = now + 1000000000;
		return false;
	}
}

static
bool lock_piece(Task *task, int64_t now)
{ $_DBG_FN
	GameState *game = task->ctx;

	Task *spawn_task = &game->tasks[TASK_SPAWN_BLOCK];
	spawn_task->time = now + 1000000000;
	queue_insert(game->scheduler, spawn_task);
	return true;
}
