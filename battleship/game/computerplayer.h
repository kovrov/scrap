#pragma once

#include "seagrid.h"
#include "game.h"

class ComputerPlayer
{
public:
	ComputerPlayer();
	~ComputerPlayer();
	void PlaceShips(SeaGrid* sea, const Config& config);
	void Shoot();
private:
	bool* m_shotsTable;
};
