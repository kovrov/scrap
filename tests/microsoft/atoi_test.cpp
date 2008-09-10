/*
	Convert integer to string representation 

	Write a function to convert an integer n into its ASCII string
	representation for a given base
	
	The function must be implemented in a portable way that covers
	all possible values of n, and all bases between 2 and 16. 

	You are not allowed to use any library functions (given that this
	is a function that is included in the standard C library). 

		char* itoa(int n, int base) 
		{ 
			//   e.g. itoa(123, 10) returns the null-terminated 
			//   string "123"
			...
		} 

	If you would like to implement the solution in C#, consider the following signature: 

		public string itoa(int n, int base);
*/



/* this function will allocate memory for string
   releasing is responsobility of caller */
char* itoa(int n, int base)
{
	if (base < 2 || base > 16)
	{
		throw "invalid base"; // TODO: make up something better
	}

	static char digits[] = "0123456789ABCDEF";
	size_t size = sizeof (int) * 8; // size of buffer for base 2 representation
	// I could use static buffer as well...
	char* buff = new char[size]; // i do not check for null as new should throw in case of memory error
	
	int len = 0;
	bool negative = false;
	if (n < 0)
	{
		negative = true;
		n = 0 - n; // I could shift, but not sure about other platforms (endianess)
	}

	while (base + n > base)
	{
		int i = n % base;
		buff[len++] = digits[i];
		n -= i;
		n /= base;
	}

	if (negative)
		buff[len++] = '-';

	// reverse the string - is the first comes to my mind, and i do not have much time for better solution ...
	int half_len = len/2;
	for (int i=0; i < half_len; i++)
	{
		// swap
		char tmp = buff[i];
		buff[i] = buff[len-1-i];
		buff[len-1-i] = tmp;
	}

	buff[len] = '\0';
	return buff;
}


int _tmain(int argc, _TCHAR* argv[])
{
	try
	{
		char* str = itoa(-15, 2);
		printf("%s\n", str);
		delete str;

		str = itoa(-15, 8);
		printf("%s\n", str);
		delete str;

		str = itoa(-15, 16);
		printf("%s\n", str);
		delete str;
	}
	catch (...)
	{
		// something happenned
	}

	return 0;
}

