#ifdef _DEBUG
	#define _CRTDBG_MAP_ALLOC
	#include <stdlib.h>
	#include <crtdbg.h>
#endif

#include <iostream>
#include <vector>
#include <map>
#include <exception>
#include <stdlib.h>
#include <time.h>

#include "../game/logic.h"
#include "../game/ai.h"
#include "../game/board.h"

#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH


void print_sea(logic::Game& game, logic::PLAYER_HANDLE player_id, board::Pos& last_shot, board::SHOT res)
{
	int rows = 10;
	int side = rows * 2 + 1;
	std::vector<char> grid(rows * side, ' ');

	foreach (const board::Shot& shot, game.GetPlayerShots(player_id))
		grid[shot.y * side + shot.x * 2 + 1] = '.';

	foreach (const board::Ship& ship, game.GetOpponentShips(player_id))
	{
		foreach (const board::ShipSegment& segment, ship.segments)
			grid[segment.pos.y * side + segment.pos.x * 2 + 1] = segment.active ? ' ' : 'x';
	}
	grid[last_shot.y * side + last_shot.x * 2] = '[';
	grid[last_shot.y * side + last_shot.x * 2 + 2] = ']';
	const char* padding = (player_id == 0) ? "                                       |" : "";
	for (int i=0; i < rows; i++)
	{
		std::cout << padding;
		for (int j = i * side; j < (i + 1) * side; j++)
			std::cout << grid[j];
		std::cout << '\n';
	}
	std::cout << padding
		<< " PLAYER_" << player_id << ' '
		<< res << ' '
		<< last_shot.x << ',' << last_shot.y << "\n\n";
}

void run()
{
	logic::PLAYER_HANDLE PLAYER1 = 0;
	logic::PLAYER_HANDLE PLAYER2 = 1;
	logic::Game game(PLAYER1, PLAYER2);
	std::map<logic::PLAYER_HANDLE, ai::ComputerPlayer> players;
	std::map<logic::PLAYER_HANDLE, int> shots_made;
	while (true)
	{
		logic::STATE state = game.GetState();
		if (state == logic::BATTLE_STARTED)
		{
			game.Setup(PLAYER1, ai::setup_ships(10, game.GetConfig()));
			game.Setup(PLAYER2, ai::setup_ships(10, game.GetConfig()));
			players[PLAYER1] = ai::ComputerPlayer(10, game.GetConfig());
			players[PLAYER2] = ai::ComputerPlayer(10, game.GetConfig());
			shots_made[PLAYER1] = shots_made[PLAYER2] = 0;
		}
		else if (state == logic::PLAYER_TURN)
		{
			logic::PLAYER_HANDLE current_player_id = game.GetCurrentPlayer();
			ai::ComputerPlayer& current_player = players[current_player_id];
			board::Pos shot = current_player.Shot();
			board::SHOT res = game.Shoot(current_player_id, shot);
			current_player.Track(shot, res);
			shots_made[current_player_id] += 1;
			print_sea(game, current_player_id, shot, res);
		}
		else if (state == logic::BATTLE_ENDED)
		{
			printf("# BATTLE ENDED\n");
			printf("%d win, shots made: %d\n", game.GetCurrentPlayer(), shots_made[game.GetCurrentPlayer()]);
			break;
		}
		else
		{
			throw std::exception();  // unknown state
		}
	}
}

int main(int argc, char* argv[])
{
	srand((unsigned)time(NULL));
	run();
	#ifdef _DEBUG
		_CrtDumpMemoryLeaks();
	#endif
	return 0;
}
