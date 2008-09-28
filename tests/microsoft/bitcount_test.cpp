/*

Given an integer number as a parameter, write a function to count the number
of "1" or set bits in the number. For example if input is 7, your code should
output 3 since the binary representation of 7 is 0111.  

*/



#include <stdio.h>
#include <assert.h>


int count_bits(int n)
{
	int count = 0;
	for (int i = 0; i < sizeof(int)*8; i++) // hope you dont mind the "sizeof" in the loop..
	{
		//printf("%d", (n >> i) & 1);
		if (n >> i)
			count++;
	}
	//printf("\n");
	return count;
}

int main(int argc, char* argv[])
{
	assert (count_bits(7) == 3);
	return 0;
}

