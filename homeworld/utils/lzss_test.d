import std.stdio;
import std.stream;
import win32.windows;


struct BitFile
{
    Stream _file;
    ubyte _mask = 0b10000000;
    ubyte _rack;

	bool bitioFileInputBit()
	{
		if (_mask == 0b10000000)
			_file.read(_rack);  // throws at EOF

		bool res = _rack & _mask ? true: false;  // wtf?

		_mask >>= 1;
		if (_mask == 0)
			_mask = 0b10000000;

		return res;
	}

	ubyte bitioFileInputBits(int bit_count) // 3|7|11
	{
		uint return_value = 0;
		uint mask = 0b00000000000000000000000000000001 << (bit_count - 1);
		while (mask != 0)
		{
			if (_mask == 0b10000000)
				_file.read(_rack);  // throws at EOF

			if (_rack & _mask)
				return_value |= mask;

			mask >>= 1;
			_mask >>= 1;
			if (_mask == 0)
				_mask = 0b10000000;
		}
		return return_value;
	}
}


const INDEX_BIT_COUNT = 12;
const LENGTH_BIT_COUNT = 4;
const BREAK_EVEN = (1 + INDEX_BIT_COUNT + LENGTH_BIT_COUNT) / 9;
const END_OF_STREAM = 0;


void expandLZSS(ref BitFile input, Stream output)
{
    int window_pos;
    ubyte c;
    int match_length;
    ubyte match_position;
	ubyte[1 << INDEX_BIT_COUNT] window;

    window_pos = 1;
    while (true)
	{
        if (input.bitioFileInputBit())
		{
            c = input.bitioFileInputBits(8);
            writef("%s", cast(char)c);//output.write(c);
            window[window_pos] = c;
            window_pos = (window_pos + 1) % window.length;
        }
		else
		{
            match_position = input.bitioFileInputBits(INDEX_BIT_COUNT); // throws at EOF
            match_length = input.bitioFileInputBits(LENGTH_BIT_COUNT);
            match_length += BREAK_EVEN;
            for (int i = 0 ; i <= match_length ; i++)
			{
                c = window[(match_position + i) % window.length];
                writef("%s", cast(char)c);//output.write(c);
                window[window_pos] = c;
                window_pos = (window_pos + 1) % window.length;
            }
        }
    }
}


void main()
{
	BitFile bitfile;
	bitfile._file = new File("data.lzss");
	expandLZSS(bitfile, null);
}
