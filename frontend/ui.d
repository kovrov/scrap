static import sys;
static import tree;
static import generic;
alias generic.Point!(short) Point;


enum MOUSE_DIRECTION { ENTER, LEAVE }
enum MOUSE_ACTION { PRESS, RELEASE, DOUBLECLICK }
enum FB
{
	NONE         = 0,
	StateChanged = 1,
	CaptureMouse = 1<<1,
	ReleaseMouse = 1<<2,
}

struct MouseButtonEvent
{
	Point pos;
	MOUSE_ACTION action;
	uint button;
	//T target;
}

interface UpwardEventListener
{
	void handleUpwardEvent(ref MouseButtonEvent);
	//FB deactivate();
}

interface Focusable  // focus policy interface
{
	//FB focusOnKey();
	abstract bool focusOnMouse(MOUSE_ACTION action, uint button);
	abstract FB onKey(uint keycode);
}


/* this is important concept - injecting an interface into root of the class hierarchy */
class TargetNode(alias PAINT_INTERFACE)
{
	mixin PAINT_INTERFACE;

	mixin tree.Node;
	mixin tree.setParent;
	mixin tree.opApply!("!node.hidden");  // for mouse cursor hit test (with condition mixin)
	mixin tree.opApplyReverse!("!node.hidden");  // for drawing (with condition mixin)

	static typeof(this) activeNode;
	static Focusable focusedNode;

	bool hidden;
	bool disabled;

	string name;

	bool nested = true;
	union
	{
		generic.Rect!(short, ushort) rect;
		struct
		{
			short x, y;
			ushort width, height;
		}
		static assert (rect.sizeof == short.sizeof*2 + ushort.sizeof*2);
	}

	this(string name, typeof(this) parent=null)
	{
		if (parent)
			this.setParent(parent);
		this.name = name;
	}

	Point position_abs()
	{
		auto abs_pos = this.rect.position;
		auto parent = this.nested ? this.parent : null;
		while (parent)
		{
			abs_pos += parent.rect.position;
			parent = parent.nested ? parent.parent : null;
		}
		return abs_pos;
	}

	abstract FB onMouseOver(MOUSE_DIRECTION dir);
	abstract FB onMouseButton(const ref Point pos, MOUSE_ACTION action, uint button/*, modifiers*/);
	abstract FB onMouseScroll(int x, int y);
}

enum MOUSE
{
	MOVE  = 1,
	LEAVE,
	UP,
	DOWN,
}

class EventManager(T /* : TargetNode */)
{
	T root;
	T mouseOldTarget;
	T mouseHolder;
	sys.Window window;

	this(sys.Window window)
	{
		this.window = window;
	}

import std.stdio;
	void dispatch_mouse_input(const ref Point pos, sys.MOUSE type, int button = -1)
	{
		UpwardEventListener[32] event_path_stack;
		UpwardEventListener[] get_event_path(T target_node)
		{
			int i = 0;
			for (auto node=target_node.parent; node !is null; node=node.parent)
			{
				auto listener = cast(UpwardEventListener)node;
				if (listener !is null)
					event_path_stack[i++] = listener;
			}
			return event_path_stack[0..i];
		}
		auto nodeUnderCursor = findControl(this.root, pos);
		auto target = (this.mouseHolder !is null) ? this.mouseHolder : nodeUnderCursor;

		switch (type)
		{
		case sys.MOUSE.PRESS:
			assert (button > -1);
			if (target is null || target.disabled)
				return;
			//TODO: Downward Propagation a.k.a. Sinking/Tunneling/Preview/Capturing of event
			this.process(target.onMouseButton(pos, MOUSE_ACTION.PRESS, button/*, modifiers*/), target, pos);
			//TODO: Upward Propagation a.k.a. Bubbling of event
			auto event = MouseButtonEvent(pos, MOUSE_ACTION.PRESS, button);
			foreach (ref listener; get_event_path(target))
			{
				listener.handleUpwardEvent(event);
			}
			// set focus...
			auto focusable = cast(Focusable)target;
			if (focusable !is null && T.focusedNode !is focusable && focusable.focusOnMouse(MOUSE_ACTION.PRESS, button))
			{
				T.focusedNode = focusable;
				this.window.redraw();  // FB.StateChanged
			}
			break;
		case sys.MOUSE.RELEASE:
			assert (button > -1);
			if (target is null || target.disabled)
				return;
			this.process(target.onMouseButton(pos, MOUSE_ACTION.RELEASE, button/*, modifiers*/), target, pos);
			// arguable focus stuff...
			auto focusable = cast(Focusable)target;
			if (focusable !is null && T.focusedNode !is focusable && focusable.focusOnMouse(MOUSE_ACTION.RELEASE, button))
			{
				T.focusedNode = focusable;
				this.window.redraw();  // FB.StateChanged
			}
			break;
		case sys.MOUSE.MOVE:
			auto newTarget = (this.mouseHolder is null || this.mouseHolder is nodeUnderCursor) ? nodeUnderCursor : null;
			if (this.mouseOldTarget !is newTarget)
				passMouse(newTarget, pos);
			if (target is null || target.disabled)
				return;
			//TODO: subscription (tracking) of mouse movement
			//this.process(target.onMouseMove(pos), target, pos);
			break;
		}
	}

	protected
	void passMouse(ref T target, const ref Point pos)
	{
		assert (this.mouseOldTarget !is target);

		if (this.mouseOldTarget !is null)
			this.process(this.mouseOldTarget.onMouseOver(MOUSE_DIRECTION.LEAVE), this.mouseOldTarget, pos);
			//TODO: check if this.mouseOldTarget just captured mouse

		if (target !is null && !target.disabled)
			this.process(target.onMouseOver(MOUSE_DIRECTION.ENTER), target, pos);

		this.mouseOldTarget = target;
	}

	protected
	void process(FB feedback, T target, const ref Point pos)
	{
		assert (target !is null);
		if (feedback & FB.CaptureMouse)
		{
			assert (this.mouseHolder is null);
			this.mouseHolder = target;
		}
		if (feedback & FB.ReleaseMouse)
		{
			assert (this.mouseHolder is target);
			this.mouseHolder = null;
			//TODO: get rid of recursion
			target = findControl(this.root, pos);
			if (this.mouseOldTarget !is target)
				passMouse(target, pos);
		}
		if (feedback & FB.StateChanged)
			this.window.redraw();  // render manager - redraw scene
	}
}


T findControl(T)(T root, const ref Point point)
{
	foreach (ref node; root)
	{
		auto translated_point = (!node.nested || node.parent is null) ?
				point :
				point - node.parent.position_abs();
		if (node.rect.contains(translated_point))
			return node;
	}
	return null;
}
