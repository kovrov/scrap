#ifndef QUEUE_H
#define QUEUE_H


#include <stdbool.h>
#include <stdint.h>

typedef bool (*TaskCB)(int64_t, void *);

typedef struct
{
	int64_t time;
	TaskCB update;
	void* ctx;
} Task;

typedef struct queue_tag Queue;

Queue * queue_new();
void    queue_free(Queue *);
void    queue_insert(Queue *q, Task *task);
Task *  queue_pop(Queue *q);
Task *  queue_top(Queue *q);
bool    queue_is_empty(Queue *q);


#endif
