#pragma once

#include <vector>


namespace fsm {


struct State;


struct Event
{
	Event(int id) { m_event = id; }

	template <class T>
	void addTransition(bool (*callback)(void), T* ctx, State* state)
	{
	}

private:
	int m_event;
};


struct State
{
	State(int id) { m_state = id; }
	template <class T>
	Event* addEvent(int event_id, bool (*callback)(void), T* ctx)
	{
		m_events.push_back(Event(event_id));
		return &m_events.back();
	}
private:
	int m_state;
	std::vector<Event> m_events;
};


class StateMachine
{
public:
	StateMachine(void) {}
	~StateMachine(void) {}
	State* addState(int id)
	{
		m_states.push_back(State(id));
		return &m_states.back();
	}
	void setState(int);
	void dispatchEvent(int);
private:
	std::vector<State> m_states;
};


}  // namespace
