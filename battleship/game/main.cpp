#include <iostream>
#include <vector>
#include <map>
#include <exception>

#include "logic.h"
#include "ai.h"
#include "board.h"

void print_sea(logic::Game& game, logic::PLAYER_HANDLE player_id, board::Pos& last_shot, board::SHOT res)
{
	int rows = 10;
	int side = rows*2+1;
	std::vector<char> grid((rows*side), ' ');
	const std::vector<board::Pos> shots = game.GetPlayerShots(player_id);
	for (std::vector<board::Pos>::const_iterator it = shots.begin(); it != shots.end(); it++)
		grid[(*it).y * side + (*it).x * 2 + 1] = '.';
	const std::vector<board::Ship> ships = game.GetOpponentShips(player_id);
	for (std::vector<board::Ship>::const_iterator it=ships.begin(); it != ships.end(); it++)
	{
		const std::vector<board::ShipSegment> segments = (*it).segments;
		for (std::vector<board::ShipSegment>::const_iterator it=segments.begin(); it != segments.end(); it++)
			grid[(*it).pos.y * side + (*it).pos.x * 2 + 1] = (*it).active ? ' ' : 'x';
	}
	grid[last_shot.y * side + last_shot.x*2] = '[';
	grid[last_shot.y * side + last_shot.x*2+2] = ']';
	char padding[] = "                                        ";
	if (player_id == 0) padding [39] = '|'; // PLAYER1
	for (int i=0; i < rows; i++)
	{
		std::cout << padding;
		for (int j = i * side; j < (i + 1) * side; j++)
			std::cout << grid[j];
	}
	std::cout << padding << player_id << ' ' << res << ' ' << last_shot.x << ',' << last_shot.y << '\n';
}

int main(int argc, char *argv[])
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
			throw std::exception("unknown state");
		}
	}
	return 0;
}
