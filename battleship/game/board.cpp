#include "board.h"

#include <vector>
#include <algorithm>
#include <assert.h>


namespace board {


SeaGrid::SeaGrid(short side_len, const std::vector<ShipAnchor>& anchors)
{
	active_ships = 0;
	side = side_len;
	short grid_len = side*side;
	std::vector<char> grid(grid_len, ' ');

	for (std::vector<ShipAnchor>::const_iterator i=anchors.begin(); i != anchors.end(); i++)
	{
		const ShipAnchor& anchor = *i;
		int start_index = anchor.pos.y * side + anchor.pos.x;
		int orient = anchor.horizontal ? 1 : side;
		std::vector<int> indices;
		for (int j=0; j < anchor.ship_size; j++)
		{
			indices.push_back(start_index + j * orient);
		}

		Ship ship;
		for (std::vector<int>::iterator j=indices.begin(); j != indices.end(); j++)
		{
			int index = *j;
			assert (grid[index] == ' ');
			grid[index] = '#';
			ship.segments.push_back(ShipSegment(index % side, index / side));
			// horizontal margin
			int pos = index - 1;  // left
			if (index % side != 0 && pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			pos = index + 1;  // right
			if (pos % side != 0 && pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			// vertical margin
			pos = index - side;  // up
			if (pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			pos = index + side;  // down
			if (pos >= 0 && pos < grid_len)
			{
				if (0 == std::count(indices.begin(), indices.end(), pos))
				{
					assert (grid[pos] != '#');
					grid[pos] = '.';
				}
			}
			// diagonal margins
			pos = index - side + 1;  // upper-right
			if (pos % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
			pos = index - side - 1;  // upper-left
			if (index % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
			pos = index + side + 1;  // lower-right
			if (pos % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
			pos = index + side - 1;  // lower-left
			if (index % side != 0 && pos >= 0 && pos < grid_len)
			{
				assert (grid[pos] != '#');
				grid[pos] = '.';
			}
		}
		ships.push_back(ship);
		active_ships++;
	}
}


bool is_active(const ShipSegment& s)
{
	return s.active;
}


SHOT SeaGrid::ShootSquare(Pos& coords)
{
	if (0 != std::count(shots.begin(), shots.end(), coords))
		throw std::exception();  // can't shoot twice
	shots.push_back(coords);
	for (std::vector<Ship>::iterator i=ships.begin(); i != ships.end(); i++)
	{
		Ship& ship = *i;
		for (std::vector<ShipSegment>::iterator j=ship.segments.begin(); j != ship.segments.end(); j++)
		{
			ShipSegment& segment = *j;
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
					active_ships--;
					return SUNK;
				}
			}
		}
	}
	return MISS;
}


}  // namespace
