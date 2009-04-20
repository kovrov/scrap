#!/usr/bin/env python

import threading
import subprocess
import re
PIPE, STDOUT = subprocess.PIPE, subprocess.STDOUT


def read_stdout(stdout, callback):
	line = None
	while line != "":  # EOF
		line = stdout.readline()
		callback(line.strip())


class SubProcess(subprocess.Popen):
	def __init__(self, args, callback):
		super(SubProcess, self).__init__(args, stdin=PIPE, stdout=PIPE, bufsize=0)
		self.read_thread = threading.Thread(target=read_stdout, args=[self.stdout, callback])
		self.read_thread.start()

	def send(self, line):
		self.stdin.write(line+"\n")


def parse_features(string):
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
				real_value = value.strip('"\'')
				real_value = float(value)
				real_value = int(value)
			except: pass
			features[name] = real_value
		name = next_name
	return features
	

class GnuChessEngine(object):
	args = ["c:/soft/winboard/gnuches5.exe", "xboard"]
	move_patterns = (re.compile(r"(?P<NUMBER>\d)\. \.\.\. (?P<MOVE>\w+)"),
	                 re.compile(r"move (?P<MOVE>\w+)"))
	def __init__(self):
		self.process = SubProcess(self.args, self.process_command)
		self.process.send("xboard")
		self.process.send("protover 2")
		self.new()

	def new(self):
		self.process.send("new")
		self.process.send("random")

	def exit(self):
		self.process.send("exit")

	def move(self, move):
		print "# MY MOVE:", move
		self.process.send(move)

	def process_command(self, command):
		# check if this is a move.
		for pattern in self.move_patterns:
			match = pattern.match(command)
			if match:
				print "# ENGINE MOVE:", match.groupdict()["MOVE"]
				return
		# if not a move, then a command perhaps.
		if command.startswith("feature"):
			for name,value in parse_features(command[len("feature"):]).items():
				print (name,value)
			return
		# well, what ever...
		print repr(command)

	def wait_for_engine_move(self):
		self.__wait_for_engine_move = True
		pass

chess = GnuChessEngine()  # a new default game
chess.move("e2e4")  # by default we play as white
chess.wait_for_engine_move()
chess.move("g1f3")  # this move is allways safe as second one
chess.wait_for_engine_move()
chess.exit()  # terminate the engine
