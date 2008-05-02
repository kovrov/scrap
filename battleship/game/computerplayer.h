#pragma once

#include "seagrid.h"
#include "game.h"

class ComputerPlayer
{
public:
	ComputerPlayer(void);
	~ComputerPlayer(void);
	void PlaceShips(SeaGrid* sea, const Config& config);
private:
};
