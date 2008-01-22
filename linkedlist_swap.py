def get_nodes_by_value(llist, val1, val2):
	n = llist.first_node
	n1 = None
	n2 = None
	pren1 = None
	pren2 = None
	while n.next:
		prev = n
		n = n.next
		if n.value == val1:
			pren1 = prev
			n1 = n
		if n.value == val2:
			pren2 = prev
			n2 = n
		if n1 and n2:
			break
	return (pren1, n1, pren2, n2)

def get_nodes_by_index(llist, id1, id2):
	n1 = None
	n2 = None
	pren1 = None
	pren2 = None
	prev = None
	i = 0
	n = llist.first_node
	while n:
		if i == id1:
			pren1 = prev
			n1 = n
		if i == id2:
			pren2 = prev
			n2 = n
		if n1 and n2:
			break
		i += 1
		prev = n
		n = n.next
	return (pren1, n1, pren2, n2)

def swap_nodes_internal(pren1, n1, pren2, n2):
	assert n1 and pren2 and n2 # simpliest check
	# this is similar to:
	#  pren1.next = n2
	#  pren2.next = n1
	#  n1.next = n2.next
	#  n2.next = n1.next
	# but with temporary copies, to preserve values
	if pren1:
		if n1 is pren2: 
			(n1.next, n2.next, pren1.next) = (n2.next, n1, n2)
		else:
			(n1.next, n2.next, pren1.next, pren2.next) = (n2.next, n1.next, n2, n1)
	else:
		if n1 is pren2: 
			(pren2.next, n1.next, n2.next, pren1.next) = (n1, n2.next, n1, n2)
		else:
			(pren2.next, n1.next, n2.next) = (n1, n2.next, n1.next)

def swap(llist, id1, id2):
	 pren1, n1, pren2, n2 = get_nodes_by_index(llist, id1, id2)
	 swap_nodes_internal(pren1, n1, pren2, n2)

def swap_values(llist, val1, val2):
	 pren1, n1, pren2, n2 = get_nodes_by_value(llist, val1, val2)
	 swap_nodes_internal(pren1, n1, pren2, n2)


# TODO: tests
def get_list(llist):
	n = llist.first_node
	l = []
	while n:
		l.append(n.value)
		n = n.next
	return l

class LList:
	pass

class Node:
	def __repr__(self):
		next = self.next.value if self.next else "-"
		return "<" + self.value + ":" + next + ">"

l = LList()
n = l.first_node = Node()
n.value = "a"
a = n
n.next = Node()
n = n.next
n.value = "b"
b = n
"""
n.next = Node()
n = n.next
n.value = "c"
c = n
n.next = Node()
n = n.next
n.value = "d"
d = n
n.next = Node()
n = n.next
n.value = "e"
e = n
"""
n.next = None

#dbgl = [a,b,c,d,e]
#print dbgl

print "\n1 <=> 2\n", get_list(l)
swap(l, 0, 1)
print get_list(l)
