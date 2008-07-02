#include <stdio.h>
#include <tchar.h>


// generator/continuation for C++
// author: Andrew Fedoniouk @ terrainformatica.com
// idea borrowed from: "coroutines in C" Simon Tatham,
//                     http://www.chiark.greenend.org.uk/~sgtatham/coroutines.html

//++ coroutine, generator, continuation for C++

struct _generator
{
	int _line;
	_generator():_line(-1) {}
};

#define $generator(NAME) struct NAME : public _generator

#define $emit(T) bool operator()(T& _rv) { \
					if(_line < 0) { _line=0;}\
					switch(_line) { case 0:;

#define $stop  } _line = 0; return false; }

#define $yield(V)     \
		do {\
			_line=__LINE__;\
			_rv = (V); return true; case __LINE__:;\
		} while (0)

//-- coroutine, generator, continuation for C++


$generator(descent)
{
	int i;
	$emit(int) // will emit int values. Start of body of the generator.
		for (i = 10; i > 0; i--)
			$yield(i); // a.k.a. yield in Python - return next number in [1..10], reversed.
	$stop; // stop, end of sequence. End of body of the generator.
};


int _tmain(int argc, _TCHAR* argv[])
{
	descent gen;
	for (int n; gen(n);) // "get next" generator invocation
		printf("next number is %d\n", n);
	return 0;
}
