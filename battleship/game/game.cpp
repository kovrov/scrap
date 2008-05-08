#include "game.h"
#include "fsm.h"

#include <stdlib.h>
#include <assert.h>


namespace game {


TurnBased::TurnBased(void):
m_sea(10)  // m_sea could be constructed in initialization lists only
{
	// temproray hardcoded config
	m_conf.len = 4;
	m_conf.ptr = new Config::Entity[m_conf.len];
	m_conf.ptr[0].quantity = 1; m_conf.ptr[0].size = 4;  // one huge
	m_conf.ptr[1].quantity = 2; m_conf.ptr[1].size = 3;  // two bigs
	m_conf.ptr[2].quantity = 3; m_conf.ptr[2].size = 2;  // three mediums
	m_conf.ptr[3].quantity = 4; m_conf.ptr[3].size = 1;  // four smalls
}


TurnBased::~TurnBased(void)
{
	delete[] m_conf.ptr;
}

enum 
{
	BATTLE_STARTED,
	BATTLE_ENDED,
	PLAYER_SETUP,
	NEW_GAME,
	PLAYER_TURN,
	PLAYER_SHOOT
};


void setupTurnBased()
{
	TurnBased game;
	fsm::StateMachine state_machine;

	fsm::State* battle_started = state_machine.addState(BATTLE_STARTED);
	fsm::State* player_turn    = state_machine.addState(PLAYER_TURN);
	fsm::State* battle_ended   = state_machine.addState(BATTLE_ENDED);

	fsm::Event* player_setup = battle_started->addEvent(PLAYER_SETUP, NULL, (TurnBased*)NULL);
	player_setup->addTransition(/*isAllPlayersSet*/NULL, &game, player_turn);

	fsm::Event* player_shoot = player_turn->addEvent(PLAYER_SHOOT, &game.isShotValid);
	player_shoot->addTransition(&game.isShotMissed, player_turn, &game.passTurn);
	player_shoot->addTransition(&game.isOpponentHasNoShips, battle_ended);

	fsm::Event* new_game = battle_ended->addEvent(NEW_GAME, NULL);
	new_game->addTransition(NULL, battle_started);
}


}  // namespace
