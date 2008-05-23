#include "logic.h"
#include "fsm.h"

//#include <stdlib.h>
#include <assert.h>
#include <map>


namespace logic {


struct PlayerState
{
	bool ready;
	PLAYER_HANDLE opponent;
	board::SHOT last_shot;
	board::SeaGrid* sea;
	PlayerState()
	{
		opponent = 0;
		ready = false;
	}
	PlayerState(PLAYER_HANDLE opponent_handle)
	{
		opponent = opponent_handle;
		ready = false;
	}
};

struct GameContext
{
	PLAYER_HANDLE current;
	std::map<PLAYER_HANDLE, PlayerState> players;
	GameContext(PLAYER_HANDLE player1, PLAYER_HANDLE player2)
	{
		players[player1] = PlayerState(player2);
		players[player2] = PlayerState(player1);
	}
};

struct EventData
{
};


// Rule defenitions and support

void restart_battle(GameContext* context)  // entry action
{
	for (player in context['players'].itervalues())
		player['sea'] = None;
	context['current'] = context['players'].keys()[0];
}

void does_all_players_set(GameContext* context)  // condition
{
	for (player in context['players'].itervalues())
	{
		if (not player['ready'])
			return false;
	return true;
}

void is_shot_missed(GameContext* context)  // condition
{
	current_player = context['players'][context['current']];
	return current_player['last_shot'] == 'miss';
}

void does_opponent_has_no_ships(GameContext* context)  // condition
{
	current_player = context['players'][context['current']];
	target_sea = context['players'][current_player['opponent']]['sea'];
	if (len(target_sea.active_ships) == 0)
		return true;
	else
		return false;
}

void pass_turn(GameContext* context)  // action
{
	current_player = context['players'][context['current']];
	context['current'] = current_player['opponent'];
}

void setup_ships(GameContext* context, EventData* input)  // event input
{
	player, ships = input;
	context['players'][player]['sea'] = board.SeaGrid(SEA_SIDE, ships);
	context['players'][player]['ready'] = true;
}

void player_shoot(GameContext* context, EventData* input)  // event input
{
	player, pos = input;
	current_player = context['players'][context['current']];
	target_sea = context['players'][current_player['opponent']]['sea'];
	current_player['last_shot'] = target_sea.shoot_square(pos);
}

Game::Game(PLAYER_HANDLE player1, PLAYER_HANDLE player2)
{
	m_config.push_back(FleetConf(1, 4));  // one battleship
	m_config.push_back(FleetConf(2, 3));  // two cruisers
	m_config.push_back(FleetConf(3, 2));  // three destroyers
	m_config.push_back(FleetConf(4, 1));  // four boats
	m_context = new GameContext(player1, player2);
	std::map<int, fsm::State<GameContext, EventData> > states;

	states[BATTLE_STARTED] = fsm::State<GameContext, EventData>();
	states[BATTLE_STARTED].onEnter = restart_battle;
	states[BATTLE_STARTED].events[SETUP] = fsm::Event<GameContext, EventData>;
/*		events = {
			SETUP: fsm.Event(
				input = setup_ships,
				transitions = (
					fsm.Transition(condition=does_all_players_set, state=PLAYER_TURN),))}),
	PLAYER_TURN: fsm.State(
		events = {
			SHOOT: fsm.Event(
				input = player_shoot,
				transitions = (
					fsm.Transition(condition=is_shot_missed, state=PLAYER_TURN, action=pass_turn),
					fsm.Transition(condition=does_opponent_has_no_ships, state=BATTLE_ENDED)))}),
	BATTLE_ENDED: fsm.State(
		events = {
			RESTART: fsm.Event(
				transitions = (
					fsm.Transition(state=BATTLE_STARTED),))})}
*/
	m_fsm = new fsm::Transducer<GameContext, EventData>(states, BATTLE_STARTED, m_context);
}
Game::~Game()
{
	delete m_context;
	delete m_fsm;
}

STATE Game::GetState()
{
	return (STATE)m_fsm->GetState();
}

void Game::Setup(PLAYER_HANDLE player, const std::vector<board::ShipAnchor>& ships)
{
	EventData data;  // (player, ships)
	m_fsm->Dispatch(SETUP, data);
}

board::SHOT Game::Shoot(PLAYER_HANDLE player, const board::Pos& shot)
{
	assert (m_context->current == player);
	EventData data;  // (player, shot)
	m_fsm->Dispatch(SHOOT, data);
	return m_context->players[player].last_shot;
}

PLAYER_HANDLE Game::GetCurrentPlayer()
{
	return m_context->current;
}

const std::vector<board::Ship> Game::GetOpponentShips(PLAYER_HANDLE player)
{
	PLAYER_HANDLE opponent = m_context->players[player].opponent;
	return m_context->players[opponent].sea->ships;
}

const std::vector<board::Pos> Game::GetPlayerShots(PLAYER_HANDLE player)
{
	PLAYER_HANDLE opponent = m_context->players[player].opponent;
	return m_context->players[opponent].sea->shots;
}


}  // namespace
