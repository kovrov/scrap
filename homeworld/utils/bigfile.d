/* Utilities for manipulating .big files of Relic Entertainment's Homeworld */

static import std.stream;
static import std.string;
// relative import works?
static import crc;
static import lzss;

const FILE_HEADER = "RBF";
const FILE_VERSION = "1.23";

const BF_FLAG_TOC_SORTED = 1;


/* TOC enties are dumped/loaded directly to/from .big file */
struct TOCEntry
{
    uint nameCRC1;  // first half of filename CRC
	uint nameCRC2;  // second half of filename CRC
    ushort nameLength; // CRCs and length are hash for filename
    uint storedLength;
    uint realLength;
    uint offset;
    int timeStamp;
    ubyte compressionType;  // bool?
}


class BigFileEntry
{
	TOCEntry _toc;
	string _name;
	std.stream.Stream _stream;  // InputStream

	string name()
	{
		if (_name)
			return _name;

		_stream.seekSet(_toc.offset);
		_name.length = _toc.nameLength;
		_stream.readExact(cast(void*)_name.ptr, _name.length);

		/*	When decrypting filenames, don't touch the terminating null
			when decrypting. Pass in name_size, not name_size + 1. */
		ubyte last_byte = 0xD5;
		foreach (ref i; _name)
		{
			last_byte ^= i;
			i = last_byte;
		}

		return _name;
	}

	int opEquals(ref TOCEntry e)
	{
		return (_toc.nameCRC1 == e.nameCRC1) && (_toc.nameCRC2 == e.nameCRC2);
	}

	int opCmp(ref TOCEntry e)
	{
        if (_toc.nameCRC1 != e.nameCRC1)
			return _toc.nameCRC1 - e.nameCRC1;
        return _toc.nameCRC2 - e.nameCRC2;
	}
}


class BigFile
{
	std.stream.Stream _stream;  // InputStream
	uint _flags;
	BigFileEntry[] _files;

	this(string path)
	{
		_stream = new std.stream.File(path);

		// file signature
		ubyte[FILE_HEADER.length + FILE_VERSION.length] buffer;
		size_t read = _stream.read(buffer);
		if (read != buffer.length || buffer != cast(ubyte[])(FILE_HEADER ~ FILE_VERSION))
			throw new Exception("File signature incorrect.");

		// table of contents

		uint _number_of_files;
		static assert (_number_of_files.sizeof == 4);  // section is 4 bytes exactly
		_stream.readExact(cast(void*)&_number_of_files, 4);
		// TODO: fix endianness

		static assert (_flags.sizeof == 4);  // section is 4 bytes exactly
		_stream.readExact(cast(void*)&_flags, 4);
		// TODO: fix endianness

		static assert (TOCEntry.sizeof == 32);  // each toc entry is 32 bytes exactly
		_files.length = _number_of_files;
		foreach (ref entry; _files)
		{
			entry = new BigFileEntry;
			entry._stream = _stream;
			_stream.readExact(cast(void*)&entry._toc, 32);
			// TODO: fix endianness
		}
		//_stream.seek(, std.stream.SeekPos.Current);
	}

	~this()
	{
		_stream.close();
	}

	std.stream.InputStream open(ref TOCEntry e)
	{
		auto s = new std.stream.SliceStream(_stream,
		                                    e.offset + e.nameLength + 1,
		                                    e.offset + e.nameLength + 1 + e.storedLength);
		if (e.compressionType)
			return new lzss.LZSSFilterStream(s);

		return s;
	}

	std.stream.InputStream open(string name)
	{
		string targetname = std.string.tolower(name);
		TOCEntry target;
		target.nameLength = targetname.length;
		target.nameCRC1 = crc.crc32(targetname[0 .. $/2]);
		target.nameCRC2 = crc.crc32(targetname[$/2 .. $/2*2]); //[$/2 .. $]
		BigFileEntry toc_entry;

		if (_flags & BF_FLAG_TOC_SORTED)  // binary search
		{
			int low = 0;
			int high = _files.length - 1;
			while (low <= high)
			{
				uint fileNum = (low + high) / 2;  // middle
				if (_files[fileNum] == target)
				{
					toc_entry = _files[fileNum];
					break;
				}
				else if (_files[fileNum] < target)
					low = fileNum + 1;
				else
					high = fileNum - 1;
			}
		}
		else  // unsorted toc - linear search
		{
			// optimized to start searching from wherever we left off last
			// time to potentially find sequentially ordered files faster
			static int file_num = 0;

			int startFileNum = file_num;
			do
			{
				if (_files[file_num] == target)
				{
					toc_entry = _files[file_num];
					break;
				}
				++file_num;
				if (file_num >= _files.length)
					file_num = 0;
			}
			while (file_num != startFileNum);
		}

		if (toc_entry is null)
			throw new Exception("File not found");

		return open(toc_entry._toc);
	}

	int opApply(int delegate(ref BigFileEntry) dg)
	{
		int result = 0;
		foreach (ref entry; _files)
		{
			_stream.seekSet(entry._toc.offset);
				result = dg(entry);
			if (result)
				break;
		}
		return result;
	}
}


// tests
import std.stdio;
import std.c.stdlib;

void main()
{
	string data_path = std.string.toString(getenv("HW_Data"));
	string path = (data_path ? data_path : ".") ~ "/update.big";
	auto scope bf = new BigFile(path);

	ubyte[] data;
	foreach (bf_entry; bf)
	{
		std.stdio.writefln("%s", bf_entry.name);
		auto file = bf.open(bf_entry._toc);
		data.length = bf_entry._toc.realLength;
		file.read(data);
		//foreach (char[] line; file)
			//std.stdio.writefln("%s", line);
	}
}
