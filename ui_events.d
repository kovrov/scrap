

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


class TargetNode
{
	private typeof(this) parent, child, next;
	union
	{
		Rect rect;
		struct
		{
			short x, y;
			ushort width, height;
		}
	}
	string name;

	this(string name, typeof(this) parent=null)
	{
		if (parent)
			this.setParent(parent);
		this.name = name;
	}
	//TODO: refactor to mixin
	private void setParent(typeof(this) new_parent)
	{
		if (this.parent !is null)
		{
			if (this.parent is new_parent)
				return;
			//this.parent.remove(this)
		}

		if (new_parent.child is null)
			new_parent.child = this;
		else
		{
			auto child = new_parent.child;
			while (child.next !is null)
				child = child.next;
			child.next = this;
		}
		this.parent = new_parent;
	}
	/*
	private void append(typeof(this) new_child)
	{
		if (new_child.parent !is null)
		{
			if (new_child.parent is this)
				return;
			//new_child.parent.remove(new_child)
		}

		if (this.child is null)
			this.child = new_child;
		else
		{
			auto child = this.child;
			while (child.next !is null)
				child = child.next;
			child.next = new_child;
		}
		new_child.parent = this;
	}
	*/
}


TargetNode findControl(TargetNode root, const ref Point point)
{
	auto node = root;
	while (node !is null)
	{
		writefln("%s(%s)", node.classinfo.name, node.name);

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
	return null;
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
	auto grp = new Group("grp", wnd);
	auto r1 = new Radio("r1", grp);
	auto r2 = new Radio("r2", grp);
	auto b1 = new Button("b1", wnd);
	auto l1 = new Label("l1", wnd);
	auto dlg = new Dialog("dlg", root);
	auto b2 = new Button("b2", dlg);
	auto b3 = new Button("b3", dlg);
	auto l2 = new Label("l2", dlg);

	findControl(root, Point(1,2));
}

