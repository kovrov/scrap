#!/usr/bin/env python

#-threaded-subprocess-----------------------------------------------------------
import threading
import subprocess
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


#-gnu-chess---------------------------------------------------------------------
import threading
import re


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
	args = ["xboard"]
	move_patterns = (re.compile(r"(?P<NUMBER>\d)\. \.\.\. (?P<MOVE>\w+)"),
	                 re.compile(r"move (?P<MOVE>\w+)"))
	def __init__(self, path="gnuches"):
		self.__engine_move = threading.Event()
		self.__engine_move.value = None  # just added a new property
		self.__engine_move.set()  # as engine pay for black
		self.__process = SubProcess([path]+self.args, self.process_command)
		self.__process.send("xboard")
		self.__process.send("protover 2")
		self.new()

	def new(self):
		self.__process.send("new")
		self.__process.send("random")

	def exit(self):
		self.__process.send("exit")

	def move(self, move):
		assert self.__engine_move.is_set()
		self.__engine_move.clear()
		self.__engine_move.value = None
		self.__process.send(move)  # with response?

	def process_command(self, command):
		# check if this is a move.
		for match in (p.match(command) for p in self.move_patterns):
			if match:
				assert not self.__engine_move.is_set()
				self.__engine_move.value = match.groupdict()["MOVE"]
				self.__engine_move.set()
				return
		# if not a move, then a command perhaps.
		if command.startswith("feature"):
			features = parse_features(command[len("feature"):])
			return
		# well, whatever...

	def engine_move(self, wait=False):
		if wait:
			self.__engine_move.wait()
		return self.__engine_move.value


#-------------------------------------------------------------------------------
chess = GnuChessEngine("c:/soft/winboard/gnuches5.exe")  # a new default game
print "my move: e2e4"
chess.move("e2e4")  # by default we play as white
print "engine move:", chess.engine_move(wait=True)
print "my move: g1f3"
chess.move("g1f3")  # this move is allways safe as second one
print "engine move:", chess.engine_move(wait=True)
print "exit"
chess.exit()  # terminate the engine
