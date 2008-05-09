
def set_state(context, state):
	st = context['states'][state]
	if st['on_enter']:
		st['on_enter'](context)
	context['state'] = state

def dispatch(context, event, input):
	st = context['states'].get(context['state'])
	assert st, "STATE %s" % context['state']
	ev = st['events'].get(event)
	if not ev:
		raise Exception("STATE %s have no EVENT %s" % (context['state'], event))
	ev['input'](context, input)
	for tr in ev['transitions']:
		if tr['condition'] and tr['condition'](context):
			if tr['action']:
				tr['action'](context)
			set_state(context, tr['state'])
			break

def get_state(context):
	return context['state']
