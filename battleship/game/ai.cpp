#include "ai.h"

#include <algorithm>
#include <functional>
#include <exception>
#include <assert.h>
#include <stdlib.h>


namespace ai {


typedef std::vector<int> (*NEIGHBOR_FN)(size_t index, short side);
std::vector<int> neighbor_squares(size_t index, short side);
std::vector<int> horizontal_neighbor_squares(size_t index, short side);
std::vector<int> vertical_neighbor_squares(size_t index, short side);
std::vector<int> diagonal_squares(size_t index, short side);

ComputerPlayer::ComputerPlayer(short sea_side, std::vector<logic::FleetConf> fleet_conf)
{
	m_sea_side = sea_side;
	m_shots.resize(m_sea_side * m_sea_side);
	for (size_t i=0; i < m_shots.size(); i++) m_shots[i] = i;  // range(m_shots.size())
}


board::Pos ComputerPlayer::Shot()
{
	assert (m_shots.size() > 0);
	for (std::vector< std::vector<int> >::iterator it=m_targets.begin(); it != m_targets.end(); it++)
	{
		NEIGHBOR_FN get_squares = NULL;
		std::vector<int>& target = *it;
		if (target.size() < 2)
		{
			get_squares = neighbor_squares;
		}
		else
		{
			unsigned span = abs(target[0] - target[1]);
			if (span == 1)  // horisontal target
				get_squares = horizontal_neighbor_squares;
			else if (span == m_sea_side) // vertical target
				get_squares = vertical_neighbor_squares;
			else
				throw std::exception("this is impossible!");
		}

		for (std::vector<int>::iterator it=target.begin(); it != target.end(); it++)
		{
			int i = *it;
			std::vector<int> squares = get_squares(i, m_sea_side);
			for (std::vector<int>::iterator it=squares.begin(); it != squares.end(); it++)
			{
				int& shot = *it;
				if (0 < std::count(m_shots.begin(), m_shots.end(), shot))
				{
					m_shots.erase(std::find(m_shots.begin(), m_shots.end(), shot));
					return board::Pos(shot % m_sea_side, shot / m_sea_side);
				}
			}
		}
		throw std::exception("this is impossible!");
	}
	std::vector<int>::iterator shot_it = m_shots.begin() + (rand() % m_shots.size()); // random.choice(m_shots);
	int shot = *shot_it;
	m_shots.erase(shot_it);
	return board::Pos(shot % m_sea_side, shot / m_sea_side);
}




void ComputerPlayer::Track(board::Pos shot, board::SHOT res)
{
	if (res == board::MISS)
		return;
	size_t index = shot.y * m_sea_side + shot.x;
	// clear diagonal shots
	{std::vector<int> squares = diagonal_squares(index, m_sea_side);
	for (std::vector<int>::iterator it=squares.begin(); it != squares.end(); it++)
	{
		std::vector<int>::iterator find_it = std::find(m_shots.begin(), m_shots.end(), *it);
		if (find_it != m_shots.end())
			m_shots.erase(find_it);
	}}
	// find the target if its in not a new one
	std::vector< std::vector<int> >::iterator target_it = m_targets.end();
	for (std::vector< std::vector<int> >::iterator it=m_targets.begin(); it != m_targets.end(); it++)
	{
		std::vector<int>& t = *it;
		assert (0 == std::count(t.begin(), t.end(), index));
		std::vector<int> squares = neighbor_squares(index, m_sea_side);
		for (std::vector<int>::iterator square_it = squares.begin(); square_it != squares.end(); square_it++)
		{
			if (0 != std::count(t.begin(), t.end(), *square_it))
			{
				target_it = it;
				break;
			}
		}
	}

	if (res == board::HIT)
	{
		if (target_it != m_targets.end())
		{
			(*target_it).push_back(index);
			return;
		}
		m_targets.push_back(std::vector<int>(1, index));
	}

	if (res == board::SUNK)
	{
		std::vector<int> squares = neighbor_squares(index, m_sea_side);
		for (std::vector<int>::iterator it = squares.begin(); it != squares.end(); it++)
		{
			std::vector<int>::iterator find_it = std::find(m_shots.begin(), m_shots.end(), *it);
			if (find_it != m_shots.end())
				m_shots.erase(find_it);
		}
		if (target_it != m_targets.end())
		{
			std::vector<int> target = *target_it;
			m_targets.erase(target_it);
			for (std::vector<int>::iterator it = target.begin(); it != target.end(); it++)
			{
				std::vector<int> squares = neighbor_squares(*it, m_sea_side);
				for (std::vector<int>::iterator it=squares.begin(); it != squares.end(); it++)
				{
					std::vector<int>::iterator shot_it = std::find(m_shots.begin(), m_shots.end(), *it);
					if (shot_it != m_shots.end())
					{
						m_shots.erase(shot_it);
						return;
					}
				}
			}
		}
	}
}


std::vector<int> diagonal_squares(size_t index, short side)
{
	std::vector<int> res;
	unsigned length = side * side;
	size_t pos = index - side + 1;  // upper-right
	if (pos % side != 0 && pos >= 0 && pos < length)
	{
		res.push_back(pos);
	}
	pos = index - side - 1;  // upper-left
	if (index % side != 0 && pos >= 0 && pos < length)
	{
		res.push_back(pos);
	}
	pos = index + side + 1;  // lower-right
	if (pos % side != 0 && pos >= 0 && pos < length)
	{
		res.push_back(pos);
	}
	pos = index + side - 1;  // lower-left
	if (index % side != 0 && pos >= 0 && pos < length)
	{
		res.push_back(pos);
	}
	return res;
}

std::vector<int> neighbor_squares(size_t index, short side)
{
	std::vector<int> vec1 = horizontal_neighbor_squares(index, side);
	std::vector<int> vec2 = vertical_neighbor_squares(index, side);
	std::copy(vec2.begin(), vec2.end(), std::back_inserter(vec1));
	return vec1;
}

std::vector<int> horizontal_neighbor_squares(size_t index, short side)
{
	std::vector<int> res;
	size_t length = side * side;
	size_t pos = index - 1;  // left
	if (index % side != 0 && pos >= 0 && pos < length)
		res.push_back(pos);
	pos = index + 1;  // right
	if (pos % side != 0 && pos >= 0 && pos < length)
		res.push_back(pos);
	return res;
}

std::vector<int> vertical_neighbor_squares(size_t index, short side)
{
	std::vector<int> res;
	size_t length = side * side;
	size_t pos = index - side;  // up
	if (pos >= 0 && pos < length)
		res.push_back(pos);
	pos = index + side;  // down
	if (pos >= 0 && pos < length)
		res.push_back(pos);
	return res;
}

//--------------

board::ShipAnchor GenerateRandPos(short ship_size, short sea_side)
{
	bool horizontal = rand() % 2 == 1;  // random.choice((true, false));
	short x = rand() % (sea_side - (horizontal ? ship_size : 0));
	short y = rand() % (sea_side - (horizontal ? 0 : ship_size));
	return board::ShipAnchor(x, y, ship_size, horizontal);
}

bool IsSquaresAvailable(std::vector<char>& sea, const board::ShipAnchor& ship, unsigned sea_side)
{
	size_t index = ship.pos.y * sea_side + ship.pos.x;
	short orient = ship.horizontal ? 1 : sea_side;
	for (size_t i=0; i < ship.ship_size; i++)
	{
		if (sea[index + i * orient] != ' ')
			return false;
	}
	return true;
}

void OccupySquares(std::vector<char>& sea, const board::ShipAnchor& ship, int sea_side)
{
	int grid_len = sea.size();
	size_t index = ship.pos.y * sea_side + ship.pos.x;
	unsigned orient = ship.horizontal ? 1 : sea_side;

	std::vector<size_t> segments(ship.ship_size);
	for (size_t i=0; i < ship.ship_size; i++)
		segments[i] = index + i * orient;

	for (std::vector<size_t>::iterator it=segments.begin(); it != segments.end(); it++)
	{
		size_t& i = *it;
		assert (sea[i] == ' ');
		sea[i] = '#';
		// horizontal margin
		int pos = i - 1;  // left
		if (i % sea_side != 0 && pos >= 0 && pos < grid_len)
		{
			if (0 == std::count(segments.begin(), segments.end(), pos))
			{
				assert (sea[pos] != '#');
				sea[pos] = '.';
			}
		}
		pos = i + 1;  // right
		if (pos % sea_side != 0 && pos >= 0 && pos < grid_len)
		{
			if (0 == std::count(segments.begin(), segments.end(), pos))
			{
				assert (sea[pos] != '#');
				sea[pos] = '.';
			}
		}
		// vertical margin
		pos = i - sea_side;  // up
		if (pos >= 0 && pos < grid_len)
		{
			if (0 == std::count(segments.begin(), segments.end(), pos))
			{
				assert (sea[pos] != '#');
				sea[pos] = '.';
			}
		}
		pos = i + sea_side;  // down
		if (pos >= 0 && pos < grid_len)
		{
			if (0 == std::count(segments.begin(), segments.end(), pos))
			{
				assert (sea[pos] != '#');
				sea[pos] = '.';
			}
		}
		// diagonal margins
		pos = i - sea_side + 1;  // upper-right
		if (pos % sea_side != 0 && pos >= 0 && pos < grid_len)
		{
			assert (sea[pos] != '#');
			sea[pos] = '.';
		}
		pos = i - sea_side - 1;  // upper-left
		if (i % sea_side != 0 && pos >= 0 && pos < grid_len)
		{
			assert (sea[pos] != '#');
			sea[pos] = '.';
		}
		pos = i + sea_side + 1;  // lower-right
		if (pos % sea_side != 0 && pos >= 0 && pos < grid_len)
		{
			assert (sea[pos] != '#');
			sea[pos] = '.';
		}
		pos = i + sea_side - 1;  // lower-left
		if (i % sea_side != 0 && pos >= 0 && pos < grid_len)
		{
			assert (sea[pos] != '#');
			sea[pos] = '.';
		}
	}
}


board::ShipAnchor RandomlyPlaceShip(short size, std::vector<char>& sea, short sea_side)
{
	board::ShipAnchor pos = GenerateRandPos(size, sea_side);
	while (!IsSquaresAvailable(sea, pos, sea_side))
		pos = GenerateRandPos(size, sea_side);
	OccupySquares(sea, pos, sea_side);
	return pos;
}

std::vector<board::ShipAnchor> setup_ships(short sea_side, std::vector<logic::FleetConf> fleet_conf)
{
	std::vector<board::ShipAnchor> ships;
	std::vector<char> sea(sea_side * sea_side, ' ');
	for (std::vector<logic::FleetConf>::iterator it=fleet_conf.begin(); it != fleet_conf.end(); it++)
	{
		for (size_t i=0; i < (*it).quantity; i++)
			ships.push_back(RandomlyPlaceShip((*it).size, sea, sea_side));
	}
	return ships;
}


}
