==================
Battleship Project
==================

Following is formal game rules pseudo code:

# table form:

context = BattleshipGame()

states = [
	# state           # entry action  # Exit action
	{BATTLE_STARTED,  reset_game,     NULL},
	{PLAYER_TURN,     NULL,           NULL},
	{BATTLE_ENDED,    NULL,           NULL}]

transitions = [
	# state           # input       # condition            # transition   # action
	{BATTLE_STARTED   player_setup  all_players_set        PLAYER_TURN             },
	{PLAYER_TURN      player_shoot  shot_missed            PLAYER_TURN    pass_turn},
	{PLAYER_TURN      player_shoot  opponent_has_no_ships  BATTLE_ENDED            },
	{BATTLE_ENDED     new_game                             BATTLE_STARTED          }]

input action


# object form:

game = BattleshipGame()

logic = MealyMachine() # Finite State Transducer
battle_started = logic.addState(BATTLE_STARTED)
  player_setup = battle_started.addEvent(PLAYER_SETUP)
    player_setup.addTransition(all_players_set, PLAYER_TURN)
player_turn = logic.addState(PLAYER_TURN)
  player_shoot = player_turn.addEvent(PLAYER_SHOOT, game.shotValidator)
    player_shoot.addTransition(game.shotMissed, PLAYER_TURN, game.passTurn)
    player_shoot.addTransition(game.opponentHasNoShips, BATTLE_ENDED)
battle_ended logic.addState(BATTLE_ENDED)
  new_game = battle_ended.addEvent(NEW_GAME)
	  new_game.addTransition(NULL, BATTLE_STARTED)



# usage example:

logic.state(BATTLE_STARTED)
logic.dispatch(PLAYER_SETUP, EventData(PLAYER1, (3,4,...)))
logic.dispatch(PLAYER_SETUP, EventData(PLAYER2, (5,6,...)))
logic.dispatch(PLAYER_SHOOT, EventData(PLAYER1, (7,8)))
