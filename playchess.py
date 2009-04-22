#!/usr/bin/env python
"""
Chess Engine Communication Protocol states:

init_mode
	* feature receive
	* feature accept|reject

move_mode
	* send move
	* offer draw?
	* new|end game?

wait_mode
	* accept move
	* offer draw?
	* new|end game?

ping_mode
	?

"""
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
	next_str = features_string.strip()
	while next_str:
		for match in (m for m in (p.match(next_str) for p in patterns) if m):
			name, value_str, next_str = match.groups()
			try:
				value = float(value_str)
				value = int(value_str)
				value = value_str
			except: pass
			features[name] = value
			break
		else:
			raise Exception("can't parse features string - not a properly formed")
	return features
	

class GnuChessEngine(object):
	__args = ["xboard"]
	__receive_move_patterns = (re.compile(r"move (?P<MOVE>\w+)")),
			re.compile(r"(?P<NUMBER>\d)\. \.\.\. (?P<MOVE>\w+)"),
	__receive_illigalmove_patterns = re.compile(r"Illegal move: (?P<MOVE>\w+)"),
			re.compile(r"Illegal move \((?P<REASON>[\w\s]+)\): (?P<MOVE>\w+)")

	def __init__(self, path="gnuches"):
		#  default config
		self.__send_move_format = "%s"
		self.__may_offer_draw = False
		self.__pingable = False
		#  rest of initialization
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
		for match in (p.match(command) for p in self.__receive_move_patterns):
			if match:
				self.__engine_hint.clear()
				self.__engine_hint.value = None
				assert not self.__engine_move.is_set()
				self.__engine_move.value = match.groupdict()["MOVE"]
				self.__engine_move.set()
				return
		for match in (p.match(command) for p in self.__receive_illigalmove_patterns):
			if match:
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
		if command == "offer draw":  # engine wants to offer a draw by agreement
			return
		if command == "resign":  # engine wants to resign
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

	def ping(self):
		if not self.__pingable:
			raise Exception("ping not implemented")
		#self.__block_mode("ping", ):
		self.__send("ping")

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

default_features = {
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
	'myname':    None,
	'variants':  [],
	'colors':    True,  # (False)
	'ics':       False,
	'name':      None,
	'pause':     False,
}

desired_features = {
	'ping':      True, #
	'setboard':  True, #
	'playother': True, #
	'time':      True, #
	'draw':      True, # self.__may_offer_draw = Frue
	'reuse':     True, #
	'analyze':   True, #
	'myname':    None,  # don't care
	'variants':  "normal",
	'colors':    False, # don't like
	'name':      None,  # don't care
}


resp = ("rejected","accepted")

for key in set(engine_features) & set(desired_features):
	print "%s: %s == %s" % (key, engine_features[key], desired_features[key]),
	if desired_features[key] is None:  # don't care - accept
		print "(%s)" % resp[True]
	else:
		print "(%s)" % resp[engine_features[key] == desired_features[key]]


#  Commands from the engine to xboard

#  feature FEATURE1=VALUE1 FEATURE2=VALUE2 ...
startswith(r'''feature ''')

#  Illegal move: MOVE
re.compile(r'''^Illegal move: (?P<MOVE>\w+)'''),

#  Illegal move (REASON): MOVE
re.compile(r'''^Illegal move \((?P<REASON>[\w\s]+)\): (?P<MOVE>\w+)''')

#  Error (ERRORTYPE): COMMAND
re.compile('''Error (ERRORTYPE): COMMAND''')

#  move MOVE
re.compile(r'''^move (?P<MOVE>\w+)''')),
re.compile(r'''^(?P<NUMBER>\d)\. \.\.\. (?P<MOVE>\w+)''')

#  RESULT {COMMENT}
re.compile(r'''^RESULT {COMMENT}''')

#  resign
       == '''resign'''

# offer draw
       == '''offer draw'''

# tellopponent MESSAGE
startswith('''tellopponent ''') # MESSAGE

# tellothers MESSAGE
startswith('''tellothers ''') # MESSAGE

# tellall MESSAGE
startswith('''tellall ''') # MESSAGE

# telluser MESSAGE
startswith('''telluser ''') # MESSAGE

# tellusererror MESSAGE
startswith('''tellusererror ''') # MESSAGE

# askuser REPTAG MESSAGE
re.compile(r'''^askuser REPTAG MESSAGE''')

# tellics MESSAGE
startswith('''tellics ''') # MESSAGE

# tellicsnoalias MESSAGE
startswith('''tellicsnoalias ''') # MESSAGE

# # COMMENT
startswith(r'''#''') # COMMENT
