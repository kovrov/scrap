static import sys;
static import tree;
static import generic;
alias generic.Point!(short) Point;


enum FB
{
	NONE         = 0,
	StateChanged = 1,
	CaptureMouse = 1<<1,
	ReleaseMouse = 1<<2,
}

interface Activatable  // activate polycy interface
{
	ui.FB activate();
	//ui.FB deactivate();
}

interface Focusable  // focus policy interface
{
	//ui.FB focusOnKey();
	bool focusOnMouse(uint button);
}

/* this is important concept - injecting an interface into root of the class hierarchy */
class TargetNode(alias PAINT_INTERFACE)
{
	mixin PAINT_INTERFACE;

	mixin tree.Node;
	mixin tree.setParent;
	mixin tree.opApplyReverse;

	static typeof(this) activeNode;
	static Focusable focusedNode;

	bool overlapped;
	bool hidden;
	bool disabled;
	//parentnotify
	//group

	string name;
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
		auto parent = this.parent;
		while (parent)
		{
			abs_pos += parent.rect.position;
			parent = parent.parent;
		}
		return abs_pos;
	}

	abstract FB onMousePass(MOUSE_DIRECTION dir);
	abstract FB onMouseMove(const ref Point pos/*, vect*/);
	abstract FB onMouseDrag(const ref Point pos/*, vect*/, uint[] buttons/*, modifiers*/);
	abstract FB onMouseButton(const ref Point pos, MOUSE_ACTION action, uint button/*, modifiers*/);
	abstract FB onMouseScroll(int x, int y);
}

enum MOUSE_DIRECTION { ENTER, LEAVE }
enum MOUSE_ACTION { PRESS, RELEASE, DOUBLECLICK }

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

	void dispatch_mouse_input(const ref Point pos, sys.MOUSE type, int button = -1)
	{
		auto nodeUnderCursor = findControl(this.root, pos);
		auto target = (this.mouseHolder !is null) ? this.mouseHolder : nodeUnderCursor;
		switch (type)
		{
		case sys.MOUSE.PRESS:
			assert (button > -1);
			if (target is null || target.disabled)
				return;
			this.process(target.onMouseButton(pos, MOUSE_ACTION.PRESS, button/*, modifiers*/), target, pos);
			auto focusable = cast(Focusable)target;
			if (focusable !is null && T.focusedNode !is focusable && focusable.focusOnMouse(button))
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
			break;
		case sys.MOUSE.MOVE:
			auto newTarget = (this.mouseHolder is null || this.mouseHolder is nodeUnderCursor) ? nodeUnderCursor : null;
			if (this.mouseOldTarget !is newTarget)
				passMouse(newTarget, pos);
			if (target is null || target.disabled)
				return;
			this.process(target.onMouseMove(pos), target, pos);
			break;
		}
	}

	protected
	void passMouse(ref T target, const ref Point pos)
	{
		assert (this.mouseOldTarget !is target);

		if (this.mouseOldTarget !is null)
			this.process(this.mouseOldTarget.onMousePass(MOUSE_DIRECTION.LEAVE), this.mouseOldTarget, pos);
			//TODO: check if this.mouseOldTarget just captured mouse

		if (target !is null && !target.disabled)
			this.process(target.onMousePass(MOUSE_DIRECTION.ENTER), target, pos);

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
	T best_match;
	Point parent_abs_pos;
	auto node = root;
	while (node !is null)
	{
		if (node.child !is null)  // the node is an internal (inner) node
		{
			if (node.rect.contains(point - parent_abs_pos))
			{
				// save so far best matched target
				best_match = node;
			}
			parent_abs_pos += node.rect.position;
			node = node.child;
		}
		else
		{
			if (node.rect.contains(point - parent_abs_pos))
			{
				// first matched terminal node (leaf) is what we need
				return node;
			}

			if (node.next !is null)  // the node is a leaf
			{
				node = node.next;
				continue;
			}
			else  // the node is a last leaf
			{
				assert (node is node.parent.lastChild);
				if (best_match is node.parent)
				{
					// found best match
					return best_match;
				}
				auto parent = node.parent;
				node = null;
				while (parent !is null)
				{
					parent_abs_pos -= parent.rect.position;
					if (parent.next)
					{
						node = parent.next;
						break;
					}
					parent = parent.parent;
				}
			}
		}
	}
	return best_match;
}
