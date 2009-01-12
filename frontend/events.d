enum MOUSE_DIRECTION { ENTER, LEAVE }
enum MOUSE_ACTION { PRESS, RELEASE, DOUBLECLICK }
struct Point {}

/* all possible events should be described here */
struct EventHandlers
{
	// keyboard input
	void function(uint key)
			keyPress;
	void function(uint key)
			keyRelease;
	void function(MOUSE_ACTION action, uint button)
			focusOnClick;
	// mouse input
	void function(const ref Point pos, MOUSE_ACTION action, uint button)
			mouseButton;
	void function(int x, int y)
			mouseScroll;
	void function(MOUSE_DIRECTION dir)
			mouseOver;
}

class Base
{
	EventHandlers* handlers;
}

class Foo : Base
{
	static EventHandlers eventMap;
	static this()
	{
		eventMap.mouseButton = &_onMouseButton;
		eventMap.mouseOver   = &_onMouseOver;
	}
	this() { handlers = &eventMap; }

	void _onMouseButton(const ref Point pos, MOUSE_ACTION action, uint button) {}
	void _onMouseOver(MOUSE_DIRECTION dir) {}
}

class Bar : Base
{
	static EventHandlers eventMap;
	static this()
	{
		eventMap.keyPress   = &_onKeyPress;
		eventMap.keyRelease = &_onKeyRelease;
	}
	this() { handlers = &eventMap; }

	void _onMouseButton(const ref Point pos, MOUSE_ACTION action, uint button) {}
	void _onMouseOver(MOUSE_DIRECTION dir) {}

	void _onKeyPress(uint key) {}
	void _onKeyRelease(uint key) {}
}


import std.stdio;
void main()
{
	Base foo = new Foo;
	if (foo.handlers.mouseOver !is null)
	{
		void delegate(MOUSE_DIRECTION dir) handler;
		handler.funcptr = foo.handlers.mouseOver;
		handler.ptr = cast(void*)foo;
		handler(MOUSE_DIRECTION.ENTER);
	}
	Base bar = new Bar;
}
