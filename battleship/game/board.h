#pragma once
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

struct ShipAnchor
{
	Pos pos;
	short ship_size;
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
};

struct Ship
{
	std::vector<ShipSegment> segments;
	bool operator== (const Ship& ship) const
	{
		return (this == &ship) ? true : false;
	}
};

class SeaGrid
{
public:
	SeaGrid(short side, const std::vector<ShipAnchor>& anchors);
	SHOT ShootSquare(Pos& coords);
	std::vector<Ship> ships;
	std::vector<Ship> active_ships;
	std::vector<Pos> shots;
	short side;
};


}; // namespace
