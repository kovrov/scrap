
#include <iostream>
#include <assert.h>


struct Node
{
	char* value;
	Node* next;
};

void swap(Node** first, Node* left, Node* right)
{
	assert (first != NULL && left != NULL && right != NULL);

	Node* pre_left = NULL;
	Node* pre_right = NULL;
	Node* post_left = left->next;
	Node* post_right = right->next;

	/* assuming the list is not circular */
	Node* current = *first;
	while (current != NULL)
	{
		if (current->next == left)
			pre_left = current;
		if (current->next == right)
			pre_right = current;
		current = current->next;
	}

	if (pre_left && pre_left != right)
		pre_left->next = right;

	if (post_right == left)
		left->next = right;
	else
		left->next = post_right;

	if (pre_right && pre_right != left)
		pre_right->next = left;

	if (post_left == right)
		right->next = left;
	else
		right->next = post_left;

	if (*first == left)
		*first = right;
	else if (*first == right)
		*first = left;
}


// test

void print_llist(Node* first)
{
	Node* current = first;
	while (current != NULL)
	{
		std::cout << current->value;
		current = current->next;
	}
	std::cout << std::endl;
}

void reset_llist(Node* nodes, size_t len)
{
	for (size_t i = 1; i < len;  i++)
		nodes[i-1].next = &nodes[i];
	nodes[len-1].next = NULL;
}

int main(int argc, char* argv[])
{
	Node nodes[5] = {{"0"}, {"1"}, {"2"}, {"3"}, {"4"}};

	reset_llist(nodes, 5);
	Node* first = nodes;
	swap(&first, &nodes[0], &nodes[1]);
	std::cout << "0<=>1 (10234) == ";
	print_llist(first);

	reset_llist(nodes, 5);
	first = nodes;
	swap(&first, &nodes[0], &nodes[2]);
	std::cout << "0<=>2 (21034) == ";
	print_llist(first);

	reset_llist(nodes, 5);
	first = nodes;
	swap(&first, &nodes[0], &nodes[4]);
	std::cout << "0<=>4 (41230) == ";
	print_llist(first);

	reset_llist(nodes, 5);
	first = nodes;
	swap(&first, &nodes[1], &nodes[2]);
	std::cout << "1<=>2 (02134) == ";
	print_llist(first);

	reset_llist(nodes, 5);
	first = nodes;
	swap(&first, &nodes[1], &nodes[3]);
	std::cout << "1<=>3 (03214) == ";
	print_llist(first);

	reset_llist(nodes, 5);
	first = nodes;
	swap(&first, &nodes[2], &nodes[4]);
	std::cout << "2<=>4 (01432) == ";
	print_llist(first);

	reset_llist(nodes, 5);
	first = nodes;
	swap(&first, &nodes[3], &nodes[4]);
	std::cout << "3<=>4 (01243) == ";
	print_llist(first);

	return 0;
}

