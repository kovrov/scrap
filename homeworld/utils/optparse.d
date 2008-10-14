
import std.stdio;

void main (string[] args)
{
	writefln("args:");
	foreach (arg; args[1..$])
		writefln(" %s", arg);
}
