#include <iostream>
#include <assert.h>

#define STACK_SIZE 1024

class Queue
{
	friend void print_queue(const Queue& q); // for testing

	char in_stack[STACK_SIZE];
	int in_marker;
	char out_stack[STACK_SIZE];
	int out_marker;
public:
	Queue()
	{
		in_marker = out_marker = -1; // empty
	}
	void push(char c)
	{
		if (out_marker == STACK_SIZE-1)
			throw "queue is full";

		// pour existing values from out_stack into in_stack
		for (int i = 0; i <= out_marker; i++)
			in_stack[++in_marker] = out_stack[i];
		out_marker = -1;

		// put new value on top of in_stack
		in_stack[++in_marker] = c;

		// pour queue back into out_stack 
		for (int i = 0; i <= in_marker; i++)
			out_stack[++out_marker] = in_stack[i];
		in_marker = -1;
	}
	char pop()
	{
		if (out_marker < 0)
			throw "pop from empty queue";
		return out_stack[out_marker--];
	}
};

void print_queue(const Queue& q)
{
	for (int i = 0; i <= q.out_marker; i++)
		std::cout << q.out_stack[i];
	std::cout << std::endl;
}

int main(int argc, char* argv[])
{
	Queue q;
	q.push('1');
	q.push('2');
	q.pop();
	q.push('3');
	q.push('4');
	q.push('5');
	print_queue(q);
	return 0;	
}
