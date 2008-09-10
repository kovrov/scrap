/*
	Find k-th largest element in array 

	1.	Given a very large array of n integers, find the k-th largest value
		in the array efficiently. You may assume that k is much smaller
		than n. Specifically, write the following function: 
		 
		int kthLargest(int n, int *array, int k);
		 
		Note that 1 <= k, thus if the function is called with k=1 it should
		return the largest value in the array. The function should not count
		duplicate values in the array multiple times, e.g. the third largest
		(k=3) of [1,3,2,2] is 1, not 2. 
		 
	2.	Explain what the running time and the memory usage of your function
		is as a function of n, the number of elements of the array. 

	For instance, consider the following call: 

		int array[] = {220,14,73,19,1,3,100,55,12,7,100,44,99}; 
		int n = sizeof(array)/sizeof(int); 
		kthLargest(n, array, 1); // returns 220 
		kthLargest(n, array, 2); // returns 100 
		kthLargest(n, array, 3); // returns 99 

	You are not allowed to use any library functions. 

	Hint: you are allowed to modify the array inside your function if you'd
	like to, although that is not strictly necessary.  

	If you would like to implement the solution in C#, consider the following
	signature: 

		public int kthLargest(int[] array, int k);
*/


/*

mem usage is only few variables - two int to search results, and another two
for loops.

runningtime complexity (I believe) is O(n*k).

there is other possible solution to sort array removing duplicates, and then
just return k'th element of resulted array.

*/

int kthLargest(int n, int *array, int k)
{
	int top;
	int prev_top = 0x7FFFFFFF; // FIXME: hack - platform dependant biggest int
	for (int i=0; i < k; i++)
	{
		top = -0x7FFFFFFF; // FIXME: hack - platform dependant smallest int;
		for (int j=0; j<n; j++)
		{
			if (array[j] > top)
			{
				if (array[j] < prev_top)
					top = array[j];
			}
		}
		prev_top = top;
	}

	return top;
}


int _tmain(int argc, _TCHAR* argv[])
{
	int array[] = {220,14,73,19,1,3,100,55,12,7,100,44,99}; 
	int n = sizeof(array)/sizeof(int); 
	printf("%d\n", kthLargest(n, array, 1)); // returns 220 
	printf("%d\n", kthLargest(n, array, 2)); // returns 100 
	printf("%d\n", kthLargest(n, array, 3)); // returns 99 
	printf("%d\n", kthLargest(n, array, 12)); // returns 1

	return 0;
}

