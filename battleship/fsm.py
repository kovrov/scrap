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

	def __set_state(self, state_id):
		st = self.states[state_id]
		if st.on_enter:
			st.on_enter(self.context)
		self.current_state_id = state_id
		return state_id

	def dispatch(self, event_id, input_data):
		st = self.states.get(self.current_state_id)
		assert st, "STATE %s" % self.current_state_id
		event = st.events.get(event_id)
		if event is None:
			raise Exception("STATE %s have no EVENT %s" % (self.current_state_id, event_id))
		event.input(self.context, input_data)
		for tr in event.transitions:
			if tr.condition and tr.condition(self.context):
				if tr.action:
					tr.action(self.context)
				self.__set_state(tr.state)
				return

	def get_state(self):
		return self.current_state_id
