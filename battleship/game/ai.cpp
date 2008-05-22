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
			for (std::vector<int>::iterator it=squares.begin(); it != squares.end(); i++)
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
	std::vector<int>* targetP = NULL;
	for (std::vector< std::vector<int> >::iterator it=m_targets.begin(); it != m_targets.end(); it++)
	{
		std::vector<int>& t = *it;
		assert (0 == std::count(t.begin(), t.end(), index));
		std::vector<int> squares = neighbor_squares(index, m_sea_side);
		for (std::vector<int>::iterator it = squares.begin(); it != squares.end(); it++)
		{
			int& n = *it;
			if (0 != std::count(t.begin(), t.end(), n))
			{
				targetP = &t;
				break;
			}
		}
	}

	if (res == board::HIT)
	{
		if (targetP != NULL)
		{
			targetP->push_back(index);
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
		if (targetP != NULL)
		{
			m_targets.erase(*targetP);
			for (i in targetP)
			{
				for (n in neighbor_squares(i, m_sea_side))
				{
					if (n in m_shots)
						m_shots.remove(n);
				}
			}
		}
	}
}


std::vector<int> diagonal_squares(index, side)
{
	std::vector<int> res;
	length = m_side * m_side;
	pos = index - side + 1;  // upper-right
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

std::vector<int> neighbor_squares(index, side)
{
	return horizontal_neighbor_squares(index, side) + vertical_neighbor_squares(index, side)
}

std::vector<int> horizontal_neighbor_squares(index, side)
{
	res = []
	length = side ** 2
	pos = index - 1;  // left
	if index % side != 0 && pos >= 0 && pos < length:
		res.append(pos)
	pos = index + 1;  // right
	if pos % side != 0 && pos >= 0 && pos < length:
		res.append(pos)
	return res
}

void vertical_neighbor_squares(index, side)
{
	res = []
	length = side ** 2
	pos = index - side;  // up
	if pos >= 0 && pos < length:
		res.append(pos)
	pos = index + side;  // down
	if pos >= 0 && pos < length:
		res.append(pos)
	return res
}

//--------------

void setup_ships(sea_side, fleet_conf)
{
	/*
	typical_config = [
	(1, 4),  // one huge
	(2, 3),  // two bigs
	(3, 2),  // three mediums
	(4, 1)]  // four smalls
	*/
	ships = []
	sea = [' '] * (sea_side**2)
	for quantity, size in fleet_conf:
		for i in xrange(quantity):
			ships.append(randomly_place_ship(size, sea))
	return ships
}

void randomly_place_ship(size, sea)
{
	sea_side = int(math.sqrt(len(sea)))
	pos = generate_random_position(size, sea_side)
	while not is_squares_available(sea, pos):
		pos = generate_random_position(size, sea_side)
	occupy_squares(sea, pos)
	return pos
}

void generate_random_position(ship_size, sea_side)
{
	horizontal = random.choice((True, False))
	x = random.randrange(sea_side - (ship_size if horizontal else 0))
	y = random.randrange(sea_side - (0 if horizontal else ship_size))
	return (x, y, ship_size, horizontal)
}

void is_squares_available(sea, ship)
{
	sea_side = int(math.sqrt(len(sea)))
	x, y, ship_size, horizontal = ship
	index = y * sea_side + x
	orient = 1 if horizontal else sea_side
	for i in [index + i * orient for i in xrange(ship_size)]:
		if sea[i] != ' ':
			return False
	return True
}

void occupy_squares(sea, ship)
{
	sea_side = int(math.sqrt(len(sea)))
	x, y, ship_size, horizontal = ship
	index = y * sea_side + x
	orient = 1 if horizontal else sea_side
	pos = [index + i * orient for i in xrange(ship_size)]
	S = int(math.sqrt(len(sea)))
	for (i in pos)
	{
		assert sea[i] == ' '
		sea[i] = '#'
		// horizontal margin
		if i % S != 0 && i-1 >= 0 && i-1 < len(sea) && i-1 not in pos)
		{
			assert sea[i-1] != '#'
			sea[i-1] = '.';  // left
		}
		if (i+1) % S != 0 && i+1 >= 0 && i+1 < len(sea) && i+1 not in pos)
		{
			assert sea[i+1] != '#'
			sea[i+1] = '.';  // right
		}
		// vertical margin
		if i-S >= 0 && i-S < len(sea) && i-S not in pos)
		{
			assert sea[i-S] != '#'
			sea[i-S] = '.';  // up
		}
		if i+S >= 0 && i+S < len(sea) && i+S not in pos)
		{
			assert sea[i+S] != '#'
			sea[i+S] = '.';  // down
		}
		// diagonal margin
		if (i-S+1) % S != 0 && i-S+1 >= 0 && i-S+1 < len(sea))
		{
			assert sea[i-S+1] != '#'
			sea[i-S+1] = '.';  // upper-right
		}
		if i % S != 0 && i-S-1 >= 0 && i-S-1 < len(sea))
		{
			assert sea[i-S-1] != '#'
			sea[i-S-1] = '.';  // upper-left
		}
		if (i+S+1) % S != 0 && i+S+1 >= 0 && i+S+1 < len(sea))
		{
			assert sea[i+S+1] != '#'
			sea[i+S+1] = '.';  // lower-right
		}
		if i % S != 0 && i+S-1 >= 0 && i+S-1 < len(sea))
		{
			assert sea[i+S-1] != '#'
			sea[i+S-1] = '.';  // lower-left
		}
	}
}


}
