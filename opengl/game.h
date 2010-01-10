#ifndef GAME_H
#define GAME_H

#include "queue.h"
#include "scene.h"


typedef struct GameState_tag GameState;


GameState *game_new(Queue *, Scene *);
void game_free(GameState *);
void game_restart(GameState *);


#endif
