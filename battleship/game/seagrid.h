#pragma once

enum SQUARE
{
	AVAILABLE,
	OCCUPIED,
	BLOCKED
};

class SeaGrid
{
public:
	SeaGrid(unsigned short side);
	~SeaGrid(void);
	bool IsSquaresAvailable(int squares[], int squares_len);
	void OccupySquares(int squares[], int squares_len);
	unsigned int SideSize() { return m_sideSize; }

private:
	SQUARE* m_grid;  // array
	int m_gridSize;
	unsigned int m_sideSize;
};
