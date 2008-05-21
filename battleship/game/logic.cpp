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

Game::Game(PLAYER_HANDLE player1, PLAYER_HANDLE player2)
{
	m_config.push_back(FleetConf(1, 4));  // one battleship
	m_config.push_back(FleetConf(2, 3));  // two cruisers
	m_config.push_back(FleetConf(3, 2));  // three destroyers
	m_config.push_back(FleetConf(4, 1));  // four boats
	m_context = new GameContext(player1, player2);
	std::map<int, fsm::State<GameContext, EventData> > states;
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
