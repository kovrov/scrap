
#include <stdio.h>
#include <tchar.h>
#include <stack>
#include <assert.h>

enum Direction
{
   left     = 1, // move left  (x-1)
   backward = 2, // move down  (y-1)
   right    = 3, // move right (x+1)
   forward  = 4  // move up    (y+1)
};


class classMaze
{
public:
   // Initialize:  1. Creates a session
   //              2. Creates a random maze which can be as large as 100 X 100
   //              3. Places a 'mouse' in the maze at a random location
   //              4. Places a 'piece of cheese' in the maze at a random location
   void Initialize();


   // Move: Try to move the mouse in the direction specified.
   //
   //       Returns:  False if the move could not be performed
   //                 True if the move was performed
   bool Move( Direction tryMovingMouseInThisDirection );


   // Success: Determines if the mouse is at the same place in the maze as
   //          the cheese
   //
   //          Returns:  True if the mouse and cheese are at the same place
   //                    False if the mouse is not at the same location as
   //                          the cheese
   bool Success();
};

enum Status
{
   UNKNOWN = 1,
   POSSIBLE = 2,
   DEADEND = 3
};

enum Availability
{
	yes,
	no,
	perhaps // =)
};

struct Pos
{
	Pos(int ix, int iy)
	{
		x = ix;
		y = ix;
	}
	int x;
	int y;
};

struct PosState
{
	PosState(Pos& p)
	:	pos(p)
	{
		left = perhaps;
		right = perhaps;
		top = perhaps;
		bottom = perhaps;
	}
	Pos pos;
	Availability left;
	Availability right;
	Availability top;
	Availability bottom;
};

struct BackHint
{
	BackHint(PosState& p)
	: ps (p)
	{
		backdir = (Direction)0; // unknown
	}
	PosState ps;
	Direction backdir;
};


Pos solve(classMaze* maze)
{
	int mazeMap[200][200]; // considering maze max sile is 100
	memset(mazeMap, UNKNOWN, 200*200);
	maze->Initialize();

	Pos pos(0,0);
	std::stack<BackHint> back;

	while (!maze->Success())
	{
		// check ...
		switch (mazeMap[pos.x][pos.y])
		{
		case DEADEND:
			// go back stack
			{
			BackHint hint = back.top();
			assert (maze->Move(hint.backdir));
			back.pop();
			pos = hint.ps.pos;
			}
			break;

		default:
			// continue exploration
			if (pos.x > -100 && maze->Move(left))
			{
				pos.x -= 1;
				mazeMap[pos.x][pos.y] = POSSIBLE;
				PosState ps(pos);
				ps.right = yes;
				back.push(BackHint(ps));
			}

			else if (pos.x < 100 && maze->Move(right))
			{
				pos.x += 1;
				mazeMap[pos.x][pos.y] = POSSIBLE;
				PosState ps(pos);
				ps.left = yes;
				back.push(BackHint(ps));
			}

			else if (pos.y > -100 && maze->Move(backward))
			{
				pos.y -= 1;
				mazeMap[pos.x][pos.y] = POSSIBLE;
				PosState ps(pos);
				ps.top = yes;
				back.push(BackHint(ps));
			}

			else if (pos.y < 100 && maze->Move(forward))
			{
				pos.y += 1;
				mazeMap[pos.x][pos.y] = POSSIBLE;
				PosState ps(pos);
				ps.bottom = yes;
				back.push(BackHint(ps));
			}

			else
			{
				mazeMap[pos.x][pos.y] = DEADEND;
				// dead end?
			}
		}
	}
	return pos;
}

int main(int argc, char* argv[])
{
	return 0;
}

