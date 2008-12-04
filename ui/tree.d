

template Node()
{
	typeof(this) parent, child, prev, next;
}


void setParent()(typeof(this) new_parent)
{
	if (this.parent !is null)
	{
		if (this.parent is new_parent)
			return;

		if (this.prev !is null)
		{
			assert (this.prev.parent is this.parent);
			this.prev.next = this.next;
		}

		if (this.next !is null)
		{
			assert (this.next.parent is this.parent);
			this.next.prev = this.prev;
		}

		this.prev = null;
		this.next = null;
		this.parent = null;
	}

	if (new_parent.child is null)
		new_parent.child = this;
	else
	{
		auto last_child = new_parent.child;
		while (last_child.next !is null)
			last_child = last_child.next;
		last_child.next = this;
		this.prev = last_child;
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


// finds lowest matched leaf using depth-first traversal
T deepSearch(T, P)(T root, P predicate)
{
	T target;
	auto node = root;
	while (node !is null)
	{
		if (node.child !is null)
		{
			// we in an internal (inner) node
			node = node.child;
		}
		else if (node.next !is null)
		{
			// we in a leaf
			node = node.next;
		}
		else
		{
			// we in a last leaf
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
	return target;
}

T traverse(T, C)(T root, C visitor)
{
	T target;
	auto node = root;
	while (node !is null)
	{
		if (node.child !is null)
		{
			// we in an internal (inner) node
			visitor(node);
			node = node.child;
		}
		else if (node.next !is null)
		{
			// we in a leaf
			visitor(node);
			node = node.next;
		}
		else
		{
			// we in a last leaf
			visitor(node);
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
	return target;
}
