#pragma once
#include <vector>
#include "board.h"
#include "fsm.h"


namespace logic {
/*
This module is describing high-level control flow of the game, that is
essentially logic behind "game rules".
This is typical "controller" in MVC terminology.
*/

enum STATE { BATTLE_STARTED, PLAYER_TURN, BATTLE_ENDED };
enum EVENT { SETUP, SHOOT, RESTART };

#define SEA_SIDE 10

typedef int PLAYER_HANDLE;

struct FleetConf
{
	unsigned short size, quantity;
	FleetConf(short s, short q){ size = s, quantity = q;}
};

struct GameContext;
struct EventData;

class Game
{
public:
	Game(PLAYER_HANDLE player1, PLAYER_HANDLE player2);
	~Game();
	STATE GetState();
	void Setup(PLAYER_HANDLE player, const std::vector<board::ShipAnchor>& ships);
	board::SHOT Shoot(PLAYER_HANDLE player, const board::Pos& shot);
	PLAYER_HANDLE GetCurrentPlayer();
	const std::vector<board::Ship> GetOpponentShips(PLAYER_HANDLE player);
	const std::vector<board::Pos> GetPlayerShots(PLAYER_HANDLE player);
	const std::vector<FleetConf> GetConfig();
private:
	std::vector<FleetConf> m_config;
	GameContext* m_context;
	fsm::Transducer<GameContext,EventData>* m_fsm;
};


}  // namespace
