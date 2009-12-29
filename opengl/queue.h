#ifndef QUEUE_H
#define QUEUE_H


#include <stdbool.h>
#include <stdint.h>

typedef struct task_tag Task;

typedef bool (*TaskCB)(Task *, int64_t);

struct task_tag
{
	int64_t time;
	TaskCB update;
	void* ctx;
};

typedef struct queue_tag Queue;

Queue * queue_new();
void    queue_free(Queue *);
void    queue_insert(Queue *q, Task *task);
Task *  queue_pop(Queue *q);
Task *  queue_top(Queue *q);
bool    queue_is_empty(Queue *q);


#endif
