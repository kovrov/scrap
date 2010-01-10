#include <stdlib.h>
#include "queue.h"


struct queue_tag
{
	Task **heap;
	size_t allocated;
	size_t length;
};

Queue * queue_new()
{
	Queue *q = NULL;
	q = malloc(sizeof(Queue));
	q->heap = malloc(16*sizeof(Task *));
	q->allocated = 16;
	q->length = 1;
	return q;
}

void queue_free(Queue *q)
{
	free(q->heap);
	q->allocated = -1;
	q->length = -1;
	q->heap = NULL;
	free(q);
}


/* binary heap stuff */
void queue_insert(Queue *q, Task *task)
{
	int index;
	if (q->allocated < q->length + 1)
	{
		q->heap = realloc(q->heap, q->allocated * 2 * sizeof(Task *));
		q->allocated *= 2;
	}

	q->length += 1;
	index = q->length - 1;
	while (index > 1 && task->time < q->heap[index / 2]->time)
	{
		q->heap[index] = q->heap[index / 2];
		index /= 2;
	}
	q->heap[index] = task;
}

Task * queue_pop(Queue *q)
{
	/* assert (q->length - 1 > 0); */
	unsigned node_index;
	Task * first = q->heap[1];
	Task * last = q->heap[1] = q->heap[q->length];
	q->length -= 1;
	if (q->length < 2) /* no elements */
		return first;
	node_index = 1;
	while (node_index * 2 < q->length)  /* until there is atleast one child */
	{
		unsigned child_index = node_index * 2;
		if (child_index + 1 < q->length && q->heap[child_index + 1] < q->heap[child_index])
			child_index++;
		if (q->heap[child_index] >= last)
			break;
		q->heap[node_index] = q->heap[child_index];
		node_index = child_index;
	}
	q->heap[node_index] = last;
	return first;
}

Task * queue_top(Queue *q)
{
	return q->heap[1];
}

bool queue_is_empty(Queue *q)
{
	return q->length < 2;
}

