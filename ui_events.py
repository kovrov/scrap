# depth-first traversal

def propogate_mouse_hover_event(event):
	for widget in root.children:
		if widget.rect.contains(event.point):
			if widget.on_mouse_hover: widget.on_mouse_hover(event)
			break


def traverse(root):
	node = root
	while node:
		# sinking phase
		print node.name
		#
		if node.child:
			node = node.child
		elif node.next:
			node = node.next
		else:
			parent = node.parent
			node = None
			while parent:
				if parent.next:
					node = parent.next
					break
				parent = parent.parent


class Node:
	def __init__(self, name, parent=None):
		self.name = name
		self.child = None
		self.next = None
		self.parent = parent
		if (parent):
			parent.append(self)
	def append(self, new_child):
		if self.child:
			child = self.child
			while child:
				if not child.next:
					child.next = new_child
					break
				child = child.next
		else:
			self.child = new_child
#	def __str__(self):
#		return "%s(next:%s, child:%s)" % (self.name, str(self.next), str(self.child))

root = Node("root")
wnd = Node("wnd", root)
grp = Node("grp", wnd)
r1 = Node("r1", grp)
r2 = Node("r2", grp)
b1 = Node("b1", wnd)
l1 = Node("l1", wnd)
dlg = Node("dlg", root)
b2 = Node("b2", dlg)
b3 = Node("b3", dlg)
l2 = Node("l2", dlg)

#print root
traverse(root)
