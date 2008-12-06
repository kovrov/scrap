static import generic;
alias generic.Point!(short) Point;
alias generic.Rect!(short, ushort) Rect;

static import tree;

class TargetNode
{
	union
	{
		Rect rect;
		struct
		{
			short x, y;
			ushort width, height;
		}
		static assert (Rect.sizeof == short.sizeof*2 + ushort.sizeof*2);
	}
	string name;

	mixin tree.Node;
	mixin tree.setParent;
	mixin tree.opApplyReverse;

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
}


enum MOUSE {MOVE}

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

class Manager
{
	alias void delegate (ref MouseEvent ev) MouseHandler;
	MouseHandler callback;
	void register(MouseHandler cb)
	{
		this.callback = cb;
	}
	void dispatch(ref MouseEvent ev)
	{
		switch (ev.type)
		{
		case MOUSE.MOVE:
			if (this.callback !is null)
				this.callback(ev);
			break;
		}
	}
}


TargetNode findControl(TargetNode root, const ref Point point)
{
	TargetNode best_match;
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
