/* Utilities for manipulating .big files of Relic Entertainment's Homeworld */

static import std.stream;
static import std.string;
import crc;  // relative import works?
import lzss;  // relative import works?

const FILE_HEADER = "RBF";
const FILE_VERSION = "1.23";

const BF_FLAG_TOC_SORTED = 1;


bool bigCRC64EQ(TOCEntry a, TOCEntry b){return (a.nameCRC1 == b.nameCRC1) && (a.nameCRC2 == b.nameCRC2);}
bool bigCRC64GT(TOCEntry a, TOCEntry b){return (a.nameCRC1 > b.nameCRC1) || (a.nameCRC1 == b.nameCRC1 && a.nameCRC2 > b.nameCRC2);}
bool bigCRC64LT(TOCEntry a, TOCEntry b){return (a.nameCRC1 < b.nameCRC1) || (a.nameCRC1 == b.nameCRC1 && a.nameCRC2 < b.nameCRC2);}


/* TOC enties are serialized in .big file */
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
} ;

/*	When decrypting filenames, don't touch the terminating null when decrypting.
	Pass in name_size, not name_size + 1. */
void decrypt_name(ubyte[] buffer) 
{ 
    ubyte last_byte = 0xD5;
    foreach (ref i; buffer) 
    { 
        last_byte ^= i; 
        i = last_byte; 
    } 
} 

class BigFile
{
	std.stream.Stream _stream;  // InputStream
	uint _number_of_files;
	uint _flags;
	TOCEntry[] _toc;

	this(string path)
	{
		_stream = new std.stream.File(path);

		// file signature
		ubyte[FILE_HEADER.length + FILE_VERSION.length] buffer;
		size_t read = _stream.read(buffer);
		if (read != buffer.length || buffer != cast(ubyte[])(FILE_HEADER ~ FILE_VERSION))
			throw new Exception("File signature incorrect.");

		// table of contents

		static assert (_number_of_files.sizeof == 4);  // section is 4 bytes exactly
		_stream.readExact(cast(void*)&_number_of_files, 4);
		// TODO: fix endianness

		static assert (_flags.sizeof == 4);  // section is 4 bytes exactly
		_stream.readExact(cast(void*)&_flags, 4);
		// TODO: fix endianness

		static assert (TOCEntry.sizeof == 32);  // each toc entry is 32 bytes exactly
		_toc.length = _number_of_files;
		foreach (ref entry; _toc)
		{
			_stream.readExact(cast(void*)&entry, 32);
			// TODO: fix endianness
		}

		// test
		//auto pos = _stream.position();
		foreach (ref entry; _toc)
		{
			_stream.seekSet(entry.offset);
			ubyte[] bbuffer;
			bbuffer.length = entry.nameLength;
			assert (_stream.read(bbuffer) == bbuffer.length);
			decrypt_name(bbuffer);
			writefln("entry: %s {%X:%X:%d}", cast(char[])bbuffer, entry.nameCRC1, entry.nameCRC2, entry.nameLength);
		}
		//_stream.seekSet(pos);

		//_stream.seek(, std.stream.SeekPos.Current); 
	}

	~this()
	{
		_stream.close();
	}

	std.stream.InputStream open(string name)
	{
		string targetname = std.string.tolower(name);
		TOCEntry target;
		target.nameLength = targetname.length;
		target.nameCRC1 = crc32(targetname[0 .. $/2]);
		target.nameCRC2 = crc32(targetname[$/2 .. $/2*2]); //[$/2 .. $]
		TOCEntry* e;

		if (0 && _flags & BF_FLAG_TOC_SORTED)  // binary search
		{
			int low = 0;
			int high = _number_of_files - 1;
			while (low <= high)
			{
				uint fileNum = (low + high) / 2;  // middle
				if (bigCRC64EQ(target, _toc[fileNum]))
				{
					e = &_toc[fileNum];
					break;
				}
				else if (bigCRC64GT(target, _toc[fileNum]))
					low = fileNum + 1;
				else // if (b < a[fileNum])
					high = fileNum -1;
			}
		}
		else
		{
			// unsorted toc -- linear search, but optimized to
			// start searching from wherever we left off last time
			// to potentially find sequentially ordered files faster
			static int file_num = 0;
			int startFileNum = file_num;
			do
			{
				if (_toc[file_num].nameLength == target.nameLength &&
					_toc[file_num].nameCRC1 == target.nameCRC1 &&
					_toc[file_num].nameCRC2 == target.nameCRC2)
				{
					e = &_toc[file_num];
					break;
				}
				++file_num;
				if (file_num >= _number_of_files)
					file_num = 0;
			}
			while (file_num != startFileNum);
		}

		if (e is null)
			throw new Exception("File not found");

		auto s = new std.stream.SliceStream(_stream,
		                                    e.offset + e.nameLength + 1,
		                                    e.offset + e.nameLength + 1 + e.storedLength);
		if (e.compressionType)
			return new LZSSFilterStream(s);

		return s;
	}
}


// tests
import std.stdio;
import win32.windows;
//pragma (lib, "win32.lib");

void main()
{
	char[1024] buffer;
	size_t read = GetEnvironmentVariable("HW_Data", buffer.ptr, buffer.length);
	string path = (read > 0 ? buffer[0 .. read] : ".") ~ "/update.big";
	auto scope bf = new BigFile(path);

	auto file = bf.open("AiPlayer.script");
	foreach (char[] line; file)
	{
		std.stdio.writefln("%s", line);
	}
}
