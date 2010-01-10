#ifndef SCENE_H
#define SCENE_H

#include <stdbool.h>

typedef unsigned RGBA;

typedef struct SceneItem_tag SceneItem;

typedef struct Scene_tag Scene;

Scene * scene_new();
void scene_free(Scene *scene);
bool scene_render(Scene *scene);
void scene_add_item(Scene *, SceneItem *);
void scene_scale(Scene *, float);


SceneItem * scene_item_new();
void scene_item_free(SceneItem *item);
void scene_item_reset(SceneItem *);
void scene_item_add_rect(SceneItem *, float, float, float, float, RGBA);

#endif
