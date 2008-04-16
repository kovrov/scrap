import std.stdio;
import std.stream;
import win32.windows;


struct BitFile
{
    Stream _file;
    ubyte _mask;
    ubyte _rack;

	bool bitioFileInputBit()
	{
		if (_mask == 0b10000000)
			_file.read(_rack);  // throws at EOF

		_mask >>= 1;
		if (_mask == 0)
			_mask = 0b10000000;

		return _rack & _mask ? true : false;
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
            output.write(c);
            window[window_pos] = c;
            window_pos = (window_pos + 1) & (window.length - 1);  // smart way to wrap index?
        }
		else
		{
            match_position = input.bitioFileInputBits(INDEX_BIT_COUNT); // throws at EOF
            match_length = input.bitioFileInputBits(LENGTH_BIT_COUNT);
            match_length += BREAK_EVEN;
            for (int i = 0 ; i <= match_length ; i++)
			{
                c = window[(match_position + i) & (window.length - 1)];  // smart way to wrap index?
                output.write(c);
                window[window_pos] = c;
                window_pos = (window_pos + 1) & (window.length - 1);  // smart way to wrap index?
            }
        }
    }
}


void main()
{
	int i = ' ';
	ubyte b = ' ';
	//writefln("%b:%b", 0b00000000000000000000000000000001 << (8 - 1),  cast(ubyte)(0b00000000000000000000000000000001 << (8 - 1)));
	//writefln("%b:%b", 0b00000001 << (8 - 1),  cast(ubyte)(0b00000001 << (8 - 1)));
	writefln("%b:%b", 0b00000000000000000000000000000001 << (12 - 1), cast(ubyte)(0b00000000000000000000000000000001 << (12 - 1)));
	writefln("%b:%b", 0b00000001 << (12 - 1), cast(ubyte)(0b00000001 << (12 - 1)));
	//writefln("%b:%b", 0b00000000000000000000000000000001 << (4 - 1),  cast(ubyte)(0b00000000000000000000000000000001 << (4 - 1)));
	//writefln("%b:%b", 0b00000001 << (4 - 1),  cast(ubyte)(0b00000001 << (4 - 1)));
}
