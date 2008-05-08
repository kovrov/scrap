#include "computerplayer.h"
#include <stdlib.h>
#include <assert.h>

ComputerPlayer::ComputerPlayer()
{
}

ComputerPlayer::~ComputerPlayer()
{
}


/* helper functions */
void generate_random_position(int out_buffer[], unsigned int ship_size, unsigned int sea_side)
{
	assert (ship_size > 0);
	assert (out_buffer != NULL);
	assert (ship_size < sea_side);
	bool horizontal = rand() % 2 ? true : false;
	int h = rand() % (sea_side - (horizontal ? ship_size : 0));
	int v = rand() % (sea_side - (horizontal ? 0 : ship_size));
	int index = v * sea_side + h;
	int orient = horizontal ? 1 : sea_side;
	for (unsigned int i=0; i < ship_size; i++)
		out_buffer[i] = index + i * orient;
}

void randomly_place_ship(SeaGrid* sea, unsigned int size)
{
	assert (sea != NULL);
	unsigned int sea_side = sea->SideSize();
	int* ship_pos = new int[size];
	generate_random_position(ship_pos, size, sea_side);
	while (!sea->IsSquaresAvailable(ship_pos, size))
		generate_random_position(ship_pos, size, sea_side);
	sea->OccupySquares(ship_pos, size);
	delete[] ship_pos;
}



void ComputerPlayer::PlaceShips(SeaGrid* sea, const Config& config)
{
	assert (sea != NULL);
	assert (config.len > 0);
	assert (config.ptr != NULL);
	for (unsigned int i=0; i < config.len; i++)
	{
		for (unsigned int i=0; i < config.ptr[i].quantity; i++)
		{
			randomly_place_ship(sea, config.ptr[i].size);
		}
	}
}

void ComputerPlayer::Shoot()
{
	//m_shotsTable[]
}
