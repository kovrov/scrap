import std.stream;
import std.string;
import std.stdio;

void main()
{
	Stream file = new BufferedFile("c:/data/desktop/data.txt");
	scope (exit) file.close();

	const max_chars = 'z' - 'A';
	char[1024][max_chars] res;

	foreach (string line; file)
	{
		string[] digit_and_letters = split(line, ":");
		foreach (string letter; split(digit_and_letters[1]))
		{
			res[cast(uint)letter[0]-'A'][0] = digit_and_letters[0][0];
		}
	}

	foreach (letter, chars; res)
	{
		if (chars[0])
			writefln("%s: %s", cast(char)(letter+'A'), chars[0]);
	}
}
