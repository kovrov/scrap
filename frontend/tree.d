

template Node()
{
	typeof(this) parent, child, lastChild, prev, next;
}


void setParent()(typeof(this) new_parent)
in
{
	assert (new_parent !is null);
}
body
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
	{
		assert (new_parent.lastChild is null);
		new_parent.child = this;
	}
	else
	{
		assert (new_parent.lastChild !is null);
		new_parent.lastChild.next = this;
		this.prev = new_parent.lastChild;
	}
	new_parent.lastChild = this;
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

/* for mouse cursor hit test */
int opApply(string SKIP_CONDITION_CODE)(int delegate(ref typeof(this)) dg)
{
	int result = 0;
	auto node = this;
	//int level;
	while (node !is null)
	{
		if (node.child !is null && mixin(SKIP_CONDITION_CODE))  // the node is an internal (inner) node
		{
			assert (node.lastChild !is null);
			node = node.child;
			//level++;
		}
		else if (node.next !is null)  // the node is a leaf
		{
			if (mixin(SKIP_CONDITION_CODE))
			{
				result = dg(node);
				if (result)
					break;
			}
			node = node.next;
		}
		else  // the node is a last leaf
		{
			if (node.parent !is null )
				assert (node is node.parent.lastChild);
			if (mixin(SKIP_CONDITION_CODE))
			{
				result = dg(node);
				if (result)
					break;
			}
			auto parent = node.parent;
			node = null;
			while (parent !is null)
			{
				result = dg(parent);
				if (result)
					break;
				//level--;
				if (parent.next)
				{
					node = parent.next;
					break;
				}
				parent = parent.parent;
			}
		}
	}
	return result;
}

/* for drawing */
int opApplyReverse(string SKIP_CONDITION_CODE)(int delegate(ref typeof(this)) dg)
{
	int result = 0;
	auto node = this;
	//int level;
	while (node !is null)
	{
		if (node.lastChild !is null && (mixin(SKIP_CONDITION_CODE)))  // the node is an internal (inner) node
		{
			assert (node.child !is null);
			result = dg(node);
			if (result)
				break;
			node = node.lastChild;
			//level++;
		}
		else if (node.prev !is null)  // the node is a leaf
		{
			if (mixin(SKIP_CONDITION_CODE))
			{
				result = dg(node);
				if (result)
					break;
			}
			node = node.prev;
		}
		else  // the node is a last leaf in sequence
		{
			if (node.parent !is null)
				assert (node is node.parent.child);
			if (mixin(SKIP_CONDITION_CODE))
			{
				result = dg(node);
				if (result)
					break;
			}
			auto parent = node.parent;
			node = null;
			while (parent !is null)
			{
				//level--;
				if (parent.prev)
				{
					node = parent.prev;
					break;
				}
				parent = parent.parent;
			}
		}
	}
	return result;
}
