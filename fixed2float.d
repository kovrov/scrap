/*
 * utility for wakebreaker data conversion
 */
import std.stdio;
import std.stream;
import std.regexp;
import std.string;
import std.conv;

void main()
{
	convert_data("../data.py");
}

float x2f(int x)
{
	return cast(float)(x) / 65536;
}

void convert_data(string filename)
{
	Stream file = new BufferedFile(filename);
	scope (exit) file.close();
	foreach (char[] line; file)
	{
		uint[2][] found;
		foreach (m; RegExp("\\b([\\d]+\\.?[\\d]*)\\b").search(line))
		{
			auto match = m.match(0);
			if (std.string.find(match, '.') == -1)
			{
				found ~= [m.pre.length, m.match(0).length];
			}
		}

		if (found)
		{
			char[] tmp;
			uint start = 0;
			foreach (slice; found)
			{
				tmp ~= line[start .. slice[0]];
				tmp ~= toString(x2f(toInt(line[slice[0] .. slice[0] + slice[1]])));
				start = slice[0] + slice[1];
			}
			tmp ~= line[start .. $];
			writefln("%s  # %s", tmp, strip(line));
		}
		else
		{
			writefln(line);
		}
	}
}
