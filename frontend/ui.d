static import sys;
static import tree;
static import generic;
alias generic.Point!(short) Point;


enum MOUSE { MOVE=1, LEAVE, UP, DOWN }

/* this is important concept - injecting an interface into root of the class hierarchy */
class TargetNode(alias PAINT_INTERFACE)
{
	mixin PAINT_INTERFACE;

	mixin tree.Node;
	mixin tree.setParent;
	mixin tree.opApplyReverse;

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

	MOUSE mouseEventMask;
	abstract ui.FEEDBACK onMouse(ref MouseEvent);
}

enum FEEDBACK
{
	NONE = 0,
	Redraw = 1,
	TrackMouse = 1<<1,
	CaptureMouse = 1<<2,
}

class EventManager(T /* : TargetNode */)
{
	T root;
	T tracked;
	sys.Window window;
	this(sys.Window window)
	{
		this.window = window;
	}

	protected
	void process(FEEDBACK feedback, T target)
	{
		if (feedback & FEEDBACK.TrackMouse)
			this.tracked = target;
		if (feedback & FEEDBACK.Redraw)
			this.window.redraw();  // render manager - redraw scene
	}

	void dispatch_mouse_input(const ref Point pos, sys.MOUSE type)
	{
		auto target = findControl(this.root, pos);

		if (this.tracked !is null && this.tracked !is target)
		{
			auto old_target = this.tracked;
			this.tracked = null;
			this.process(old_target.onMouse(MouseEvent(MOUSE.LEAVE, pos)), old_target);
		}

		if (target !is null && target.mouseEventMask & MOUSE.MOVE)
		{
			this.process(target.onMouse(MouseEvent(MOUSE.MOVE, pos)), target);
		}
	}
}

struct MouseEvent
{
	MOUSE type;
	Point pos;

	this (MOUSE type, ref Point pos)
	{
		this.type = type;
		this.pos = pos;
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
