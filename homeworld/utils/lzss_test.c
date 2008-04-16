#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <assert.h>

#define INDEX_BIT_COUNT      12
#define LENGTH_BIT_COUNT     4
#define WINDOW_SIZE          ( 1 << INDEX_BIT_COUNT )
#define BREAK_EVEN           ( ( 1 + INDEX_BIT_COUNT + LENGTH_BIT_COUNT ) / 9 )
#define MOD_WINDOW( a )      ( ( a ) & ( WINDOW_SIZE - 1 ) )
#define END_OF_STREAM        0

typedef struct BitFile
{
    FILE *file;
    unsigned char mask; // WTF?
    int rack; // WTF?
    int pacifier_counter;  // WTF???
	//int index;  // like a file position, in bytes
} BitFile;

int bitIOFileInputBit( bit_file )
BitFile *bit_file;
{
    int value;

    if ( bit_file->mask == 0x80 ) {
        bit_file->rack = getc( bit_file->file );
		//++bit_file->index;
        assert( bit_file->rack != EOF );  // fatal_error( "Fatal error in InputBit!\n" );
    }
    value = bit_file->rack & bit_file->mask;
    bit_file->mask >>= 1;
    if ( bit_file->mask == 0 )
	bit_file->mask = 0x80;
    return( value ? 1 : 0 );
}


unsigned long bitIOFileInputBits( bit_file, bit_count )
BitFile *bit_file;
int bit_count;
{
    unsigned long mask;
    unsigned long return_value;

    mask = 1L << ( bit_count - 1 );
    return_value = 0;
    while ( mask != 0) {
	if ( bit_file->mask == 0x80 ) {
	    bit_file->rack = getc( bit_file->file );
		//++bit_file->index;
		assert( bit_file->rack != EOF );  //fatal_error( "Fatal error in InputBit!\n" );
	}
	if ( bit_file->rack & bit_file->mask )
            return_value |= mask;
        mask >>= 1;
        bit_file->mask >>= 1;
        if ( bit_file->mask == 0 )
            bit_file->mask = 0x80;
    }
    return( return_value );
}


int lzssExpandFileToBuffer(BitFile *input, char *output, int outputSize)
{
	int i;
	int current_position;
	int c;
	int match_length;
	int match_position;
	char *outBuffer = output;
	unsigned char window[ WINDOW_SIZE ];
 
	current_position = 1;
	for ( ; ; ) {
		if (bitIOFileInputBit(input))
		{
			c = (int)bitIOFileInputBits(input, 8);
			*(outBuffer++) = c;
			window[current_position] = (unsigned char)c;
			current_position = MOD_WINDOW(current_position + 1);
		} else {
			match_position = (int)bitIOFileInputBits(input, INDEX_BIT_COUNT);
			if (match_position == END_OF_STREAM)
				break;
			match_length = (int)bitIOFileInputBits(input, LENGTH_BIT_COUNT);
			match_length += BREAK_EVEN;
			for ( i = 0 ; i <= match_length ; i++ )
			{
				c = window[MOD_WINDOW(match_position + i)];
				*(outBuffer++) = c;
				window[current_position] = (unsigned char)c;
				current_position = MOD_WINDOW(current_position + 1);
			}
		}
	}

	return (outBuffer - output);
}

int main(int argc, char *argv[])
{
	BitFile bit_file;
    bit_file.file = fopen("data.lzss", "r");
    bit_file.rack = 0;
    bit_file.mask = 0x80;

	char output[1024 * 10];
	int outputSize = 1024 * 10;
	int len = lzssExpandFileToBuffer(&bit_file, output, outputSize);
	output[len] = 0;
	printf("%s\n", output);
	return 0;
}
