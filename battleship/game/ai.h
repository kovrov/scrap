#pragma once

#include "board.h"
#include "logic.h"

namespace ai {


class ComputerPlayer
{
	ComputerPlayer(short sea_side, std::vector<logic::FleetConf> fleet_conf);
	void Shot();
	void Track(board::Pos shot, board::SHOT res);
private:
	short m_sea_side;
	std::vector<int> m_shots;  // all possible shots
	std::vector< std::vector<int> > m_targets;  // hit, but not yet sunk opponent ships
};



}
