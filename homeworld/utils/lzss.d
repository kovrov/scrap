/*	Ripped from LZSS implementation by Michael Dipperstein
	http://michael.dipperstein.com/lzss/
*/

import std.c.string;  // memset

struct BitFile
{
    FILE* stream;       /* file pointer used by stdio functions */
    endian_t endian;    /* endianess of architecture */
    ubyte bitBuffer;    /* bits waiting to be read/written */
    ubyte bitCount;     /* number of bits in bitBuffer */
    BF_MODES mode;      /* open for read, write, or append */
}


/*	Reads an LZSS encoded input and write decoded data to output buffer.
	This algorithm encodes strings as 16 bits (a 12 bit offset + a 4 bit length).
*/
int decodeLZSS(ubyte[] input, ubyte[] output)
{
	BitFile bfp_in;

	unsigned int i, nextChar;
	encoded_string_t code;              /* offset/length code for string */

	/* convert output file to bitfile */
	bfp_in = MakeBitFile(input, BF_READ);

	/************************************************************************
	* Fill the sliding window buffer with some known vales.  Encoder must
	* use the same values.  If common characters are used, there's an
	* increased chance of matching to the earlier strings.
	************************************************************************/
	memset(slidingWindow, 1, WINDOW_SIZE * sizeof(ubyte));

	nextChar = 0;

	while (true)
	{
		int c = BitFileGetBit(bfp_in);
		if (c == EOF)
		{
			/* we hit the EOF */
			break;
		}

		if (c == UNCODED)
		{
			/* uncoded character */
			if ((c = BitFileGetChar(bfp_in)) == EOF)
			{
				break;
			}

			/* write out byte and put it in sliding window */
			putc(c, output);
			slidingWindow[nextChar] = c;
			nextChar = Wrap((nextChar + 1), WINDOW_SIZE);
		}
		else
		{
			/* offset and length */
			code.offset = 0;
			code.length = 0;

			if ((BitFileGetBitsInt(bfp_in, &code.offset, OFFSET_BITS, sizeof(unsigned int))) == EOF)
			{
				break;
			}

			if ((BitFileGetBitsInt(bfp_in, &code.length, LENGTH_BITS, sizeof(unsigned int))) == EOF)
			{
				break;
			}

			code.length += MAX_UNCODED + 1;

			/****************************************************************
			* Write out decoded string to file and lookahead.  It would be
			* nice to write to the sliding window instead of the lookahead,
			* but we could end up overwriting the matching string with the
			* new string if abs(offset - next char) < match length.
			****************************************************************/
			for (i = 0; i < code.length; i++)
			{
				c = slidingWindow[Wrap((code.offset + i), WINDOW_SIZE)];
				putc(c, output);
				uncodedLookahead[i] = c;
			}

			/* write out decoded string to sliding window */
			for (i = 0; i < code.length; i++)
			{
				slidingWindow[(nextChar + i) % WINDOW_SIZE] = uncodedLookahead[i];
			}

			nextChar = Wrap((nextChar + code.length), WINDOW_SIZE);
		}
	}

	/* we've decoded everything, free bitfile structure */
	BitFileToFILE(bfp_in);

	return (EXIT_SUCCESS);
}





import std.stdio;

//unittest
void main()
{
}
