#!/usr/bin/env python

import threading
import subprocess
PIPE, STDOUT = subprocess.PIPE, subprocess.STDOUT


"""
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
"""

class SubProcess(subprocess.Popen):
	def __init__(self, args):
		super(SubProcess, self).__init__(args, stdin=PIPE, stdout=PIPE, bufsize=0)
	def send(self, line):
		self.stdin.write(line+"\n")
	def send_receive(self, line, callback):
		self.stdin.write(line+"\n")
		callback(self.stdout.readline().strip())


class GnuChessEngine(object):
	args = ["c:/soft/winboard/gnuches5.exe", "xboard"]
	def __init__(self):
		self.process = SubProcess(self.args)
		self.process.send("xboard")
		def accept_features(string):
			features = {}; value = None; name = None
			for i in string.split("="):
				try:
					value, next_name = i.rsplit(" ",1)
				except:
					if name is None:
						next_name = i
					else:
						value = i
				if name is not None:
					try:
						real_value = value.strip('"')
						real_value = float(value)
						real_value = int(value)
					except: pass
					features[name] = real_value
				name = next_name
			for f,v in features.items():
				print (f,v)
		self.process.send_receive("protover 2", accept_features)
	def demo(self):
		self.process.send("new")
		self.process.send("random")
		self.process.send("exit")

chess = GnuChessEngine()
chess.demo()
