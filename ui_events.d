

struct Point { short x, y; }
struct Size { ushort width, height; }

struct Rect
{
	union
	{
		Point position;//origin;
		struct{ short x, y; }
	}
	union
	{
		Size size;
		struct{ ushort width, height; }
	}

	bool contains(const ref Point point)
	{
		return x <= point.x && y <= point.y &&
				point.x <= x + width && point.y <= y + height;
	}
}




void findControl(Node root)
{
	auto node = root;
	while (node !is null)
	{
		// sinking phase
		writefln("depth-first.. %s", node.name);
		//
		if (node.child !is null)
			node = node.child;
		else if (node.next !is null)
			node = node.next;
		else
		{
			auto parent = node.parent;
			node = null;
			while (parent !is null)
			{
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


class Node
{
	Node child, next, parent;
	string name;

	this(string name, Node parent=null)
	{
		if (parent)
			parent.append(this);
		this.name = name;
	}
	void append(Node new_child)
	{
		if (this.child is null)
			this.child = new_child;
		else
		{
			auto child = this.child;
			while (child.next !is null)
				child = child.next;
			child.next = new_child;
			new_child.parent = this;
		}
	}
}





import std.stdio;

void main()
{
	/*
	Rect r;
	r.x = 1;
	r.y = 2;
	r.width = 32;
	r.height = 18;
	Point p = Point(34,20);
	writefln("%s contains %s: ", r, p, r.contains(p));
	*/

	auto root = new Node("root");
	auto wnd = new Node("wnd", root);
	auto grp = new Node("grp", wnd);
	auto r1 = new Node("r1", grp);
	auto r2 = new Node("r2", grp);
	auto b1 = new Node("b1", wnd);
	auto l1 = new Node("l1", wnd);
	auto dlg = new Node("dlg", root);
	auto b2 = new Node("b2", dlg);
	auto b3 = new Node("b3", dlg);
	auto l2 = new Node("l2", dlg);

	//print root
	findControl(root);
}

