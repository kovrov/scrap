#ifndef __BATTLESHIP_LOGIC_H
#define __BATTLESHIP_LOGIC_H


#include <vector>
#include "board.h"


// pimpl (forward declarations) of fsm stuff
namespace fsm { template <typename CTX, typename DATA> class Transducer; }


namespace logic {
/*
This module is describing high-level control flow of the game, that is
essentially logic behind "game rules".
This is typical "controller" in MVC terminology.
*/

enum STATE { BATTLE_STARTED, PLAYER_TURN, BATTLE_ENDED };
enum EVENT { SETUP, SHOOT, RESTART };

typedef int PLAYER_HANDLE;

struct FleetConf
{
	unsigned short size, quantity;
	FleetConf(short s, short q) { size = s, quantity = q; }
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
	std::vector<board::Ship> GetOpponentShips(PLAYER_HANDLE player);
	std::vector<board::Ship> GetPlayerShips(PLAYER_HANDLE player);
	std::vector<board::Shot> GetPlayerShots(PLAYER_HANDLE player);
	std::vector<FleetConf> GetConfig() { return m_config; }
private:
	std::vector<FleetConf> m_config;
	GameContext* m_context;
	fsm::Transducer<GameContext,EventData>* m_fsm;
};


}  // namespace


#endif // __BATTLESHIP_LOGIC_H
