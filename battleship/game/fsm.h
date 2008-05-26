#ifndef __BATTLESHIP_FSM_H
#define __BATTLESHIP_FSM_H

#pragma warning (disable: 4290) // exception specification ignored

#include <vector>
#include <map>
#include <exception>
#include <assert.h>


namespace fsm {


// forward declarations
template <typename CTX, typename DATA> struct State;
template <typename CTX, typename DATA> struct Event;
template <typename CTX, typename DATA> struct Transition;


// public API
template <typename CTX, typename DATA>
struct State
{
	State()
	{
		onEnter = NULL;
		onExit = NULL;
	}
	void (*onEnter)(CTX*); // CALLBACK
	void (*onExit)(CTX*);  // CALLBACK
	std::map<int, Event<CTX,DATA> > events;
};

template <typename CTX, typename DATA>
struct Event
{
	bool (*input)(CTX*, const DATA&);  // INPUT_VALIDATOR
	std::vector<Transition<CTX,DATA> > transitions;
	Event()
	{
		input = NULL;
	}
};

template <typename CTX, typename DATA>
struct Transition
{
	int state;
	bool (*condition)(CTX*);  // ACTION_CALLBACK
	void (*action)(CTX*);  // CALLBACK
	Transition()
	{
		condition = NULL;
		action = NULL;
	}
};


class InvalidEventException: public std::exception
{
};


template <typename CTX, typename DATA>
class Transducer
{
public:
	Transducer(const std::map<int, State<CTX,DATA> >& states, int initial_state, CTX* context)
	{
		assert (context != NULL);
		p_context = context;
		m_states = states;
		SetState(initial_state);
	}

	void Dispatch(int event_id, DATA& input) throw (InvalidEventException)
	{
		std::map<int, State<CTX,DATA> >::iterator st = m_states.find(m_state);
		assert (st != m_states.end());
		std::map<int, Event<CTX,DATA> >::iterator ev = (*st).second.events.find(event_id);
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

	int GetState()
	{
		return m_state;
	}

	int SetState(int state)
	{
		State<CTX,DATA>& st = m_states[state];
		if (st.onEnter)
			st.onEnter(p_context);
		m_state = state;
		return state;
	}

private:
	std::map<int, State<CTX,DATA> > m_states;
	int m_state;
	CTX* p_context;
};


}  // namespace


#endif // __BATTLESHIP_FSM_H
