#pragma once
#pragma warning (disable: 4290) // exception specification ignored

#include <vector>
#include <map>


namespace fsm {


// Private implementation (?)
template <typename CTX, typename DATA> struct State;
template <typename CTX, typename DATA> struct Event;
template <typename CTX, typename DATA> struct Transition;


// public API
template <typename CTX, typename DATA>
struct State
{
	void (*onEnter)(CTX*); // CALLBACK
	void (*onExit)(CTX*);  // CALLBACK
	std::map<int, Event<CTX,DATA> > events;
};

template <typename CTX, typename DATA>
struct Event
{
	bool (*input)(CTX*, DATA&);  // INPUT_VALIDATOR
	std::vector<Transition<CTX,DATA> > transitions;
};

template <typename CTX, typename DATA>
struct Transition
{
	int state;
	bool (*condition)(CTX*);  // ACTION_CALLBACK
	void (*action)(CTX*);  // CALLBACK
};


class InvalidEventException: public std::exception
{
};


template <typename CTX, typename DATA>
class Transducer
{
public:
	Transducer(const std::map<int, State<CTX,DATA> >& states, int initial_state, CTX* context);
	void Dispatch(int event_id, DATA& input) throw (InvalidEventException);
	int GetState();
	int SetState(int state);
private:
	std::map<int, State<CTX,DATA> > m_states;
	int m_state;
	CTX* p_context;
};


}  // namespace
