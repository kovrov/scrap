/*
There is an array of N integer elements (can be positive or negative).
Find the sequence of consecutive numbers that add up to a maximum (or highest)
total within the array. Write a function to find the sum and also the start
and end positions of the sequence. The solution should be of O(N) time complexity. 

For example if the array is (0, -1, 2, -1, 3, -1, 0), maximum sum would be
4 (= 2 + -1 + 3). Start position is 3 and end position is 5.  

*/


#include <stdio.h>
#include <assert.h>

struct MaxSum
{
	int start;
	int end;
	int sum;
};

MaxSum max_sum(int arr[], size_t n)
{
	assert (n > 1);

	/* in this aproach I'm trying to sum everything between positive
	   numbers ("peaks"), and return the best attempt */

	// initial set up
	int a = 0;
	int b = 1;
	int sum = arr[0] + arr[1];

	MaxSum ret; // could use out params, but return struct is more readeble
	ret.start = a;
	ret.end = b;
	ret.sum = sum;

	for (size_t i=b+1; i < n; i++)
	{
		if (arr[i] < 0)
		{
			sum += arr[i];
			b = i;
		}
		else if (arr[i] > 0) // in case of positive number - continue to sum or restart summing
		{
			if (arr[a] > 0 && sum + arr[i] > 0) // sum and save best attempt
			{
				sum += arr[i];
				b = i;
				if (sum > ret.sum)
				{
					ret.start = a;
					ret.end = b;
					ret.sum = sum;
				}
			}
			else  // there's no point to sum further, need to start new attempt
			{
				// save if needed
				if (sum > ret.sum)
				{
					ret.start = a;
					ret.end = b;
					ret.sum = sum;
				}
				// restart if possible
				if (i < n)
				{
					sum = arr[i];
					a = i;
				}
			}

		}
	}
	return ret;
}


int main(int argc, char* argv[])
{
	int n;
	MaxSum ret;

	int array1[] = {0, -1, 2, -1, 3, -1, 0};
	n = sizeof(array1)/sizeof(int);
	ret = max_sum(array1, n);
	printf("sum:%d [%d:%d]\n", ret.sum, ret.start+1 , ret.end+1); // 4 (2 + -1 + 3), start 3, end 5

	int array2[] = {0, 2, -2, -1, -3, 1, 0, 4, 1};
	n = sizeof(array2)/sizeof(int);
	ret = max_sum(array2, n);
	printf("sum:%d [%d:%d]\n", ret.sum, ret.start+1 , ret.end+1); // 6 (1 + 0 + 4 + 1) start 6, end 9

	int array3[] = {0, -2, 2, -4, 3, -3, -2};
	n = sizeof(array3)/sizeof(int);
	ret = max_sum(array3, n);
	printf("sum:%d [%d:%d]\n", ret.sum, ret.start+1 , ret.end+1); // 1 (2 + -4 + 3) start 3, end 5

	int array4[] = {2, -1, 2, -1, 3};
	n = sizeof(array4)/sizeof(int);
	ret = max_sum(array4, n);
	printf("sum:%d [%d:%d]\n", ret.sum, ret.start+1 , ret.end+1); // 5 (2 + -1 + 2 + -1 + 3) start 1, end 5

	int array5[] = {0, -1, 2, -4, 3, -3, 2};
	n = sizeof(array5)/sizeof(int);
	ret = max_sum(array5, n);
	printf("sum:%d [%d:%d]\n", ret.sum, ret.start+1 , ret.end+1); // 1 (0 + -1 + 2) start 1, end 3
	                                                           // or 1 (2 + -4 + 3) start 3, end 5
	                                                           // or 1 (3 + -3 + 2) start 5, end 7

	/* ok, corner cases I do not have yet solutions for. */

	//FIXME: failing - one of "peak" numbers involved is zero
	int array6[] = {0, -1, 2, -4, 2, -3, -2};
	n = sizeof(array6)/sizeof(int);
	ret = max_sum(array6, n);
	printf("sum:%d [%d:%d]\n", ret.sum, ret.start+1 , ret.end+1); // 1 (0 + -1 + 2) start 1, end 3
	return 0;
	//FIXME: not even thought of - all numbers involved are negative
	int array7[] = {0, -1, -2, -4, -2, -3, -2};
	n = sizeof(array7)/sizeof(int);
	ret = max_sum(array7, n);
	printf("sum:%d [%d:%d]\n", ret.sum, ret.start+1 , ret.end+1); // OMG!
	return 0;
}

