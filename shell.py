#!/usr/bin/env python

import threading
import subprocess
PIPE, STDOUT = subprocess.PIPE, subprocess.STDOUT

args = ["cmd"]

def read_stdout(stdout):
	line = None
	while line != "":  # EOF
		line = stdout.readline()
		print repr(line)

p = subprocess.Popen(args, stdin=PIPE, stdout=PIPE, bufsize=0)
t = threading.Thread(target=read_stdout, args=[p.stdout])
t.start()

while True:
	try:
		p.stdin.write(raw_input()+"\n")
	except IOError:  # the only reliable way to know if process is closed
		break

t.join()
