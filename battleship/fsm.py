""" Very basic finite state machinery """

class State(object):
	__slots__ = ('on_enter', 'on_exit', 'events')
	def __init__(self, on_enter=None, on_exit=None, events=None):
		self.on_enter = on_enter
		self.on_exit = on_exit
		self.events = events

class Event(object):
	__slots__ = ('input', 'transitions')
	def __init__(self, input=None, transitions=None):
		self.input = input
		self.transitions = transitions

class Transition(object):
	__slots__ = ('condition', 'state', 'action')
	def __init__(self, condition=None, state=None, action=None):
		self.condition = condition
		self.state = state
		self.action = action

class Transducer:
	def __init__(self, states, initial_state, context):
		self.context = context
		self.states = states
		self.__set_state(initial_state)

	def __set_state(self, state):
		st = self.states[state]
		if st.on_enter:
			st.on_enter(self.context)
		self.state = state
		return state

	def dispatch(self, event, input):
		st = self.states.get(self.state)
		assert st, "STATE %s" % self.state
		ev = st.events.get(event)
		if not ev:
			raise Exception("STATE %s have no EVENT %s" % (self.state, event))
		ev.input(self.context, input)
		for tr in ev.transitions:
			if tr.condition and tr.condition(self.context):
				if tr.action:
					tr.action(self.context)
				self.__set_state(tr.state)
				return

	def get_state(self):
		return self.state
