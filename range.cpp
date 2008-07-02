
#include <vector>
#include <algorithm>

#include <iostream>

struct IncrementNumber
{
	int current;
	IncrementNumber(int number=0) { current = number; }
	int operator()() { return current++; }
};




int main()
{
	std::vector<int> vect(10);
	std::generate_n(vect.begin(), vect.size(), IncrementNumber());
	//for (int i=0; i < vect.size(); i++) vect[i] = i;

	for (std::vector<int>::iterator it=vect.begin(); it!=vect.end(); ++it)
		std::cout << *it << " ";
	std::cout << std::endl;
	return 0;
}
