

class State(object):
	__slots__ = ['on_enter', 'on_exit', 'events']
	def __init__(self, on_enter=None, on_exit=None, events=None):
		self.on_enter = on_enter
		self.on_exit = on_exit
		self.events = events

class Event(object):
	__slots__ = ['input', 'transitions']
	def __init__(self, input=None, transitions=None):
		self.input = input
		self.transitions = transitions

class Transition(object):
	__slots__ = ['condition', 'state', 'action']
	def __init__(self, condition=None, state=None, action=None):
		self.condition = condition
		self.state = state
		self.action = action


def set_state(context, state):
	#print "### SET_STATE:", state
	st = context['states'][state]
	if st.on_enter:
		st.on_enter(context)
	context['state'] = state
	#context['on_state_changed'](state)
	return state

def dispatch(context, event, input):
	#print "### DISPATCH:", event, input
	st = context['states'].get(context['state'])
	assert st, "STATE %s" % context['state']
	ev = st.events.get(event)
	if not ev:
		raise Exception("STATE %s have no EVENT %s" % (context['state'], event))
	ev.input(context, input)
	for tr in ev.transitions:
		if tr.condition and tr.condition(context):
			if tr.action:
				tr.action(context)
			set_state(context, tr.state)
			return
	#set_state(context, context['state'])

def get_state(context):
	#print "### GET_STATE"
	return context['state']
