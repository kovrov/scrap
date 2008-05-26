#include "logic.h"
#include "fsm.h"

#include <assert.h>
#include <map>


namespace logic {


struct PlayerState
{
	bool ready;
	PLAYER_HANDLE opponent;
	board::SHOT last_shot;
	board::SeaGrid* sea;
	PlayerState() // DELME
	{
		opponent = 0;
		ready = false;
		sea = NULL;
	}
	PlayerState(PLAYER_HANDLE opponent_handle)
	{
		opponent = opponent_handle;
		ready = false;
		sea = NULL;
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
	~GameContext()
	{
		for (std::map<PLAYER_HANDLE, PlayerState>::iterator it=players.begin(); it != players.end(); it++)
		{
			if (it->second.sea != NULL)
			{
				delete it->second.sea;
				it->second.sea = NULL;
			}
		}
	}
};

enum EVENTDATATYPE { SHIPS, POS };

struct EventData
{
	PLAYER_HANDLE player;
	EVENTDATATYPE type;
	void* data;
	EventData(PLAYER_HANDLE p, const std::vector<board::ShipAnchor>* ships)
	{
		player = p;
		type = SHIPS;
		data = const_cast<std::vector<board::ShipAnchor>*>(ships);
	}
	EventData(PLAYER_HANDLE p, const board::Pos* pos)
	{
		player = p;
		type = POS;
		data = const_cast<board::Pos*>(pos);
	}
};


// Rule defenitions and support

void restart_battle(GameContext* context)  // entry action
{
	for (std::map<PLAYER_HANDLE,PlayerState>::iterator it = context->players.begin();
		it != context->players.end();
		it++)
	{
		PlayerState& player = it->second;
		player.sea = NULL;
	}
	context->current = context->players.begin()->first;
}

bool does_all_players_set(GameContext* context)  // condition
{
	for (std::map<PLAYER_HANDLE,PlayerState>::iterator it = context->players.begin();
		it != context->players.end();
		it++)
	{
		PlayerState& player = it->second;
		if (!player.ready)
			return false;
	}
	return true;
}

bool is_shot_missed(GameContext* context)  // condition
{
	PlayerState& current_player = context->players[context->current];
	return current_player.last_shot == board::MISS;
}

bool does_opponent_has_no_ships(GameContext* context)  // condition
{
	PlayerState& current_player = context->players[context->current];
	board::SeaGrid* target_sea = context->players[current_player.opponent].sea;
	return target_sea->active_ships == 0;
}

void pass_turn(GameContext* context)  // action
{
	context->current = context->players[context->current].opponent;
}

bool setup_ships(GameContext* context, const EventData& input)  // event input
{
	assert (input.type == SHIPS);
	const std::vector<board::ShipAnchor>& ships = *reinterpret_cast<std::vector<board::ShipAnchor>*>(input.data);
	if (context->players[input.player].sea != NULL)
		delete context->players[input.player].sea;
	context->players[input.player].sea = new board::SeaGrid(10, ships);
	context->players[input.player].ready = true;
	return true;
}

bool player_shoot(GameContext* context, const EventData& input)  // event input
{
	assert (input.player == context->current);
	assert (input.type == POS);
	board::Pos& pos = *reinterpret_cast<board::Pos*>(input.data);
	PlayerState& current_player = context->players[context->current];
	board::SeaGrid* target_sea = context->players[current_player.opponent].sea;
	current_player.last_shot = target_sea->ShootSquare(pos);
	return true;
}

Game::Game(PLAYER_HANDLE player1, PLAYER_HANDLE player2)
{
	m_config.push_back(FleetConf(1, 4));  // one battleship
	m_config.push_back(FleetConf(2, 3));  // two cruisers
	m_config.push_back(FleetConf(3, 2));  // three destroyers
	m_config.push_back(FleetConf(4, 1));  // four boats
	m_context = new GameContext(player1, player2);
	std::map<int, fsm::State<GameContext, EventData> > states;

	states[BATTLE_STARTED] = fsm::State<GameContext,EventData>();
	states[BATTLE_STARTED].onEnter = restart_battle;
	states[BATTLE_STARTED].events[SETUP] = fsm::Event<GameContext,EventData>();
	states[BATTLE_STARTED].events[SETUP].input = setup_ships;
		fsm::Transition<GameContext,EventData> tr;
		tr.condition = does_all_players_set;
		tr.state = PLAYER_TURN;
	states[BATTLE_STARTED].events[SETUP].transitions.push_back(tr);

	states[PLAYER_TURN] = fsm::State<GameContext,EventData>();
	states[PLAYER_TURN].events[SHOOT] = fsm::Event<GameContext,EventData>();
	states[PLAYER_TURN].events[SHOOT].input = player_shoot;
		fsm::Transition<GameContext,EventData> player_turn_tr;
		player_turn_tr.state = PLAYER_TURN;
		player_turn_tr.condition = is_shot_missed;
		player_turn_tr.action = pass_turn;
	states[PLAYER_TURN].events[SHOOT].transitions.push_back(player_turn_tr);
		fsm::Transition<GameContext,EventData> battle_ended_tr;
		battle_ended_tr.state = BATTLE_ENDED;
		battle_ended_tr.condition = does_opponent_has_no_ships;
	states[PLAYER_TURN].events[SHOOT].transitions.push_back(battle_ended_tr);

	states[BATTLE_ENDED] = fsm::State<GameContext,EventData>();
	states[BATTLE_ENDED].events[RESTART] = fsm::Event<GameContext,EventData>();
	fsm::Transition<GameContext,EventData> battle_started_tr;
	battle_started_tr.state = BATTLE_STARTED;
	states[BATTLE_ENDED].events[RESTART].transitions.push_back(battle_started_tr);

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
	EventData data(player, &ships);  // (player, ships)
	m_fsm->Dispatch(SETUP, data);
}

board::SHOT Game::Shoot(PLAYER_HANDLE player, const board::Pos& shot)
{
	assert (m_context->current == player);
	EventData data(player, &shot);
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
