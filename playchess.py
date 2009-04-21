#!/usr/bin/env python

import re
import threading
import subprocess
PIPE, STDOUT = subprocess.PIPE, subprocess.STDOUT
import logging
logging.basicConfig(level=logging.INFO)


def read_stdout(stdout, callback):
	line = None
	while line != "":  # EOF
		line = stdout.readline()
		callback(line.strip())


def parse_features(features_string):
	patterns = (re.compile(r"""^([\w_-]+)\s*=\s*["]([^"]+)["]\s*(.*)$"""),
				re.compile(r"""^([\w_-]+)\s*=\s*[']([^']+)[']\s*(.*)$"""),
				re.compile(r"""^([\w_-]+)\s*=\s*([^ \t'"]+)\s*(.*)$"""))
	features = {}
	next_string = features_string.strip()
	while next_string:
		for match in (m for m in (p.match(next_string) for p in patterns) if m):
			name, value, next_string = match.groups()
			features[name] = value
			break
		else:
			raise Exception("can't parse features string - not a properly formed")
	return features
	

class GnuChessEngine(object):
	__args = ["xboard"]
	__move_patterns = (re.compile(r"(?P<NUMBER>\d)\. \.\.\. (?P<MOVE>\w+)"),
	                   re.compile(r"move (?P<MOVE>\w+)"))

	def __init__(self, path="gnuches"):
		self.__process = subprocess.Popen([path]+self.__args, stdin=PIPE, stdout=PIPE, bufsize=0)
		self.read_thread = threading.Thread(target=read_stdout, args=[self.__process.stdout, self.__receive])
		self.read_thread.start()

		self.__send("xboard")
		self.__send("protover 2")
		self.__engine_move = threading.Event()
		self.__engine_move.value = None #  "value" is not part of threading.Event
		# similary for hint by chess engine
		self.__engine_hint = threading.Event()
		self.__engine_hint.value = None #  ditto
		#  start new chess game
		self.new()

	def new(self):
		self.__engine_move.set()  # as engine pays black
		self.__send("new")
		self.__send("random")

	def exit(self):
		self.__send("exit")

	def play(self, move):
		self.__engine_hint.clear()
		self.__engine_hint.value = None
		assert self.__engine_move.is_set()
		self.__engine_move.clear()
		self.__engine_move.value = None
		self.__send(move)  # with response?

	def __send(self, command):
		logging.info("engine << %s",repr(command))
		self.__process.stdin.write(command+"\n")

	def __receive(self, command):
		logging.info("engine >> %s",repr(command))
		# check if this is a move.
		for match in (p.match(command) for p in self.__move_patterns):
			if match:
				self.__engine_hint.clear()
				self.__engine_hint.value = None
				assert not self.__engine_move.is_set()
				self.__engine_move.value = match.groupdict()["MOVE"]
				self.__engine_move.set()
				return
		# if not a move, then a command perhaps.
		if command.startswith("feature"):  # typically response for "protover"
			features = parse_features(command[len("feature"):].strip())
			return
		if command.startswith("Hint:"):  # typically response for "hint"
			assert not self.__engine_hint.is_set()
			self.__engine_hint.value = command[len("Hint:"):].strip()
			self.__engine_hint.set()
			return
		# well, whatever...

	def get_move(self, wait=False):
		if wait:
			self.__engine_move.wait()
		return self.__engine_move.value

	def hint(self):
		self.__send("hint")
		self.__engine_hint.wait()
		return self.__engine_hint.value


#-------------------------------------------------------------------------------
engine = GnuChessEngine("c:/soft/winboard/gnuches5.exe")  # a new default game
print "engine hint:", engine.hint()
print "my move: e2e4"
engine.play("e2e4")  # by default we play as white
print "engine move:", engine.get_move(wait=True)
print "engine hint:", engine.hint()
print "my move: g1f3"
engine.play("g1f3")  # this move is allways safe as second one
print "engine move:", engine.get_move(wait=True)
engine.exit()  # terminate the engine
