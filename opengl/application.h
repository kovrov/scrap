#ifndef APPLICATION_H
#define APPLICATION_H

#include <stdbool.h>
#include "queue.h"


typedef struct application_tag Application;

typedef bool (*RenderCB)(void *data);


Application * application_new(const char *title);

void application_free(Application *app);

void application_run(Application *app, RenderCB render, void *scene);

Queue * application_tasks(Application *app);

#endif
