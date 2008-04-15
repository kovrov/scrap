/*	Ripped from LZSS implementation by Michael Dipperstein
 *	http://michael.dipperstein.com/lzss/
 */

static import std.stream;  // memset


enum BF	{
		READ = 0,
		WRITE = 1,
		APPEND = 2,
		NO_MODE }

enum ENDIAN {
		UNKNOWN,
		LITTLE,
		BIG}


struct EncodedString
{
	uint offset;    /* offset to start of longest match */
	uint length;    /* length of longest match */
}


struct BitFile
{
    std.stream.Stream _stream;   /* file pointer used by stdio functions */
    ENDIAN _endian;              /* endianess of architecture */
    ubyte _bitBuffer;            /* bits waiting to be read/written */
    ubyte _bitCount;             /* number of bits in bitBuffer */
    BF _mode;                    /* open for read, write, or append */

	/*   This function returns the next byte from the file passed as a parameter.
	 *   Reads next byte from file and updates buffer accordingly.
	 *   Returns EOF if a whole byte cannot be obtained.  Otherwise, the character read.
	 */
	ubyte readByte() // BitFileGetChar
	{
		ubyte buff; // 4 bytes!!
		_stream.read(buff); // throw if at EOF

		if (_bitCount == 0)  // we can just get byte from file
			return buff;

		/* we have some buffered bits to return too */
		/* figure out what to return */
		ubyte tmp = (cast(ubyte)returnValue) >> _bitCount;
		tmp |= (_bitBuffer << (8 - _bitCount));

		/* put remaining in buffer. count shouldn't change. */
		_bitBuffer = returnValue;

		return tmp;
	}

	/*	This function returns the next bit from the file passed as a parameter.
	 *	The bit value returned is the msb in the bit buffer.
	 *	Reads next bit from bit buffer.  If the buffer is empty, a new byte will be
	 *	read from the file.
	 *	Returns 0 if bit == 0, 1 if bit == 1, and EOF if operation fails.
	 */
	int getBit()
	{
		int returnValue;

		if (_bitCount == 0)  // buffer is empty, read another character
		{
			returnValue = _stream.getc();
			if (returnValue == EOF)
				return EOF;
			_bitCount = 8;
			_bitBuffer = returnValue;
		}

		// bit to return is msb in buffer
		_bitCount--;
		returnValue = _bitBuffer >> _bitCount;

		return (returnValue & 0x01);
	}
}


enum {	ENCODED = 0,     // encoded string
		UNCODED = 1,     // unencoded character
		MAX_UNCODED = 2} // maximum match length not encoded and maximum length encoded (4 bits)

const OFFSET_BITS = 12;
const LENGTH_BITS = 4;


/* wraps array index within array bounds (assumes value < 2 * limit) */
template wrap(T)
{
	T wrap(T value, T limit) { return value < limit ? value : value - limit;}
}


/*	This function provides a machine independent layer that allows a single
 *	function call to stuff an arbitrary number of bits into an integer type
 *	variable.
 *	Calls a function that reads bits from the bit buffer and file stream.  The
 *	bit buffer will be modified as necessary. the bits will be written to "bits"
 *	from least significant byte to most significant byte.
 *	Returns EOF for failure, otherwise the number of bits read by the called
 *	function.
 */
int BitFileGetBitsInt(ref BitFile stream, void* bits, uint count, size_t size)
{
	switch (stream._endian)
	{
//	case ENDIAN.LITTLE: return BitFileGetBitsLE(stream, bits, count);
//	case ENDIAN.BIG:    return BitFileGetBitsBE(stream, bits, count, size);
	default:            return EOF;
	}
}


/*	Reads an LZSS encoded input and write decoded data to output buffer.
 *	This algorithm encodes strings as 16 bits (a 12 bit offset + a 4 bit length).
 */
int decodeLZSS(std.stream.Stream input, std.stream.Stream output)
{
	// convert output file to bitfile
	BitFile bit_file;
	bit_file._stream = input;
	bit_file._mode = BF.READ;
    //bit_file.endian = DetermineEndianess();
	// offset/length code for string
	EncodedString code;  
	/* Fill the sliding window buffer with some known vales.  Encoder must
	 * use the same values.  If common characters are used, there's an
	 * increased chance of matching to the earlier strings.
	 */
	ubyte[] uncodedLookahead;
	ubyte[1 << OFFSET_BITS] slidingWindow = 1; // memset // FIXME: 1?
	uint nextChar = 0;
	while (true)
	{
		int c = bit_file.getBit();
		if (c == EOF)
			break;

		if (c == UNCODED)  // unencoded character
		{
			c = bit_file.readByte();
			if (c == EOF)
				break;

			// write out byte and put it in sliding window
			output.write(c);
			slidingWindow[nextChar] = c;
			nextChar = wrap(nextChar + 1, slidingWindow.length);
		}
		else  // c is encoded string
		{
			code.offset = 0;
			code.length = 0;

			if (BitFileGetBitsInt(bit_file, &code.offset, OFFSET_BITS, uint.sizeof) == EOF)
				break;

			if (BitFileGetBitsInt(bit_file, &code.length, LENGTH_BITS, uint.sizeof) == EOF)
				break;

			code.length += MAX_UNCODED + 1;

			/****************************************************************
			* Write out decoded string to file and lookahead.  It would be
			* nice to write to the sliding window instead of the lookahead,
			* but we could end up overwriting the matching string with the
			* new string if abs(offset - next char) < match length.
			****************************************************************/
			for (ubyte i = 0; i < code.length; i++)
			{
				c = slidingWindow[wrap(code.offset + i, slidingWindow.length)];
				output.write(c);
				uncodedLookahead[i] = c;
			}

			/* write out decoded string to sliding window */
			for (uint i = 0; i < code.length; i++)
				slidingWindow[(nextChar + i) % slidingWindow.length] = uncodedLookahead[i];

			nextChar = wrap(nextChar + code.length, slidingWindow.length);
		}
	}

	/* we've decoded everything, free bitfile structure */
//	BitFileToFILE(bit_file);

	return true;
}
