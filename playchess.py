#!/usr/bin/env python

import re
import threading
import subprocess
PIPE, STDOUT = subprocess.PIPE, subprocess.STDOUT
import logging
logging.basicConfig(level=logging.INFO)


def synchronized(f):
	r_lock = threading.RLock()
	def wrapper(*args):
		with r_lock:
			return f(*args)
	wrapper.__name__ = f.__name__
	wrapper.__dict__ = f.__dict__
	wrapper.__doc__ = f.__doc__
	return wrapper


def read_stdout(stdout, callback):
	line = None
	while line != "":  # EOF
		line = stdout.readline()
		callback(line.strip())


def parse_features(features_string):
	patterns = (re.compile(r"""^(\w+)\s*=\s*"([^"]+)"\s*(.*)$"""),
				re.compile(r"""^(\w+)\s*=\s*'([^']+)'\s*(.*)$"""),
				re.compile(r"""^(\w+)\s*=\s*([^\s'"]+)\s*(.*)$"""))
	features = {}
	next_string = features_string.strip()
	while next_string:
		for match in (m for m in (p.match(next_string) for p in patterns) if m):
			name, value, next_string = match.groups()
			try:
				value = float(value)
				value = int(value)
			except: pass
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
		self.__can_send = threading.Event()
		self.__can_send.set()
		self.__process = subprocess.Popen([path]+self.__args, stdin=PIPE, stdout=PIPE, bufsize=0)
		self.read_thread = threading.Thread(target=read_stdout, args=[self.__process.stdout, self.__receive])
		self.read_thread.start()
		self.__send("xboard")
		self.__set_protover()
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

	@synchronized
	def __send(self, command):
		self.__can_send.wait()
		logging.info("engine << %s", repr(command))
		self.__process.stdin.write(command+"\n")

	@synchronized
	def __receive(self, command):
		logging.info("engine >> %s", repr(command))
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
			self.__receive_features(parse_features(command[len("feature"):].strip()))
			return
		if command.startswith("Hint:"):  # typically response for "hint"
			assert not self.__engine_hint.is_set()
			self.__engine_hint.value = command[len("Hint:"):].strip()
			self.__engine_hint.set()
			return
		# well, whatever...

	def __set_protover(self):
		assert self.__can_send.is_set()
		#  Send "protover" command, and block output fot 2 seconds,
		#  while expecting "features" from the engine.
		self.__can_send.timer = threading.Timer(2.0, lambda: self.__can_send.set())
		self.__send("protover 2")
		self.__can_send.clear()  # block __send
		self.__can_send.timer.start()

	def __receive_features(self, features):
		#features['setboard']
		#features['analyze']
		#features['ping']
		#features['draw']
		#features['sigint']
		#features['variants']
		self.name = features['myname']
		if features.get("done", None):
			self.__can_send.timer.cancel()
			del self.__can_send.timer
			self.__can_send.set()

	def get_move(self, wait=False):
		if wait:
			self.__engine_move.wait()
		return self.__engine_move.value

	def hint(self):
		self.__send("hint")
		self.__engine_hint.wait()
		return self.__engine_hint.value

"""
#-------------------------------------------------------------------------------
engine = GnuChessEngine("c:/soft/winboard/gnuches5.exe")  # a new default game
print "playing against", engine.name
print "engine hint:", engine.hint()
print "my move: e2e4"
engine.play("e2e4")  # by default we play as white
print "engine move:", engine.get_move(wait=True)
print "engine hint:", engine.hint()
print "my move: g1f3"
engine.play("g1f3")  # this move is allways safe as second one
print "engine move:", engine.get_move(wait=True)
engine.exit()  # terminate the engine
#-------------------------------------------------------------------------------
"""

engine_features = {
	'draw': 0,
	'ping': 1,
	'sigint': 0,
	'myname': 'GNU Chess 5.07',
	'done': 1,
	'setboard': 1,
	'variants': 'normal',
	'analyze': 1,
}

features = {
	'ping':      False,  # (True)
	'setboard':  False,  # (True)
	'playother': False,  # (True)
	'san':       False,
	'usermove':  False,
	'time':      True,  # (True)
	'draw':      True,  # (True)
	'sigint':    True,
	'sigterm':   True,
	'reuse':     True,  # (True)
	'analyze':   True,  # (True)
	'myname':    "",
	'variants':  [],
	'colors':    True,  # (False)
	'ics':       False,
	'name':      False,
	'pause':     False,
}


resp = ("rejected","accepted")
for name, value in engine_features.iteritems():
	print "%s : %s (%s)" % (name, value, resp[features.get(name, None) == value])
