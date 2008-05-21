#include "fsm.h"
#include <exception>
#include <assert.h>

namespace fsm {


template <typename CTX, typename DATA>
Transducer<CTX,DATA>::Transducer(const std::map<int, State<CTX,DATA> >& states, int initial_state, CTX* context)
{
	p_context = context;
	m_states = states;
	SetState(initial_state);
}


template <typename CTX, typename DATA>
void Transducer<CTX,DATA>::Dispatch(int event_id, DATA& input) throw (InvalidEventException)
{
	std::map<int, State<CTX,DATA> >::iterator st = m_states.find(m_state);
	assert (st != m_states.end());
	std::map<int, Event<CTX,DATA> >::iterator ev = st->second.events.find(event_id);
	if (ev == st->second.events.end())
		throw InvalidEventException();
	ev->second.input(p_context, input);
	std::vector<Transition<CTX,DATA> >::iterator tr;
	for (tr = ev->second.transitions.begin(); tr != ev->second.transitions.end(); tr++)
	{
		if (tr->condition && tr->condition(p_context))
		{
			if (tr->action)
				tr->action(p_context);
			SetState(tr->state);
			return;
		}
	}
}


template <typename CTX, typename DATA>
int Transducer<CTX,DATA>::GetState()
{
	return m_state;
}


template <typename CTX, typename DATA>
int Transducer<CTX,DATA>::SetState(int state)
{
	State<CTX,DATA>& st = m_states[state];
	if (st.onEnter)
		st.onEnter(p_context);
	m_state = state;
	return state;
}




}  // namespace
