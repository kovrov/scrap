static import std.stream;


struct BitFile
{
	std.stream.InputStream _stream;
	ubyte _mask = 0b10000000;
	ubyte _rack;

	bool bitioFileInputBit()
	{
		if (_mask == 0b10000000)
			_stream.read(_rack);  // throws at EOF

		bool res = _rack & _mask ? true: false;  // wtf?

		_mask >>= 1;
		if (_mask == 0)
			_mask = 0b10000000;

		return res;
	}

	uint bitioFileInputBits(int bit_count)
	{
		uint return_value = 0;
		uint mask = 0b00000000000000000000000000000001 << (bit_count - 1);
		while (mask != 0)
		{
			if (_mask == 0b10000000)
				_stream.read(_rack);  // throws at EOF

			if (_rack & _mask)
				return_value |= mask;

			_mask >>= 1;
			if (_mask == 0)
				_mask = 0b10000000;
			mask >>= 1;
		}
		return return_value;
	}
}


const INDEX_BIT_COUNT = 12;
const LENGTH_BIT_COUNT = 4;
const BREAK_EVEN = (1 + INDEX_BIT_COUNT + LENGTH_BIT_COUNT) / 9;
const END_OF_STREAM = 0;


void expandLZSS(std.stream.InputStream input, std.stream.OutputStream output)
{
	BitFile bit_file;
	bit_file._stream = input;

	ubyte c;
	uint match_length;
	uint match_position;
	ubyte[1 << INDEX_BIT_COUNT] window;
	int window_pos = 1;
	while (true)
	{
		if (bit_file.bitioFileInputBit())
		{
			c = bit_file.bitioFileInputBits(8);
			output.write(c);
			window[window_pos] = c;
			window_pos = (window_pos + 1) % window.length;
		}
		else
		{
			match_position = bit_file.bitioFileInputBits(INDEX_BIT_COUNT);
			if (match_position == END_OF_STREAM)
				break;
			match_length = bit_file.bitioFileInputBits(LENGTH_BIT_COUNT) + BREAK_EVEN;
			for (uint i = 0; i <= match_length; i++)
			{
				c = window[(match_position + i) % window.length];
				output.write(c);
				window[window_pos] = c;
				window_pos = (window_pos + 1) % window.length;
			}
		}
	}
}


class LZSSFilterStream : std.stream.Stream
{
	private BitFile _bit_file;
	bool _eof = false;

	// readBlock stuff
	ubyte[] _overflow_buffer;
	ubyte[1 << INDEX_BIT_COUNT] _window;
	int _window_pos = 1;

	this (std.stream.InputStream input)
	{
		_bit_file._stream = input;
		readable = true;
		writeable = false;
		seekable = false;
	}

	override size_t readBlock(void* buffer, size_t size)
	{
		if (_eof || size < 1)
			return 0;

		ubyte* outbuf = cast(ubyte*)buffer;
		size_t read = 0;
		if (_overflow_buffer.length)
		{
			if (_overflow_buffer.length > size) // 30 > 1
			{
				outbuf[0 .. size] = _overflow_buffer[0 .. size];
				_overflow_buffer = _overflow_buffer[size .. $];
				read = size;
			}
			else
			{
				read = _overflow_buffer.length;
				outbuf[0 .. read] = _overflow_buffer;
				_overflow_buffer.length = 0;
			}
		}

		ubyte c;
		while (read < size)
		{
			if (_bit_file.bitioFileInputBit())
			{
				c = _bit_file.bitioFileInputBits(8);
				outbuf[read++] = c;
				_window[_window_pos] = c;
				_window_pos = (_window_pos + 1) % _window.length;
			}
			else
			{
				uint match_position = _bit_file.bitioFileInputBits(INDEX_BIT_COUNT);
				if (match_position == END_OF_STREAM)
				{
					_eof = true;
					break;
				}
				uint match_length = _bit_file.bitioFileInputBits(LENGTH_BIT_COUNT) + BREAK_EVEN;
				for (uint i = 0; i <= match_length; i++)
				{
					c = _window[(match_position + i) % _window.length];
					if (read < size)
						outbuf[read++] = c;
					else
						_overflow_buffer ~= c;
					_window[_window_pos] = c;
					_window_pos = (_window_pos + 1) % _window.length;
				}
			}
		}
		return read;
	}

	override size_t writeBlock(void* buffer, size_t size)
	{
		throw new Exception("not implemented");
	}

	override ulong seek(long offset, std.stream.SeekPos whence)
	{
		throw new Exception("not implemented");
	}

	override bool eof()
	{
		return _eof;
	}
}


//version (unittest) // D 2.0
	static import std.stdio;

unittest
{
	auto scope stream = new LZSSFilterStream(new std.stream.File("data.lzss"));
	foreach (char[] line; stream)
	{
		std.stdio.writefln("%s", line);
	}
}
