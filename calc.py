"""
mul (a*b)
sub (a-b)
div (a/b)
add (a+b)
r (a**(1.0/b))
pow (a**b)
mod (a%b)
"""


#in ['push 3', 'push 2', 'add', 'push 1', 'add']
#out 6
def calculate(statements):
	#print statements
	stack = []
	for s in statements:
		if s.startswith('push'):
			stack.append(int(s.split()[1]))
		elif s == 'add':
			a = stack.pop()
			b = stack.pop()
			stack.append(a+b)
		elif s == 'root':
			a = stack.pop()
			b = stack.pop()
			stack.append(a**(1.0/b))
		elif s == 'sub':
			a = stack.pop()
			b = stack.pop()
			stack.append(a-b)
		elif s == 'mul':
			a = stack.pop()
			b = stack.pop()
			stack.append(a*b)
		elif s == 'div':
			a = stack.pop()
			b = stack.pop()
			stack.append(a/b)
		elif s == 'pow':
			a = stack.pop()
			b = stack.pop()
			stack.append(a**b)
		elif s == 'mod':
			a = stack.pop()
			b = stack.pop()
			stack.append(a%b)
	return stack[0]



#in ('1+(2+3)')
#out ['1', '+', '(', '2', '+', '3', ')']
def tokenize(s):
	res = []
	digit = ''
	for c in s:
		if c == ' ':
			pass
		elif c.isdigit():
			digit += c
		else:
			if len(digit):
				res.append(digit)
			digit = ''
			res.append(c)
	if len(digit):
		res.append(digit)
	#print "###", res
	return res


#in tokenize('1+(2-3)*2')
#out ['1', '+', [ '2', '-', '3', ] '*', '2',]
def parse(tokens):
	#print "parse(%s)" % tokens
	current = []
	res = current
	stack = [current]
	for i in tokens:
		if i == '(':
			stack.append([])
			current.append(stack[-1])
			current = stack[-1]
		elif i == ')':
			stack.pop()
			current = stack[-1]
		else:
			current.append(i)
	#print " ", res
	return res

opmap = {
	'*':'mul',
	'-':'sub',
	'/':'div',
	'+':'add',
	'r':'root',
	'^':'pow',
	'%':'mod'}
#in calculate(visit(parse(tokenize('1+(2+3)'))))
#out 6
def visit(tree):
	print "visit(%s)" % tree
	res = []
	ops = []
	def unfold(nodes):
		for i in reversed(nodes):
			if type(i) is list:
				unfold(i)
			else:
				if i.isdigit():
					res.append('push ' + i)
				if ops:
					for op in ops:
						res.append(opmap[op])
					ops[:] = []
				if not i.isdigit():
					ops.append(i)
	unfold(tree)
	print " ", res
	return res



def test():
	#calculator tests (1)
	assert calculate(['push 1', 'push 2', 'add']) == 3
	assert calculate(['push 2', 'push 100', 'root']) == 10.0
	assert calculate(['push 10', 'push 20', 'sub', 'push 5', 'add', 'push 5', 'push 100', 'mul', 'div']) == 33

	#tokenizer tests (2)
	assert list(tokenize('1+(2+3)')) == ['1', '+', '(', '2', '+', '3', ')']
	assert list(tokenize('100 r 10 % 5 ^ 1 - 10 *20+3')) == ['100', 'r', '10', '%', '5', '^', '1', '-', '10', '*', '20', '+', '3']
	assert list(tokenize('(1+2) * (3/4)')) == ['(', '1', '+', '2', ')', '*', '(', '3', '/', '4', ')']

	#parser tests (3)
	assert parse(tokenize('1+(2+3)')) == ['1', '+', ['2', '+', '3']]
	assert parse(tokenize('((1/2)*(2+(5r3)))-5')) == [[['1', '/', '2'], '*', ['2', '+', ['5', 'r', '3']]], '-', '5']

	#visit tests (4)
	assert list(visit(parse(tokenize('1+(2+3)')))) == ['push 3', 'push 2', 'add', 'push 1', 'add']
	assert list(visit(parse(tokenize('((1/2)*(3+(4r5)))-6')))) == ['push 6', 'push 5', 'push 4', 'root', 'push 3', 'add', 'push 2', 'push 1', 'div', 'mul', 'sub']

	#final tests
	assert calculate(visit(parse(tokenize('1+(2+3)')))) == 6
	assert abs(calculate(visit(parse(tokenize('((10*10) + (5*5)) r 2')))) - 11.1803398875) < 0.00001
	assert abs(calculate(visit(parse(tokenize('((1./2.)*(3.+(4.r5.)))-6.')))) + 3.84024604461) < 0.00001

if __name__ == "__main__":
	test()
