#ifndef __BATTLESHIP_AI_H
#define __BATTLESHIP_AI_H


#include "board.h"
#include "logic.h"


namespace ai {


std::vector<board::ShipAnchor> setup_ships(short sea_side, const std::vector<logic::FleetConf>& fleet_conf);


class ComputerPlayer
{
public:
	ComputerPlayer() {}
	ComputerPlayer(short sea_side, const std::vector<logic::FleetConf>& fleet_conf);
	board::Pos Shot();
	void Track(board::Pos shot, board::SHOT res);
private:
	short m_sea_side;
	std::vector<int> m_shots;  // all possible shots
	std::vector< std::vector<int> > m_targets;  // hit, but not yet sunk opponent ships
};


}  // namespace


#endif // __BATTLESHIP_AI_H
