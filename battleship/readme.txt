==================
Battleship Project
==================

Following is formal game rules pseudo code:

[russian]

state.STARTED:
  event: player_setup(player_id, ships)
    all_players_set: goto_state(INPROGRESS)
state.INPROGRESS:
  event: player_shoot(player_id, shots)
    atleast_one_player_has_no_ships: goto_state(ENDED)
    all_players_placed_shots: goto_state(INPROGRESS)
state.ENDED:
  event: new_game()
    default: goto_state(STARTED)


[american?]
