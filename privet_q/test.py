#!/usr/bin/python

file = open('c:/data/desktop/data.txt', 'r')
try:
	res = {}
	for line in file:
		(digit, letters) = line.split(':')
		for char in letters.split():
			if char in res:
				res[char] += digit
			else:
				res[char] = [digit]
finally:
	file.close()

for char, digits in sorted(res.iteritems()):
	print "%s: %s" % (char, " ".join(digits))
