
import std.stdio;
import std.conv;

struct Option
{
	void delegate(string) action;
}

Option action(void delegate(string) fn)
{
	Option opt;
	opt.action = fn;
	return opt;
}

void main(string[] args)
{
	foreach (arg ; args)
	{
		writefln("%s", arg);
	}
	auto opt = action((string s){writefln("i'm %s action", s);});
	opt.action("test");
}
