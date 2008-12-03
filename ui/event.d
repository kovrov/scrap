

struct Point
{
	short x, y;
	const Point opAdd(const ref Point other) { return Point(x +  other.x, y +  other.y); }
	const Point opSub(const ref Point other) { return Point(x -  other.x, y -  other.y); }
	void opAddAssign(const ref Point other)               { x += other.x; y += other.y; }
	void opSubAssign(const ref Point other)               { x -= other.x; y -= other.y; }
}
struct Size { ushort width, height; }

struct Rect
{
	//union
	//{
		Point position;//origin;
	//	struct{ short x, y; }
	//}
	//union
	//{
		Size size;
	//	struct{ ushort width, height; }
	//}

	bool contains(const ref Point point)
	{
		return position.x <= point.x && position.y <= point.y &&
				point.x <= position.x + size.width && point.y <= position.y + size.height;
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
		auto pos = parent_abs_pos + node.rect.position;
		writef("%*s%s [%d,%d]", indent*2, "" , node.name, pos.x, pos.y);
		auto tmp = point - parent_abs_pos;
		writef("   {[%d,%d].contains([%d,%d])}", node.rect.position.x, node.rect.position.y, tmp.x, tmp.y);

		if (node.child !is null)  // the node is an internal (inner) node
		{
			if (node.rect.contains(point - parent_abs_pos))
			{
				if (best_match is node.parent)
				{
					writef(" #best_match");
					best_match = node;
				}
			}
			parent_abs_pos += node.rect.position;
			indent++;
			node = node.child;
		}
		else if (node.next !is null)  // the node is a leaf
		{
			if (node.rect.contains(point - parent_abs_pos))
			{
				writefln(" #found");
				return node;
			}
			node = node.next;
		}
		else  // the node is a last leaf
		{
			if (node.rect.contains(point - parent_abs_pos))
			{
				writefln(" #found");
				return node;
			}
			if (best_match is node.parent)
			{
				writefln(" #found best_match");
				return best_match;
			}
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
		writefln();
	}
	writefln(" #return best_match");
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
	  auto dlg = new Dialog("dlg", root);
	  dlg.rect = Rect(Point(200,200),Size(400,200));  // [200,200-600,400]
	    auto b2 = new Button("b2", dlg);
	    b2.rect = Rect(Point(10,10),Size(18,48));     // [210,210-228,258]
	    auto b3 = new Button("b3", dlg);
	    b3.rect = Rect(Point(10,40),Size(20,50));     // [210,240-230,290]
	    auto l2 = new Label("l2", dlg);
	    l2.rect = Rect(Point(10,70),Size(20,50));     // [210,270-230,320]
	  auto wnd = new Window("wnd", root);
	  wnd.rect = Rect(Point(100,100),Size(400,200));  // [100,100-500,300]
	    auto b1 = new Button("b1", wnd);
	    b1.rect = Rect(Point(10,170),Size(20,30));    // [110,270-130,300]
	    auto l1 = new Label("l1", wnd);
	    l1.rect = Rect(Point(40,170),Size(20,30));    // [150,440-170,470]
	    auto grp = new Group("grp", wnd);
	    grp.rect = Rect(Point(10,10),Size(290,150));  // [110,110-400,260]
	      auto r1 = new Radio("r1", grp);
	      r1.rect = Rect(Point(10,10),Size(10,50));   // [120,120-130,170]
	      auto r2 = new Radio("r2", grp);
	      r2.rect = Rect(Point(10,30),Size(10,50));   // [120,140-130,190]

	auto target = findControl(root, Point(600,400));
	writefln("%s: %s", target, target?target.name:"-");
}
