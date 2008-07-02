import std.stream;
import std.string;
import std.stdio;

void main()
{
	Stream file = new BufferedFile("c:/data/desktop/data.txt");
	scope (exit) file.close();

	string[][string] res;
	foreach (string line; file)
	{
		string[] digit_and_letters = split(line, ":");
		foreach (string letter; split(digit_and_letters[1]))
		{
			res[letter.dup] ~= digit_and_letters[0].dup;
		}
	}

	foreach (string letter; res.keys.sort)
	{
		writefln("%s: %s", letter, join(res[letter], " "));
	}
}
