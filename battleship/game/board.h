#ifndef __BATTLESHIP_BOARD_H
#define __BATTLESHIP_BOARD_H


#include <vector>


namespace board {

	
enum SHOT { MISS, HIT, SUNK };  // results

struct Pos
{
	short x,y;
	Pos(short x_val, short y_val)
	{
		x = x_val;
		y = y_val;
	}
	bool operator== (const Pos& pos) const
	{
		return (x == pos.x && y == pos.y) ? true : false;
	}
};

struct Shot
{
	short x,y;
	SHOT result;
};

struct ShipAnchor
{
	ShipAnchor(short x, short y, short size, bool horiz)
	: pos (x,y)
	{
		ship_size = size;
		horizontal = horiz;
	}
	Pos pos;
	unsigned short ship_size;
	bool horizontal;
};

struct ShipSegment
{
	Pos pos;
	bool active;
	ShipSegment(short x, short y):
		pos (x, y)
	{
		active = true;
	}
	bool operator== (const ShipSegment& segment) const
	{
		return (pos == segment.pos) ? true : false;
	}
};

struct Ship
{
	std::vector<ShipSegment> segments;
	bool operator== (const Ship& ship) const
	{
		return (segments == ship.segments) ? true : false;
	}
};

class SeaGrid
{
public:
	SeaGrid(short side, const std::vector<ShipAnchor>& anchors);
	SHOT ShootSquare(Pos& coords);
	std::vector<Ship> ships;
	unsigned int active_ships;
	std::vector<Shot> shots;
	short side;
};


}  // namespace


#endif // __BATTLESHIP_BOARD_H
