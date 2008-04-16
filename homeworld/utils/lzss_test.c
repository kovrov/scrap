#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <assert.h>

#define INDEX_BIT_COUNT      12
#define LENGTH_BIT_COUNT     4
#define WINDOW_SIZE          ( 1 << INDEX_BIT_COUNT )
#define BREAK_EVEN           ( ( 1 + INDEX_BIT_COUNT + LENGTH_BIT_COUNT ) / 9 )
#define END_OF_STREAM        0

typedef struct BitFile
{
	FILE *file;
	unsigned char mask; // WTF?
	int rack; // WTF?
	int pacifier_counter;  // WTF???
} BitFile;

int bitIOFileInputBit(BitFile *bit_file)
{
	int value;

	if (bit_file->mask == 0x80)  // 10000000
	{
		bit_file->rack = getc(bit_file->file);
		assert (bit_file->rack != EOF);  // fatal_error("Fatal error in InputBit!\n");
	}
	value = bit_file->rack & bit_file->mask;
	bit_file->mask >>= 1;
	if (bit_file->mask == 0)
		bit_file->mask = 0x80;  // 10000000
	return value ? 1 : 0;
}

int bitIOFileInputBits(BitFile *bit_file, int bit_count)
{
	int mask;
	int return_value;

	mask = 1 << (bit_count - 1);
	return_value = 0;
	while (mask != 0)
	{
		if (bit_file->mask == 0x80)  // 10000000
		{
			bit_file->rack = getc(bit_file->file);
			assert (bit_file->rack != EOF);  //fatal_error("Fatal error in InputBit!\n");
		}
		if (bit_file->rack & bit_file->mask)
			return_value |= mask;
		mask >>= 1;
		bit_file->mask >>= 1;
		if (bit_file->mask == 0)
			bit_file->mask = 0x80;  // 10000000
	}
	return return_value;
}

int lzssExpandFileToBuffer(BitFile *input, unsigned char *output, int outputSize)
{
	int i;
	int current_position;
	unsigned char c;
	int match_length;
	int match_position;
	unsigned char *outBuffer = output;
	unsigned char window[WINDOW_SIZE];
 
	current_position = 1;
	while (1)
	{
		if (bitIOFileInputBit(input))
		{
			c = (unsigned char)bitIOFileInputBits(input, 8);
			*(outBuffer++) = c;
			window[current_position] = c;
			current_position = (current_position + 1) % WINDOW_SIZE;
		}
		else
		{
			match_position = bitIOFileInputBits(input, INDEX_BIT_COUNT);
			if (match_position == END_OF_STREAM)
				break;

			match_length = bitIOFileInputBits(input, LENGTH_BIT_COUNT) + BREAK_EVEN;

			for (i = 0; i <= match_length; i++)
			{
				c = window[(match_position + i) % WINDOW_SIZE];
				*(outBuffer++) = c;
				window[current_position] = c;
				current_position = (current_position + 1) % WINDOW_SIZE;
			}
		}
	}

	return outBuffer - output;
}

int main(int argc, char *argv[])
{
	BitFile bit_file;
	bit_file.file = fopen("data.lzss", "rb");
	bit_file.rack = 0;
	bit_file.mask = 0x80;  // 10000000

	unsigned char output[10 * 1024];
	int outputSize = 10 * 1024;
	int len = lzssExpandFileToBuffer(&bit_file, output, outputSize);
	output[len] = 0;
	printf("%s\n", output);

	return 0;
}
