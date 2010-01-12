#ifndef APPLICATION_H
#define APPLICATION_H

#include <stdbool.h>
#include "queue.h"


typedef struct application_tag Application;
typedef struct ViewPort_tag ViewPort;
typedef bool (*RenderCB)(void *);
typedef void (*ResizeCB)(void *, int, int);

struct ViewPort_tag
{
	void *self;
	RenderCB render;
	ResizeCB resize;
};

Application * application_new(const char *);

void application_free(Application *);

void application_run(Application *, ViewPort *);

Queue * application_tasks(Application *);

#endif
