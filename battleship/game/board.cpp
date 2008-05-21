#include "board.h"

#include <vector>
#include <algorithm>
#include <memory>
#include <assert.h>


namespace board {


SeaGrid::SeaGrid(short side_len, const std::vector<ShipAnchor>& anchors)
{
	side = side_len;
	short grid_len = side*side;
	std::vector<char> grid(grid_len, ' ');

	for (std::vector<ShipAnchor>::const_iterator it=anchors.begin(); it != anchors.end(); it++)
	{
		const ShipAnchor& anchor = *it;
		int index = anchor.pos.y * side + anchor.pos.x;
		int orient = anchor.horizontal ? 1 : side;
		std::vector<int> indices;
		for (int i=0; i < anchor.ship_size; i++)
		{
			indices.push_back(index + i * orient);
		}

		Ship ship;
		for (std::vector<int>::iterator it=indices.begin(); it != indices.end(); it++)
		{
			int& i = *it;
			assert (grid[i] == ' ');
			grid[i] = '#';
			ship.segments.push_back(ShipSegment(i % side, i / side));
			// horizontal margin
			int pos = i - 1;  // left
			if (i % side != 0 && pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			pos = i + 1;  // right
			if (pos % side != 0 && pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			// vertical margin
			pos = i - side;  // up
			if (pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			pos = i + side;  // down
			if (pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			// diagonal margins
			pos = i - side + 1;  // upper-right
			if (pos % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
			pos = i - side - 1;  // upper-left
			if (i % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
			pos = i + side + 1;  // lower-right
			if (pos % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
			pos = i + side - 1;  // lower-left
			if (i % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
		}
		ships.push_back(ship);
		active_ships.push_back(ship);
	}
}


bool is_active(const ShipSegment& s)
{
	return s.active;
}


SHOT SeaGrid::ShootSquare(Pos& coords)
{
	if (0 != std::count(shots.begin(), shots.end(), coords))
		throw std::exception("can't shoot twice");
	shots.push_back(coords);
	for (std::vector<Ship>::iterator it=ships.begin(); it != ships.end(); it++)
	{
		Ship& ship = *it;
		for (std::vector<ShipSegment>::iterator it=ship.segments.begin(); it != ship.segments.end(); it++)
		{
			ShipSegment& segment = *it;
			if (segment.pos == coords)
			{
				assert (segment.active);
				segment.active = false;
				if (std::count_if(ship.segments.begin(), ship.segments.end(), is_active))
				{
					return HIT;
				}
				else
				{
					active_ships.erase(std::find(active_ships.begin(), active_ships.end(), ship));
					return SUNK;
				}
			}
		}
	}
	return MISS;
}


}; // namespace
