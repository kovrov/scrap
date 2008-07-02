#include <vector>
#include <algorithm>
#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
	vector<int> vec1(5, 5);
	vector<int> vec2(10, 10);

	copy(vec2.begin(), vec2.end(), back_inserter(vec1));

	for (vector<int>::iterator it=vec1.begin(); it != vec1.end(); it++)
		cout << *it << ' ';
	cout << endl;
	

	return 0;
}
