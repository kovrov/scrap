#include "ai.h"

namespace ai {


ComputerPlayer::ComputerPlayer(short sea_side, std::vector<logic::FleetConf> fleet_conf)
{
	m_sea_side = sea_side;
	m_shots.resize(m_sea_side * m_sea_side);
	for (size_t i=0; i < m_shots.size(); i++) m_shots[i] = i;  // range(m_shots.size())
}


void ComputerPlayer::Shot()
{
	assert (m_shots.size() > 0);
	for (std::vector< std::vector<int> >::iterator it=m_targets.begin(); it != m_targets.end(); it++)
	{
		std::vector<int>& target = *it;
		if (target.size() < 2)
		{
			get_squares = neighbor_squares;
		}
		else
		{
			span = abs(target[0] - target[1]);
			if (span == 1)  // horisontal target
				get_squares = horizontal_neighbor_squares;
			else if (span == m_sea_side) // vertical target
				get_squares = vertical_neighbor_squares;
			else
				throw std::exception("this is impossible!");
		}

		for (i in target)
		{
			for (shot in get_squares(i, m_sea_side))
			{
				if (shot in m_shots)
				{
					m_shots.remove(shot);
					return (shot % 10, shot / 10);
				}
			}
		}
		throw std::exception("this is impossible!");
	}
	shot = random.choice(m_shots);
	m_shots.remove(shot);
	return board::Pos(shot % 10, shot / 10);
}



void ComputerPlayer::Track(board::Pos shot, board::SHOT res)
{
	if (res == board::SHOT::MISS)
		return;
	index = shot.y * m_sea_side + shot.x;
	// clear diagonal shots
	for (i in diagonal_squares(index, m_sea_side))
	{
		if (i in m_shots)
			m_shots.remove(i);
	}
	// find the target if its in not a new one
	target = None
	for (t in m_targets)
	{
		assert (index not in t);
		for (n in neighbor_squares(index, m_sea_side))
		{
			if (n in t)
			{
				target = t;
				break;
			}
		}
	}
	if (res == 'hit')
	{
		if (target is not None)
		{
			target.append(index);
			return;
		}
		m_targets.append([index,]);
	}
	if (res == 'sunk')
	{
		for (n in neighbor_squares(index, m_sea_side))
		{
			if n in m_shots:
				m_shots.remove(n);
		}
		if (target is not None)
		{
			m_targets.remove(target);
			for (i in target)
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


void diagonal_squares(index, side)
{
	res = []
	length = side ** 2
	pos = index - side + 1;  // upper-right
	if (pos % side != 0 && pos >= 0 && pos < length)
	{
		res.append(pos)
	}
	pos = index - side - 1;  // upper-left
	if (index % side != 0 && pos >= 0 && pos < length)
	{
		res.append(pos)
	}
	pos = index + side + 1;  // lower-right
	if (pos % side != 0 && pos >= 0 && pos < length)
	{
		res.append(pos)
	}
	pos = index + side - 1;  // lower-left
	if (index % side != 0 && pos >= 0 && pos < length)
	{
		res.append(pos)
	}
	return res
}

void neighbor_squares(index, side):
	return horizontal_neighbor_squares(index, side) + vertical_neighbor_squares(index, side)

void horizontal_neighbor_squares(index, side):
	res = []
	length = side ** 2
	pos = index - 1;  // left
	if index % side != 0 && pos >= 0 && pos < length:
		res.append(pos)
	pos = index + 1;  // right
	if pos % side != 0 && pos >= 0 && pos < length:
		res.append(pos)
	return res

void vertical_neighbor_squares(index, side):
	res = []
	length = side ** 2
	pos = index - side;  // up
	if pos >= 0 && pos < length:
		res.append(pos)
	pos = index + side;  // down
	if pos >= 0 && pos < length:
		res.append(pos)
	return res

//--------------

void setup_ships(sea_side, fleet_conf):
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

void randomly_place_ship(size, sea):
	sea_side = int(math.sqrt(len(sea)))
	pos = generate_random_position(size, sea_side)
	while not is_squares_available(sea, pos):
		pos = generate_random_position(size, sea_side)
	occupy_squares(sea, pos)
	return pos

void generate_random_position(ship_size, sea_side):
	horizontal = random.choice((True, False))
	x = random.randrange(sea_side - (ship_size if horizontal else 0))
	y = random.randrange(sea_side - (0 if horizontal else ship_size))
	return (x, y, ship_size, horizontal)

void is_squares_available(sea, ship):
	sea_side = int(math.sqrt(len(sea)))
	x, y, ship_size, horizontal = ship
	index = y * sea_side + x
	orient = 1 if horizontal else sea_side
	for i in [index + i * orient for i in xrange(ship_size)]:
		if sea[i] != ' ':
			return False
	return True

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
