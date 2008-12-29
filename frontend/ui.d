static import sys;
static import tree;
static import generic;
alias generic.Point!(short) Point;


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

	abstract FEEDBACK onMousePass(MOUSE_DIRECTION dir);
	abstract FEEDBACK onMouseMove(const ref Point pos/*, vect*/);
	abstract FEEDBACK onMouseDrag(const ref Point pos/*, vect*/, uint[] buttons/*, modifiers*/);
	abstract FEEDBACK onMouseButton(const ref Point pos, MOUSE_ACTION action, uint button/*, modifiers*/);
	abstract FEEDBACK onMouseScroll(int x, int y);
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

enum FEEDBACK
{
	NONE         = 0,
	Redraw       = 1,
	CaptureMouse = 1<<1,
	ReleaseMouse = 1<<2,
}

class EventManager(T /* : TargetNode */)
{
	T root;
	T tracked;
	T mouseOwner;
	sys.Window window;
	this(sys.Window window)
	{
		this.window = window;
	}

	protected
	void process(FEEDBACK feedback, T target)
	{
		if (feedback & FEEDBACK.CaptureMouse)
		{
			assert (this.mouseOwner is null);
			this.mouseOwner = target;
		}
		if (feedback & FEEDBACK.ReleaseMouse)
		{
			assert (this.mouseOwner !is null);
			this.mouseOwner = null;
		}
		if (feedback & FEEDBACK.Redraw)
			this.window.redraw();  // render manager - redraw scene
	}
import std.stdio;
	void dispatch_mouse_input(const ref Point pos, sys.MOUSE type)
	{
		auto target = (this.mouseOwner !is null) ? this.mouseOwner : findControl(this.root, pos);

		switch (type)
		{
		case sys.MOUSE.LEFT_DOWN:
			if (target !is null)
				this.process(target.onMouseButton(pos, MOUSE_ACTION.PRESS, 0/*, modifiers*/), target);
			break;
		case sys.MOUSE.LEFT_UP:
			if (target !is null)
				this.process(target.onMouseButton(pos, MOUSE_ACTION.RELEASE, 0/*, modifiers*/), target);
			break;
		case sys.MOUSE.MIDDLE_DOWN:
			break;
		case sys.MOUSE.MIDDLE_UP:
			break;
		case sys.MOUSE.RIGTH_DOWN:
			break;
		case sys.MOUSE.RIGTH_UP:
			break;
		case sys.MOUSE.MOVE:
			if (this.mouseOwner !is null)
			{
				if (!this.mouseOwner.rect.contains(pos - this.mouseOwner.parent.position_abs() ))
					target = null;
			}

			if (this.tracked !is target)
			{
				if (this.tracked !is null)
				{
					this.process(this.tracked.onMousePass(MOUSE_DIRECTION.LEAVE), this.tracked);
					//if (this.mouseOwner !is null)  // in case this.tracked just captured mouse
					//	target = this.mouseOwner;
				}
				this.tracked = target;
				if (target !is null)
				{
					this.process(target.onMousePass(MOUSE_DIRECTION.ENTER), target);
				}
			}

			if (this.mouseOwner !is null)  // tmp
				target = this.mouseOwner;

			if (target !is null)
				this.process(target.onMouseMove(pos), target);
			break;
		}
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
