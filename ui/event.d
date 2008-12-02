

struct Point
{
	short x, y;
	void opAddAssign(const ref Point other) { x += other.x; y += other.y; }
	void opSubAssign(const ref Point other) { x -= other.x; y -= other.y; }
}
struct Size { ushort width, height; }

struct Rect
{
	union
	{
		struct{ short x, y; }
		Point position;//origin;
	}
	union
	{
		struct{ ushort width, height; }
		Size size;
	}

	bool contains(const ref Point point)
	{
		return x <= point.x && y <= point.y &&
				point.x <= x + width && point.y <= y + height;
	}
}


import tree;

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

	this(string name, typeof(this) parent=null)
	{
		if (parent)
			this.setParent(parent);
		this.name = name;
	}
}


TargetNode findControl(TargetNode root, const ref Point point)
{
	TargetNode best_match;
	int indent = 0;
	Point parent_abs_pos;
	auto node = root;
	while (node !is null)
	{
		writefln("%*s%s", indent*2, "" , node.name);

		if (node.child !is null)
		{
			// the node is an internal (inner) node
		//	if (match(node))
		//		best_match = node;
			parent_abs_pos += node.rect.position;
			indent++;
			node = node.child;
		}
		else if (node.next !is null)
		{
			// the node is a leaf
		//	if (match(node))
		//		return node;
			node = node.next;
		}
		else
		{
			// the node is a last leaf
		//	if (match(node))
		//		return node;
		//	if (best_match is node.parent)
		//		return best_match;
			auto parent = node.parent;
			node = null;
			while (parent !is null)
			{
				indent--;
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
	return best_match;
}


class Window : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Group : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Radio : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Button : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Label : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Dialog : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}



import std.stdio;

void main()
{
	auto root = new TargetNode("root");
	root.rect.size = Size(640,480);
	auto wnd = new Window("wnd", root);
	wnd.rect = Rect((100,100),(400,200));
	auto b1 = new Button("b1", wnd);
	b1.rect = Rect((10,170),(20,30));
	auto l1 = new Label("l1", wnd);
	l1.rect = Rect((40,170),(20,30));
	auto grp = new Group("grp", wnd);
	grp.rect = Rect((10,10),(290,150));
	auto r1 = new Radio("r1", grp);
	r1.rect = Rect((10,10),(10,50));
	auto r2 = new Radio("r2", grp);
	r2.rect = Rect((10,30),(10,50));
	auto dlg = new Dialog("dlg", root);
	dlg.rect = Rect((200,200),(400,200));
	auto b2 = new Button("b2", dlg);
	b2.rect = Rect((10,10),(18,48));
	auto b3 = new Button("b3", dlg);
	b3.rect = Rect((10,40),(20,50));
	auto l2 = new Label("l2", dlg);
	l2.rect = Rect((10,70),(20,50));

	findControl(root, Point(1,2));
}

