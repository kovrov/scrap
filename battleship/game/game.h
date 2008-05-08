#pragma once
#include "seagrid.h"
#include "config.h"

namespace game {


class TurnBased
{
public:
	TurnBased(void);
	~TurnBased(void);

	bool isShotValid();
	bool isShotMissed();
	bool passTurn();
	bool isOpponentHasNoShips();
	bool isAllPlayersSet();

private:
	Config m_conf;
	SeaGrid m_sea;
};


}  // namespace
