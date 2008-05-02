#include "seagrid.h"
#include <assert.h>


SeaGrid::SeaGrid(unsigned short side)
{
	m_gridSize = side * side;
	m_grid = new SQUARE[m_gridSize];
}


SeaGrid::~SeaGrid(void)
{
	delete m_grid;
}


bool SeaGrid::IsSquaresAvailable(int squares[], int squares_len)
{
	for (int i=0; i < squares_len; i++)
	{
		assert (squares[i] < m_gridSize);
		if (m_grid[squares[i]] != AVAILABLE)
			return false;
	}
	return true;
}


/* "not in array" helper function */
inline bool not_in(int value, int array[], int array_len)
{
	for (int i=0; i < array_len; i++)
	{
		if (value == array[i])
			return false;
	}
	return true;
}


void SeaGrid::OccupySquares(int squares[], int squares_len)
{
	assert (IsSquaresAvailable(squares, squares_len));

	for (int i = 0; i < squares_len; i++)
	{
		assert (m_grid[i] == AVAILABLE);
		m_grid[i] = OCCUPIED;

		// horizontal margin
		int pos = i - 1;  // left
		if (i % m_sideSize != 0 && pos >= 0 && pos < m_gridSize)
		{
			if (not_in(pos, squares, squares_len))
			{
				assert (m_grid[pos] != OCCUPIED);
				m_grid[pos] = BLOCKED;
			}
		}
		pos = i + 1;  // right
		if (pos % m_sideSize != 0 && pos >= 0 && pos < m_gridSize)
		{
			if (not_in(pos, squares, squares_len))
			{
				assert (m_grid[pos] != OCCUPIED);
				m_grid[pos] = BLOCKED;
			}
		}

		// vertical margin
		pos = i - m_sideSize;  // up
		if (pos >= 0 && pos < m_gridSize)
		{
			if (not_in(pos, squares, squares_len))
			{
				assert (m_grid[pos] != OCCUPIED);
				m_grid[pos] = BLOCKED;
			}
		}
		pos = i + m_sideSize;  // down
		if (pos >= 0 && pos < m_gridSize)
		{
			if (not_in(pos, squares, squares_len))
			{
				assert (m_grid[pos] != OCCUPIED);
				m_grid[pos] = BLOCKED;
			}
		}

		// diagonal margin
		pos = i - m_sideSize + 1;  // upper-right
		if (pos % m_sideSize != 0 && pos >= 0 && pos < m_gridSize)
		{
			assert (m_grid[pos] != OCCUPIED);
			m_grid[pos] = BLOCKED;
		}
		pos = i - m_sideSize - 1;  // upper-left
		if (i % m_sideSize != 0 && pos >= 0 && pos < m_gridSize)
		{
			assert (m_grid[pos] != OCCUPIED);
			m_grid[pos] = BLOCKED;
		}
		pos = i + m_sideSize + 1;  // lower-right
		if (pos % m_sideSize != 0 && pos >= 0 && pos < m_gridSize)
		{
			assert (m_grid[pos] != OCCUPIED);
			m_grid[pos] = BLOCKED;
		}
		pos = i + m_sideSize - 1;  // lower-left
		if (i % m_sideSize != 0 && pos >= 0 && pos < m_gridSize)
		{
			assert (m_grid[pos] != OCCUPIED);
			m_grid[pos] = BLOCKED;
		}
	}
}
